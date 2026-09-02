#!/usr/bin/env python3
"""Fetch curated Frontier Voice posts through the official X API.

The collector is read-only and dependency-free. It reads the bearer token only from
X_BEARER_TOKEN, emits JSON to stdout, and never writes credentials or timeline state.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE_URL = "https://api.x.com"
DEFAULT_HOURS = 36.0
DEFAULT_MAX_PAGES = 3
DEFAULT_TIMEOUT = 30.0
RECENT_HORIZON = timedelta(days=7)
HANDLE_RE = re.compile(r"`@([A-Za-z0-9_]{1,15})`")


class XApiError(RuntimeError):
    """An X API or transport failure safe to expose in structured output."""

    def __init__(self, code: str, message: str, *, status: int | None = None):
        super().__init__(message)
        self.code = code
        self.status = status


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_utc(value: str) -> datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include Z or an explicit UTC offset")
    return parsed.astimezone(timezone.utc)


def format_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def unique_handles(handles: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for raw in handles:
        handle = raw.strip().lstrip("@")
        if not re.fullmatch(r"[A-Za-z0-9_]{1,15}", handle):
            raise ValueError(f"invalid X handle: {raw!r}")
        key = handle.casefold()
        if key not in seen:
            seen.add(key)
            result.append(handle)
    return result


def parse_registry(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    x1_start = text.find("## X1")
    x2_start = text.find("## X2")
    promotion_start = text.find("## Promotion")
    if x1_start < 0 or x2_start < 0 or x2_start <= x1_start:
        raise ValueError(f"could not find X1/X2 sections in {path}")
    if promotion_start < 0:
        promotion_start = len(text)
    x1 = unique_handles(HANDLE_RE.findall(text[x1_start:x2_start]))
    x2 = unique_handles(HANDLE_RE.findall(text[x2_start:promotion_start]))
    if not x1:
        raise ValueError(f"X1 registry is empty in {path}")
    return x1, x2


def select_handles(
    registry: Path,
    end_time: datetime,
    explicit: str | None,
    x2_mode: str,
) -> tuple[list[str], list[str], list[str]]:
    if explicit:
        selected = unique_handles(explicit.split(","))
        return selected, selected, []

    x1, x2 = parse_registry(registry)
    rotated: list[str] = []
    if x2_mode == "all":
        rotated = x2
    elif x2_mode == "one" and x2:
        rotated = [x2[end_time.date().toordinal() % len(x2)]]
    return unique_handles([*x1, *rotated]), x1, rotated


def query_for(handles: list[str]) -> str:
    authors = " OR ".join(f"from:{handle}" for handle in handles)
    return f"({authors}) -is:retweet -is:reply"


def build_query_batches(handles: list[str], max_chars: int) -> list[tuple[list[str], str]]:
    batches: list[tuple[list[str], str]] = []
    current: list[str] = []
    for handle in handles:
        candidate = [*current, handle]
        if len(query_for(candidate)) <= max_chars:
            current = candidate
            continue
        if not current:
            raise ValueError(f"handle @{handle} cannot fit within the query limit")
        batches.append((current, query_for(current)))
        current = [handle]
    if current:
        batches.append((current, query_for(current)))
    return batches


def safe_problem(body: bytes, token: str) -> str:
    decoded = body.decode("utf-8", errors="replace")[:2000].replace(token, "[redacted]")
    try:
        payload = json.loads(decoded)
    except json.JSONDecodeError:
        return decoded or "empty response"
    if isinstance(payload, dict):
        detail = payload.get("detail") or payload.get("title") or payload.get("message")
        if detail:
            return str(detail).replace(token, "[redacted]")
        errors = payload.get("errors")
        if isinstance(errors, list) and errors:
            return json.dumps(errors[:3], ensure_ascii=False).replace(token, "[redacted]")
    return json.dumps(payload, ensure_ascii=False)[:2000].replace(token, "[redacted]")


def api_get(params: dict[str, str], token: str, timeout: float) -> tuple[dict[str, Any], dict[str, str]]:
    endpoint = params.pop("_endpoint")
    url = f"{API_BASE_URL}/2/tweets/search/{endpoint}?{urlencode(params)}"
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "ai-agent-frontier-radar/1.0",
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            headers = {key.lower(): value for key, value in response.headers.items()}
    except HTTPError as error:
        body = error.read()
        code = "rate_limited" if error.code == 429 else "http_error"
        reset = error.headers.get("x-rate-limit-reset")
        suffix = f"; reset={reset}" if reset else ""
        raise XApiError(
            code,
            f"X API returned HTTP {error.code}: {safe_problem(body, token)}{suffix}",
            status=error.code,
        ) from error
    except (URLError, TimeoutError) as error:
        raise XApiError("transport_error", f"X API request failed: {error}") from error

    try:
        payload = json.loads(body)
    except json.JSONDecodeError as error:
        raise XApiError("invalid_json", "X API returned a non-JSON response") from error
    if not isinstance(payload, dict):
        raise XApiError("invalid_payload", "X API returned an unexpected JSON shape")
    return payload, headers


def fetch_batch(
    query: str,
    endpoint: str,
    start_time: datetime,
    end_time: datetime,
    token: str,
    max_pages: int,
    timeout: float,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any]]:
    posts: list[dict[str, Any]] = []
    users: dict[str, dict[str, Any]] = {}
    next_token: str | None = None
    page_count = 0
    truncated = False
    partial_errors: list[Any] = []
    last_rate_headers: dict[str, str] = {}

    while page_count < max_pages:
        params = {
            "_endpoint": endpoint,
            "query": query,
            "max_results": "100",
            "start_time": format_utc(start_time),
            "end_time": format_utc(end_time),
            "sort_order": "recency",
            "post.fields": (
                "article,article_title,conversation_id,created_at,entities,lang,note_post,text"
            ),
            "expansions": "author_id",
            "user.fields": "name,username,verified",
        }
        if next_token:
            params["next_token"] = next_token

        payload, last_rate_headers = api_get(params, token, timeout)
        page_count += 1
        data = payload.get("data", [])
        if isinstance(data, list):
            posts.extend(item for item in data if isinstance(item, dict))
        includes = payload.get("includes", {})
        included_users = includes.get("users", []) if isinstance(includes, dict) else []
        if isinstance(included_users, list):
            for user in included_users:
                if isinstance(user, dict) and user.get("id"):
                    users[str(user["id"])] = user
        errors = payload.get("errors", [])
        if isinstance(errors, list):
            partial_errors.extend(errors)

        meta = payload.get("meta", {})
        next_token = meta.get("next_token") if isinstance(meta, dict) else None
        if not next_token:
            break
        if page_count >= max_pages:
            truncated = True

    return posts, users, {
        "page_count": page_count,
        "truncated": truncated,
        "partial_errors": partial_errors,
        "rate_limit": {
            key: last_rate_headers[key]
            for key in ("x-rate-limit-limit", "x-rate-limit-remaining", "x-rate-limit-reset")
            if key in last_rate_headers
        },
    }


def normalize_posts(
    posts: Iterable[dict[str, Any]], users: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    normalized: dict[str, dict[str, Any]] = {}
    for post in posts:
        post_id = str(post.get("id", ""))
        if not post_id:
            continue
        author = users.get(str(post.get("author_id", "")), {})
        username = str(author.get("username", ""))
        canonical_url = (
            f"https://x.com/{username}/status/{post_id}"
            if username
            else f"https://x.com/i/web/status/{post_id}"
        )
        normalized[post_id] = {
            "id": post_id,
            "author": {
                "id": str(post.get("author_id", "")),
                "username": username or None,
                "name": author.get("name"),
                "verified": author.get("verified"),
            },
            "created_at": post.get("created_at"),
            "text": post.get("text", ""),
            "lang": post.get("lang"),
            "canonical_url": canonical_url,
            "conversation_id": post.get("conversation_id"),
            "entities": post.get("entities"),
            "note_post": post.get("note_post"),
            "article": post.get("article"),
            "article_title": post.get("article_title"),
        }
    return sorted(
        normalized.values(), key=lambda item: str(item.get("created_at") or ""), reverse=True
    )


def render(payload: dict[str, Any], pretty: bool) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2 if pretty else None, sort_keys=pretty))


def build_parser() -> argparse.ArgumentParser:
    default_registry = Path(__file__).resolve().parents[1] / "references" / "x-voices.md"
    parser = argparse.ArgumentParser(
        description="Fetch curated Frontier Voice posts using the official X API."
    )
    parser.add_argument("--registry", type=Path, default=default_registry)
    parser.add_argument("--handles", help="Comma-separated handles; overrides the registry")
    parser.add_argument("--x2-mode", choices=("one", "none", "all"), default="one")
    parser.add_argument("--start-time", help="Inclusive ISO-8601 timestamp; default: end minus 36h")
    parser.add_argument("--end-time", help="Exclusive ISO-8601 timestamp; default: now minus 30s")
    parser.add_argument("--hours", type=float, default=DEFAULT_HOURS)
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--dry-run", action="store_true", help="Print the query plan without network access")
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.hours <= 0:
        raise SystemExit("--hours must be greater than zero")
    if not 1 <= args.max_pages <= 10:
        raise SystemExit("--max-pages must be between 1 and 10")
    if args.timeout <= 0:
        raise SystemExit("--timeout must be greater than zero")

    now = utc_now()
    end_time = parse_utc(args.end_time) if args.end_time else now - timedelta(seconds=30)
    start_time = (
        parse_utc(args.start_time) if args.start_time else end_time - timedelta(hours=args.hours)
    )
    if start_time >= end_time:
        raise SystemExit("--start-time must be earlier than --end-time")

    handles, x1, rotated_x2 = select_handles(
        args.registry, end_time, args.handles, args.x2_mode
    )
    if not handles:
        raise SystemExit("no X handles selected")

    use_recent = start_time >= now - RECENT_HORIZON
    endpoint = "recent" if use_recent else "all"
    query_limit = 512 if use_recent else 1024
    batches = build_query_batches(handles, query_limit)
    base = {
        "schema_version": 1,
        "source": f"x_api_{endpoint}_search",
        "window": {
            "start_time": format_utc(start_time),
            "end_time": format_utc(end_time),
        },
        "coverage": {
            "requested_handles": handles,
            "x1_handles": x1,
            "rotated_x2_handles": rotated_x2,
            "query_batches": len(batches),
        },
    }

    if args.dry_run:
        render(
            {
                **base,
                "status": "planned",
                "queries": [query for _, query in batches],
                "max_pages_per_query": args.max_pages,
                "network_access": False,
            },
            args.pretty,
        )
        return 0

    token = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not token:
        render(
            {
                **base,
                "status": "degraded",
                "coverage_complete": False,
                "posts": [],
                "error": {
                    "code": "missing_credentials",
                    "message": (
                        "X_BEARER_TOKEN is not configured. Store it in the scheduler's "
                        "secret environment; never place it in the Skill, repository, or chat."
                    ),
                },
            },
            args.pretty,
        )
        return 2

    all_posts: list[dict[str, Any]] = []
    all_users: dict[str, dict[str, Any]] = {}
    batch_meta: list[dict[str, Any]] = []
    try:
        for batch_handles, query in batches:
            posts, users, meta = fetch_batch(
                query,
                endpoint,
                start_time,
                end_time,
                token,
                args.max_pages,
                args.timeout,
            )
            all_posts.extend(posts)
            all_users.update(users)
            batch_meta.append({"handles": batch_handles, **meta})
    except XApiError as error:
        render(
            {
                **base,
                "status": "degraded",
                "coverage_complete": False,
                "posts": normalize_posts(all_posts, all_users),
                "batch_meta": batch_meta,
                "error": {"code": error.code, "status": error.status, "message": str(error)},
            },
            args.pretty,
        )
        return 2

    normalized = normalize_posts(all_posts, all_users)
    truncated = any(meta["truncated"] for meta in batch_meta)
    partial_errors = [error for meta in batch_meta for error in meta["partial_errors"]]
    authors_with_posts = sorted(
        {
            str(item["author"]["username"])
            for item in normalized
            if item["author"]["username"]
        },
        key=str.casefold,
    )
    authors_folded = {author.casefold() for author in authors_with_posts}
    status = "degraded" if truncated or partial_errors else "ok"
    render(
        {
            **base,
            "status": status,
            "coverage_complete": status == "ok",
            "coverage": {
                **base["coverage"],
                "authors_with_posts": authors_with_posts,
                "handles_with_no_matching_posts": [
                    handle for handle in handles if handle.casefold() not in authors_folded
                ],
            },
            "posts": normalized,
            "batch_meta": batch_meta,
            "observed_resources": {
                "posts": len(normalized),
                "expanded_users": len(all_users),
            },
            "warning": (
                "Results hit the configured page cap; treat coverage as incomplete."
                if truncated
                else None
            ),
        },
        args.pretty,
    )
    return 2 if status == "degraded" else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        render(
            {
                "schema_version": 1,
                "status": "degraded",
                "coverage_complete": False,
                "posts": [],
                "error": {"code": "configuration_error", "message": str(error)},
            },
            True,
        )
        sys.exit(2)
