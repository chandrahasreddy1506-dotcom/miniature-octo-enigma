import os
import statistics
import time

import requests


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
ITERATIONS = int(os.getenv("PERF_ITERATIONS", "20"))
THRESHOLD_MS = float(os.getenv("PERF_THRESHOLD_MS", "800"))
TIMEOUT = float(os.getenv("PERF_TIMEOUT", "8"))

TARGETS = [
    "/",
    "/login/",
    "/register/",
]


def probe(path):
    durations = []

    for _ in range(ITERATIONS):
        start = time.perf_counter()
        response = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
        elapsed_ms = (time.perf_counter() - start) * 1000

        if response.status_code != 200:
            raise SystemExit(f"FAIL: {path} returned {response.status_code}")

        durations.append(elapsed_ms)

    p95 = statistics.quantiles(durations, n=20)[-1]
    avg = statistics.mean(durations)

    print(f"{path} -> avg={avg:.2f}ms p95={p95:.2f}ms")

    if p95 > THRESHOLD_MS:
        raise SystemExit(
            f"FAIL: {path} p95 {p95:.2f}ms exceeded threshold {THRESHOLD_MS:.2f}ms"
        )


def main():
    for target in TARGETS:
        probe(target)

    print("PASS: smoke performance checks are within threshold")


if __name__ == "__main__":
    main()
