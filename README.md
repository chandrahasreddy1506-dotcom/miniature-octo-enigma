# Automation and CI/CD

This folder contains API testing, load testing, and performance testing utilities.

## Files

- `requirements-automation.txt`: extra tools for automation checks
- `api_tests/test_web_endpoints.py`: API-level endpoint checks
- `load_tests/locustfile.py`: Locust scenario for traffic simulation
- `performance_tests/smoke_performance.py`: p95 response-time gate

## Quick Setup

1. Start app locally:
   - `python manage.py runserver`
2. Install automation dependencies:
   - `pip install -r automation/requirements-automation.txt`

## Run API tests

- `pytest automation/api_tests -q`

## Run load tests (Locust)

UI mode:
- `locust -f automation/load_tests/locustfile.py`

Headless example:
- `locust -f automation/load_tests/locustfile.py --headless --users 30 --spawn-rate 5 --run-time 2m --host http://127.0.0.1:8000`

## Run performance smoke tests

- `python automation/performance_tests/smoke_performance.py`

Tune threshold:
- `PERF_THRESHOLD_MS=1200 python automation/performance_tests/smoke_performance.py`
