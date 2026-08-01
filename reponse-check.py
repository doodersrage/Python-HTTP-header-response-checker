#!/usr/bin/env python3
"""Check HTTP response status codes for URLs listed in a text file."""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

import requests

DEFAULT_REPLACE = "http://virginiabeachwebdevelopment.com/"
DEFAULT_NEW_URL = "http://virginiabeachwebdevelopment.com/"
DEFAULT_PAGES_FILE = "pages.txt"
DEFAULT_RESULTS_FILE = "results.txt"
DEFAULT_TIMEOUT = 15.0
DEFAULT_WORKERS = 10


@dataclass(frozen=True)
class CheckResult:
    status_code: int
    url: str
    final_url: str = ""
    error: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check HTTP response codes for URLs listed in a file."
    )
    parser.add_argument(
        "-f",
        "--file",
        default=DEFAULT_PAGES_FILE,
        help=f"Input file with one URL per line (default: {DEFAULT_PAGES_FILE})",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=DEFAULT_RESULTS_FILE,
        help=f"Results output file (default: {DEFAULT_RESULTS_FILE})",
    )
    parser.add_argument(
        "--replace",
        default=DEFAULT_REPLACE,
        help="Domain or URL prefix to replace in each line",
    )
    parser.add_argument(
        "--new-url",
        default=DEFAULT_NEW_URL,
        help="Replacement value for --replace",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    parser.add_argument(
        "-j",
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"Concurrent request workers (default: {DEFAULT_WORKERS})",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Prompt for file paths and domain replacement values",
    )
    return parser.parse_args()


def prompt_with_default(label: str, default: str) -> str:
    value = input(f"{label} (default: {default}): ").strip()
    return value or default


def resolve_settings(args: argparse.Namespace) -> tuple[Path, Path, str, str]:
    if args.interactive:
        pages_file = Path(
            prompt_with_default("Links file", args.file)
        )
        output_file = Path(
            prompt_with_default("Results file", args.output)
        )
        replace = prompt_with_default("Domain to be replaced", args.replace)
        new_url = prompt_with_default("New domain", args.new_url)
    else:
        pages_file = Path(args.file)
        output_file = Path(args.output)
        replace = args.replace
        new_url = args.new_url

    return pages_file, output_file, replace, new_url


def load_urls(pages_file: Path, replace: str, new_url: str) -> list[str]:
    if not pages_file.is_file():
        raise FileNotFoundError(f"Links file not found: {pages_file}")

    urls: list[str] = []
    for line in pages_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        urls.append(stripped.replace(replace, new_url))

    if not urls:
        raise ValueError(f"No URLs found in {pages_file}")

    return urls


def check_url(session: requests.Session, url: str, timeout: float) -> CheckResult:
    try:
        response = session.get(url, timeout=timeout, allow_redirects=True)
    except requests.RequestException as exc:
        return CheckResult(status_code=0, url=url, error=str(exc))

    final_url = response.url if response.history else ""
    return CheckResult(
        status_code=response.status_code,
        url=url,
        final_url=final_url,
    )


def format_result(result: CheckResult) -> str:
    if result.error:
        return f"ERR\t{result.url}\t{result.error}\n"
    return f"{result.status_code}\t{result.url}\t{result.final_url}\n"


def check_urls(
    urls: list[str],
    timeout: float,
    workers: int,
) -> list[CheckResult]:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Python-HTTP-header-response-checker/2.0",
        }
    )

    results: list[CheckResult | None] = [None] * len(urls)
    worker_count = max(1, min(workers, len(urls)))

    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_to_index = {
            executor.submit(check_url, session, url, timeout): index
            for index, url in enumerate(urls)
        }
        for future in as_completed(future_to_index):
            index = future_to_index[future]
            results[index] = future.result()

    return [result for result in results if result is not None]


def write_results(output_file: Path, results: list[CheckResult]) -> None:
    output_file.write_text("".join(format_result(result) for result in results), encoding="utf-8")


def print_summary(results: list[CheckResult]) -> None:
    redirect_count = sum(1 for result in results if result.final_url)
    ok_count = sum(1 for result in results if result.status_code == 200)
    not_found_count = sum(1 for result in results if result.status_code == 404)
    error_count = sum(1 for result in results if result.error)

    print(f"Checked: {len(results)}")
    print(f"Redirects: {redirect_count}")
    print(f"200 OK: {ok_count}")
    print(f"404 not found: {not_found_count}")
    if error_count:
        print(f"Errors: {error_count}")
    print("DONE!")


def main() -> int:
    args = parse_args()

    try:
        pages_file, output_file, replace, new_url = resolve_settings(args)
        urls = load_urls(pages_file, replace, new_url)
        results = check_urls(urls, timeout=args.timeout, workers=args.workers)
        write_results(output_file, results)
        print_summary(results)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
