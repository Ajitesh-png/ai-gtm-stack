"""
Notch keyword-metrics helper for the blog-opportunity finder.

Graceful-degradation keyword data. Tries each configured provider in
waterfall order; skips any whose API key is missing. If NO provider is
configured, it returns the requested keywords with null metrics and sets
`fallback_required: true` so the calling skill knows to estimate volume /
difficulty via WebSearch + SERP inspection instead.

Two modes:

    # Pull metrics (volume, KD, CPC, intent, SERP features) for known keywords
    python keyword_metrics.py metrics --keywords "ai advertising,ai ad generator"

    # Expand a seed into related keyword ideas (with metrics attached)
    python keyword_metrics.py expand --seed "agentic video ads" --limit 100

    # Show which providers are wired up and exit
    python keyword_metrics.py --show-config

Output: JSON to stdout. Diagnostics go to stderr.

Environment (reads from pipelines/seo-opportunity-engine/.env first, then project .env):
    DATAFORSEO_LOGIN + DATAFORSEO_PASSWORD   - primary (Labs API, pay-as-you-go)
    SEMRUSH_API_KEY                          - fallback (Analytics API)
    AHREFS_API_TOKEN                         - fallback (v3 Keywords Explorer)

This script NEVER fabricates metrics. A missing number stays null and the
record is flagged so the skill can estimate it transparently.

Geo defaults to United States (location_code 2840, language "en") — matches
the US keyword data the SEO strategy docs are built on. Override with --location.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print(
        json.dumps(
            {
                "error": "requests not installed. Run: pip install requests",
                "provider_used": None,
                "fallback_required": True,
            }
        )
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Env loading (pipelines/seo-opportunity-engine/.env first, then project .env)
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[3]
ENV_PATHS = [
    ROOT / "pipelines" / "seo-opportunity-engine" / ".env",
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


def have(key: str) -> bool:
    v = os.environ.get(key, "").strip()
    return bool(v) and not v.lower().startswith(("your_", "<", "xxx"))


PROVIDERS = {
    "dataforseo": have("DATAFORSEO_LOGIN") and have("DATAFORSEO_PASSWORD"),
    "semrush": have("SEMRUSH_API_KEY"),
    "ahrefs": have("AHREFS_API_TOKEN"),
}

# Order matters: DataForSEO is primary per the SEO setup.
PROVIDER_ORDER = ["dataforseo", "semrush", "ahrefs"]


# ---------------------------------------------------------------------------
# Geo / language
# ---------------------------------------------------------------------------

LOCATION_CODES = {
    "united states": 2840,
    "us": 2840,
    "united kingdom": 2826,
    "uk": 2826,
    "canada": 2124,
    "australia": 2036,
    "india": 2356,
}


def location_code(name: str) -> int:
    return LOCATION_CODES.get(name.strip().lower(), 2840)


def normalize_record(
    keyword: str,
    search_volume: Optional[int] = None,
    keyword_difficulty: Optional[float] = None,
    cpc: Optional[float] = None,
    competition: Optional[float] = None,
    search_intent: Optional[str] = None,
    serp_features: Optional[list] = None,
) -> dict:
    return {
        "keyword": keyword,
        "search_volume": search_volume,
        "keyword_difficulty": keyword_difficulty,
        "cpc": round(cpc, 2) if isinstance(cpc, (int, float)) else None,
        "competition": competition,
        "search_intent": search_intent,
        "serp_features": serp_features or [],
    }


# ---------------------------------------------------------------------------
# DataForSEO (primary) — Labs API, HTTP Basic auth
# ---------------------------------------------------------------------------

DFS_BASE = "https://api.dataforseo.com"


def _dfs_auth() -> tuple[str, str]:
    return (os.environ["DATAFORSEO_LOGIN"], os.environ["DATAFORSEO_PASSWORD"])


def _dfs_post(endpoint: str, body: list) -> Optional[dict]:
    try:
        r = requests.post(
            f"{DFS_BASE}{endpoint}",
            auth=_dfs_auth(),
            json=body,
            headers={"Content-Type": "application/json"},
            timeout=90,
        )
    except requests.RequestException as exc:
        print(f"dataforseo request error: {exc}", file=sys.stderr)
        return None
    if r.status_code != 200:
        print(f"dataforseo status={r.status_code}: {r.text[:200]}", file=sys.stderr)
        return None
    data = r.json() or {}
    tasks = data.get("tasks") or []
    if not tasks or tasks[0].get("status_code") != 20000:
        msg = tasks[0].get("status_message") if tasks else data.get("status_message")
        print(f"dataforseo task error: {msg}", file=sys.stderr)
        return None
    return tasks[0]


def _dfs_extract(item: dict) -> dict:
    """Map a DataForSEO Labs item to our normalized record."""
    kw = item.get("keyword")
    ki = item.get("keyword_info") or {}
    kp = item.get("keyword_properties") or {}
    si = item.get("search_intent_info") or {}
    serp = item.get("serp_info") or {}
    features = serp.get("serp_item_types") or []
    return normalize_record(
        keyword=kw,
        search_volume=ki.get("search_volume"),
        keyword_difficulty=kp.get("keyword_difficulty"),
        cpc=ki.get("cpc"),
        competition=ki.get("competition"),
        search_intent=si.get("main_intent"),
        serp_features=features,
    )


def dfs_metrics(keywords: list[str], loc: int) -> Optional[list[dict]]:
    body = [
        {
            "keywords": keywords,
            "language_code": "en",
            "location_code": loc,
            "include_serp_info": True,
        }
    ]
    task = _dfs_post("/v3/dataforseo_labs/google/keyword_overview/live", body)
    if task is None:
        return None
    items = (task.get("result") or [{}])[0].get("items") or []
    # keyword_overview only returns keywords present in DataForSEO's DB; ones
    # with no data are silently dropped. Reconcile so every requested keyword
    # comes back — missing ones as null records (likely near-zero volume).
    by_kw = {}
    for it in items:
        rec = _dfs_extract(it)
        if rec["keyword"]:
            by_kw[rec["keyword"].strip().lower()] = rec
    out = []
    for kw in keywords:
        rec = by_kw.get(kw.strip().lower())
        if rec is None:
            rec = normalize_record(kw)
            rec["_note"] = "not in DataForSEO DB (likely near-zero volume)"
        out.append(rec)
    return out


def dfs_expand(seed: str, loc: int, limit: int) -> Optional[list[dict]]:
    body = [
        {
            "keyword": seed,
            "language_code": "en",
            "location_code": loc,
            "limit": limit,
            "include_serp_info": True,
            "order_by": ["keyword_info.search_volume,desc"],
        }
    ]
    task = _dfs_post("/v3/dataforseo_labs/google/keyword_suggestions/live", body)
    if task is None:
        return None
    items = (task.get("result") or [{}])[0].get("items") or []
    return [_dfs_extract(it) for it in items]


# ---------------------------------------------------------------------------
# Semrush (fallback) — Analytics API, simple GET, CSV-ish response
# ---------------------------------------------------------------------------

SEMRUSH_BASE = "https://api.semrush.com"
# Semrush database codes (geo). 'us' is the default.
SEMRUSH_DB = {2840: "us", 2826: "uk", 2124: "ca", 2036: "au", 2356: "in"}


def _semrush_parse(text: str) -> list[dict]:
    """Semrush returns ';'-separated rows with a header line."""
    lines = [ln for ln in text.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        return []
    headers = [h.strip() for h in lines[0].split(";")]
    rows = []
    for ln in lines[1:]:
        vals = ln.split(";")
        rows.append(dict(zip(headers, vals)))
    return rows


def _semrush_to_record(row: dict) -> dict:
    def num(*keys):
        for k in keys:
            if k in row and row[k] not in ("", None):
                try:
                    return float(row[k])
                except ValueError:
                    return None
        return None

    sv = num("Search Volume")
    return normalize_record(
        keyword=row.get("Keyword"),
        search_volume=int(sv) if sv is not None else None,
        keyword_difficulty=num("Keyword Difficulty Index", "Competition"),
        cpc=num("CPC"),
        competition=num("Competition"),
        search_intent=row.get("Intent") or None,
        serp_features=[
            f.strip() for f in (row.get("SERP Features") or "").split(",") if f.strip()
        ],
    )


def semrush_metrics(keywords: list[str], loc: int) -> Optional[list[dict]]:
    db = SEMRUSH_DB.get(loc, "us")
    out: list[dict] = []
    for kw in keywords:
        try:
            r = requests.get(
                SEMRUSH_BASE,
                params={
                    "type": "phrase_this",
                    "key": os.environ["SEMRUSH_API_KEY"],
                    "phrase": kw,
                    "database": db,
                    "export_columns": "Ph,Nq,Cp,Co,Kd,In,Fk",
                },
                timeout=60,
            )
        except requests.RequestException as exc:
            print(f"semrush request error: {exc}", file=sys.stderr)
            continue
        if r.status_code != 200 or r.text.startswith("ERROR"):
            print(f"semrush error for '{kw}': {r.text[:120]}", file=sys.stderr)
            continue
        rows = _semrush_parse(r.text)
        if rows:
            out.append(_semrush_to_record(rows[0]))
        else:
            out.append(normalize_record(kw))
    return out or None


def semrush_expand(seed: str, loc: int, limit: int) -> Optional[list[dict]]:
    db = SEMRUSH_DB.get(loc, "us")
    try:
        r = requests.get(
            SEMRUSH_BASE,
            params={
                "type": "phrase_related",
                "key": os.environ["SEMRUSH_API_KEY"],
                "phrase": seed,
                "database": db,
                "display_limit": limit,
                "export_columns": "Ph,Nq,Cp,Co,Kd,In",
            },
            timeout=90,
        )
    except requests.RequestException as exc:
        print(f"semrush expand error: {exc}", file=sys.stderr)
        return None
    if r.status_code != 200 or r.text.startswith("ERROR"):
        print(f"semrush expand error: {r.text[:120]}", file=sys.stderr)
        return None
    return [_semrush_to_record(row) for row in _semrush_parse(r.text)]


# ---------------------------------------------------------------------------
# Ahrefs (fallback) — API v3 Keywords Explorer
# ---------------------------------------------------------------------------

AHREFS_BASE = "https://api.ahrefs.com/v3"
AHREFS_COUNTRY = {2840: "us", 2826: "gb", 2124: "ca", 2036: "au", 2356: "in"}


def _ahrefs_headers() -> dict:
    return {
        "Authorization": f"Bearer {os.environ['AHREFS_API_TOKEN']}",
        "Accept": "application/json",
    }


def ahrefs_metrics(keywords: list[str], loc: int) -> Optional[list[dict]]:
    country = AHREFS_COUNTRY.get(loc, "us")
    try:
        r = requests.get(
            f"{AHREFS_BASE}/keywords-explorer/overview",
            headers=_ahrefs_headers(),
            params={
                "country": country,
                "keywords": ",".join(keywords),
                "select": "keyword,volume,difficulty,cpc",
            },
            timeout=90,
        )
    except requests.RequestException as exc:
        print(f"ahrefs request error: {exc}", file=sys.stderr)
        return None
    if r.status_code != 200:
        print(f"ahrefs status={r.status_code}: {r.text[:200]}", file=sys.stderr)
        return None
    rows = (r.json() or {}).get("keywords") or (r.json() or {}).get("results") or []
    out = []
    for row in rows:
        out.append(
            normalize_record(
                keyword=row.get("keyword"),
                search_volume=row.get("volume"),
                keyword_difficulty=row.get("difficulty"),
                cpc=row.get("cpc"),
            )
        )
    return out or None


def ahrefs_expand(seed: str, loc: int, limit: int) -> Optional[list[dict]]:
    country = AHREFS_COUNTRY.get(loc, "us")
    try:
        r = requests.get(
            f"{AHREFS_BASE}/keywords-explorer/matching-terms",
            headers=_ahrefs_headers(),
            params={
                "country": country,
                "keywords": seed,
                "select": "keyword,volume,difficulty,cpc",
                "limit": limit,
            },
            timeout=120,
        )
    except requests.RequestException as exc:
        print(f"ahrefs expand error: {exc}", file=sys.stderr)
        return None
    if r.status_code != 200:
        print(f"ahrefs expand status={r.status_code}: {r.text[:200]}", file=sys.stderr)
        return None
    rows = (r.json() or {}).get("keywords") or (r.json() or {}).get("results") or []
    return [
        normalize_record(
            keyword=row.get("keyword"),
            search_volume=row.get("volume"),
            keyword_difficulty=row.get("difficulty"),
            cpc=row.get("cpc"),
        )
        for row in rows
    ]


# ---------------------------------------------------------------------------
# Waterfall orchestration
# ---------------------------------------------------------------------------

METRIC_FNS = {
    "dataforseo": dfs_metrics,
    "semrush": semrush_metrics,
    "ahrefs": ahrefs_metrics,
}
EXPAND_FNS = {
    "dataforseo": dfs_expand,
    "semrush": semrush_expand,
    "ahrefs": ahrefs_expand,
}


def run_waterfall(mode: str, loc: int, **kwargs) -> dict:
    fns = METRIC_FNS if mode == "metrics" else EXPAND_FNS
    used = None
    skipped: list[str] = []
    failed: list[str] = []
    results: list[dict] = []

    for name in PROVIDER_ORDER:
        if not PROVIDERS[name]:
            skipped.append(name)
            continue
        try:
            if mode == "metrics":
                res = fns[name](kwargs["keywords"], loc)
            else:
                res = fns[name](kwargs["seed"], loc, kwargs["limit"])
        except Exception as exc:  # noqa: BLE001 - provider isolation
            print(f"{name} unexpected error: {exc}", file=sys.stderr)
            failed.append(name)
            continue
        if res:
            used = name
            results = res
            break
        failed.append(name)

    fallback_required = used is None
    if fallback_required and mode == "metrics":
        # Echo requested keywords with null metrics so the skill can fill via WebSearch.
        results = [normalize_record(k) for k in kwargs["keywords"]]

    return {
        "mode": mode,
        "provider_used": used,
        "providers_skipped": skipped,
        "providers_failed": failed,
        "fallback_required": fallback_required,
        "location_code": loc,
        "results": results,
        "note": (
            "No keyword API configured or all providers failed. Metrics are null; "
            "estimate search_volume / keyword_difficulty via WebSearch + SERP "
            "inspection and mark each as estimated in the backlog."
            if fallback_required
            else None
        ),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["metrics", "expand"],
        help="metrics: pull data for given keywords. expand: ideas from a seed.",
    )
    parser.add_argument("--keywords", help="Comma-separated keywords (metrics mode)")
    parser.add_argument("--seed", help="Seed phrase to expand (expand mode)")
    parser.add_argument("--limit", type=int, default=100, help="Max ideas (expand)")
    parser.add_argument("--location", default="united states", help="Geo name")
    parser.add_argument(
        "--show-config", action="store_true", help="Print configured providers and exit"
    )
    args = parser.parse_args()

    if args.show_config:
        print(json.dumps({"providers_configured": PROVIDERS, "order": PROVIDER_ORDER}, indent=2))
        return 0

    loc = location_code(args.location)

    if args.mode == "metrics":
        if not args.keywords:
            parser.error("metrics mode needs --keywords")
        kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        out = run_waterfall("metrics", loc, keywords=kws)
    elif args.mode == "expand":
        if not args.seed:
            parser.error("expand mode needs --seed")
        out = run_waterfall("expand", loc, seed=args.seed, limit=args.limit)
    else:
        parser.error("provide a mode: metrics | expand  (or --show-config)")
        return 2

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
