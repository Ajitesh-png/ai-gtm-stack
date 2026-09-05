"""
Notch lead-finder enrichment helper.

Graceful-degradation enrichment for a single lead. Tries each configured
provider in waterfall order; skips any whose API key is missing.

Usage (CLI):
    python enrich.py --linkedin-url https://linkedin.com/in/example
    python enrich.py --name "Jane Doe" --company "Acme Co"
    python enrich.py --twitter-handle exampleuser

Output: JSON to stdout with whichever fields could be filled.
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@acme.com",
        "company": "Acme Co",
        "title": "Head of Growth",
        "linkedin_url": "...",
        "twitter_url": "...",
        "providers_used": ["apollo", "hunter"],
        "providers_skipped": ["apify"],
        "providers_failed": [],
        "needs_enrichment": ["title_unverified"]
    }

Environment (reads from outreach-engine/.env if present):
    APOLLO_API_KEY    - Apollo.io (primary enrichment + email finder)
    HUNTER_API_KEY    - Hunter.io (email backup, pattern search)
    APIFY_TOKEN       - Apify (LinkedIn + X scraping)
    NEVERBOUNCE_API_KEY - Optional email validation

This script is intentionally conservative. It NEVER fabricates data.
Missing fields stay null and are reported in `needs_enrichment`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print(
        json.dumps(
            {
                "error": "requests library not installed. Run: pip install requests",
                "providers_used": [],
                "providers_skipped": [],
                "providers_failed": [],
            }
        ),
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Env loading (look for outreach-engine/.env first, then project .env)
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]
ENV_PATHS = [
    ROOT / "outreach-engine" / ".env",
    ROOT / ".env",
]


def load_env() -> None:
    """Lightweight .env loader. Doesn't override existing env vars."""
    for path in ENV_PATHS:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = value


load_env()


# ---------------------------------------------------------------------------
# Provider checks
# ---------------------------------------------------------------------------


def have(key: str) -> bool:
    v = os.environ.get(key, "").strip()
    return bool(v) and not v.startswith("your_")


PROVIDERS = {
    "apollo": have("APOLLO_API_KEY"),
    "hunter": have("HUNTER_API_KEY"),
    "apify": have("APIFY_TOKEN"),
    "neverbounce": have("NEVERBOUNCE_API_KEY"),
}


# ---------------------------------------------------------------------------
# Result accumulator
# ---------------------------------------------------------------------------


class EnrichmentResult:
    def __init__(self) -> None:
        self.data: dict = {
            "first_name": None,
            "last_name": None,
            "email": None,
            "company": None,
            "title": None,
            "linkedin_url": None,
            "twitter_url": None,
        }
        self.providers_used: list[str] = []
        self.providers_skipped: list[str] = []
        self.providers_failed: list[str] = []
        self.needs_enrichment: list[str] = []
        self.notes: list[str] = []

    def fill(self, field: str, value: Optional[str], provider: str) -> None:
        if not value:
            return
        if self.data.get(field):
            return
        self.data[field] = value.strip()
        if provider not in self.providers_used:
            self.providers_used.append(provider)

    def skipped(self, provider: str, reason: str) -> None:
        if provider not in self.providers_skipped:
            self.providers_skipped.append(provider)
            self.notes.append(f"{provider}: {reason}")

    def failed(self, provider: str, reason: str) -> None:
        if provider not in self.providers_failed:
            self.providers_failed.append(provider)
            self.notes.append(f"{provider} failed: {reason}")

    def finalize(self) -> dict:
        missing = [k for k, v in self.data.items() if v is None]
        for m in missing:
            self.needs_enrichment.append(m)
        return {
            **self.data,
            "providers_used": self.providers_used,
            "providers_skipped": self.providers_skipped,
            "providers_failed": self.providers_failed,
            "needs_enrichment": self.needs_enrichment,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Apollo enrichment
# ---------------------------------------------------------------------------


def enrich_via_apollo(
    result: EnrichmentResult,
    linkedin_url: Optional[str] = None,
    name: Optional[str] = None,
    company: Optional[str] = None,
) -> None:
    if not PROVIDERS["apollo"]:
        result.skipped("apollo", "APOLLO_API_KEY not configured")
        return

    api_key = os.environ["APOLLO_API_KEY"]
    payload: dict = {"reveal_personal_emails": True}
    if linkedin_url:
        payload["linkedin_url"] = linkedin_url
    if name:
        payload["name"] = name
    if company:
        payload["organization_name"] = company

    try:
        r = requests.post(
            "https://api.apollo.io/v1/people/match",
            json=payload,
            headers={
                "Cache-Control": "no-cache",
                "Content-Type": "application/json",
                "X-Api-Key": api_key,
            },
            timeout=30,
        )
        if r.status_code != 200:
            result.failed("apollo", f"status={r.status_code}")
            return
        person = (r.json() or {}).get("person") or {}
        if not person:
            result.failed("apollo", "no match")
            return
        result.fill("first_name", person.get("first_name"), "apollo")
        result.fill("last_name", person.get("last_name"), "apollo")
        result.fill("email", person.get("email"), "apollo")
        result.fill("title", person.get("title"), "apollo")
        result.fill("linkedin_url", person.get("linkedin_url"), "apollo")
        result.fill("twitter_url", person.get("twitter_url"), "apollo")
        org = person.get("organization") or {}
        result.fill("company", org.get("name"), "apollo")
    except requests.RequestException as exc:
        result.failed("apollo", str(exc))


# ---------------------------------------------------------------------------
# Hunter email finder (backup)
# ---------------------------------------------------------------------------


def enrich_via_hunter(result: EnrichmentResult) -> None:
    if not PROVIDERS["hunter"]:
        result.skipped("hunter", "HUNTER_API_KEY not configured")
        return
    if result.data.get("email"):
        return  # already filled
    first = result.data.get("first_name")
    last = result.data.get("last_name")
    company = result.data.get("company")
    if not (first and company):
        result.skipped("hunter", "needs first_name + company; not enough data")
        return

    api_key = os.environ["HUNTER_API_KEY"]
    params = {"api_key": api_key, "company": company, "first_name": first}
    if last:
        params["last_name"] = last

    try:
        r = requests.get(
            "https://api.hunter.io/v2/email-finder",
            params=params,
            timeout=30,
        )
        if r.status_code != 200:
            result.failed("hunter", f"status={r.status_code}")
            return
        data = (r.json() or {}).get("data") or {}
        email = data.get("email")
        if email:
            result.fill("email", email, "hunter")
    except requests.RequestException as exc:
        result.failed("hunter", str(exc))


# ---------------------------------------------------------------------------
# Public LinkedIn profile scrape (last resort, anonymous)
# ---------------------------------------------------------------------------


HEADERS_BROWSER = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def enrich_via_linkedin_public(
    result: EnrichmentResult, linkedin_url: Optional[str]
) -> None:
    """Attempt anonymous fetch of a public LinkedIn profile.

    LinkedIn hides most data behind auth. This will only catch what's in
    the public meta tags (og:title which is usually 'Name | Title' or
    just the name).
    """
    if not linkedin_url:
        return
    if result.data.get("first_name") and result.data.get("last_name"):
        return  # already have name

    try:
        r = requests.get(linkedin_url, headers=HEADERS_BROWSER, timeout=20)
        if r.status_code != 200:
            result.notes.append(
                f"linkedin_public: status={r.status_code} for {linkedin_url}"
            )
            return
        html = r.text
        # og:title is typically "First Last - Title - Company | LinkedIn"
        match = re.search(
            r'<meta property="og:title" content="([^"]+)"', html
        )
        if match:
            title_str = match.group(1)
            parts = [p.strip() for p in re.split(r" [-|] ", title_str) if p.strip()]
            if parts:
                name = parts[0]
                name_bits = name.split(None, 1)
                if len(name_bits) >= 1:
                    result.fill("first_name", name_bits[0], "linkedin_public")
                if len(name_bits) >= 2:
                    result.fill("last_name", name_bits[1], "linkedin_public")
            if len(parts) >= 2:
                # second part often title, third often company
                if not result.data.get("title"):
                    result.fill("title", parts[1], "linkedin_public")
            if len(parts) >= 3 and not result.data.get("company"):
                # strip " | LinkedIn" tail if present
                company = parts[2].split(" | ")[0]
                result.fill("company", company, "linkedin_public")
        result.fill("linkedin_url", linkedin_url, "linkedin_public")
    except requests.RequestException as exc:
        result.failed("linkedin_public", str(exc))


# ---------------------------------------------------------------------------
# Email validation (optional)
# ---------------------------------------------------------------------------


def validate_email(result: EnrichmentResult) -> None:
    email = result.data.get("email")
    if not email:
        return
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        result.notes.append(f"email_invalid_format: {email}")
        result.data["email"] = None
        return
    if not PROVIDERS["neverbounce"]:
        result.skipped("neverbounce", "NEVERBOUNCE_API_KEY not configured")
        return
    try:
        r = requests.get(
            "https://api.neverbounce.com/v4/single/check",
            params={
                "key": os.environ["NEVERBOUNCE_API_KEY"],
                "email": email,
            },
            timeout=20,
        )
        if r.status_code != 200:
            result.failed("neverbounce", f"status={r.status_code}")
            return
        data = r.json() or {}
        verdict = data.get("result")
        if verdict not in {"valid", "catchall"}:
            result.notes.append(f"email_validation: {verdict}")
            result.data["email"] = None
        else:
            result.notes.append(f"email_validation: {verdict}")
            result.providers_used.append("neverbounce")
    except requests.RequestException as exc:
        result.failed("neverbounce", str(exc))


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def enrich(
    linkedin_url: Optional[str] = None,
    name: Optional[str] = None,
    company: Optional[str] = None,
    twitter_handle: Optional[str] = None,
) -> dict:
    result = EnrichmentResult()
    if linkedin_url:
        result.data["linkedin_url"] = linkedin_url
    if twitter_handle:
        handle = twitter_handle.lstrip("@")
        result.data["twitter_url"] = f"https://x.com/{handle}"
    if name:
        bits = name.strip().split(None, 1)
        if len(bits) >= 1:
            result.fill("first_name", bits[0], "input")
        if len(bits) >= 2:
            result.fill("last_name", bits[1], "input")
    if company:
        result.fill("company", company, "input")

    # Waterfall
    enrich_via_apollo(result, linkedin_url=linkedin_url, name=name, company=company)
    enrich_via_linkedin_public(result, linkedin_url)
    enrich_via_hunter(result)
    validate_email(result)

    return result.finalize()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--linkedin-url", help="LinkedIn profile URL")
    parser.add_argument("--twitter-handle", help="X/Twitter handle (with or without @)")
    parser.add_argument("--name", help="Full display name")
    parser.add_argument("--company", help="Company name (hint)")
    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Print which providers are configured and exit",
    )
    args = parser.parse_args()

    if args.show_config:
        print(json.dumps({"providers_configured": PROVIDERS}, indent=2))
        return 0

    if not (args.linkedin_url or args.twitter_handle or args.name):
        parser.error(
            "provide at least one of --linkedin-url, --twitter-handle, or --name"
        )

    result = enrich(
        linkedin_url=args.linkedin_url,
        name=args.name,
        company=args.company,
        twitter_handle=args.twitter_handle,
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
