# HLTV Scraper API - Unit Tests

## Overview

This directory contains both **unit tests** and **integration tests** for the HLTV Scraper API.

## Test Types

### 🟢 Unit Tests (Fast)
**File:** `test_routes.py`
- **Purpose**: Test application logic in isolation
- **Mocking**: All external dependencies (Scrapy, HLTV.org, file system)
- **Speed**: Very fast (~0.03s)
- **Network**: No network calls
- **Reliability**: Always consistent results

### 🟡 Integration Tests (Slow) 
**File:** `test_integration_real.py`
- **Purpose**: Test real data fetching from HLTV.org
- **Mocking**: No mocking - real Scrapy spiders
- **Speed**: Slow (10-30s per test)
- **Network**: Real HTTP requests to HLTV.org
- **Reliability**: Depends on HLTV.org availability

## Running Tests

### Quick Commands
```bash
# Fast unit tests only (recommended for development)
make test-unit

# All tests (unit + integration)  
make test

# Only integration tests (slow, real HLTV data)
make test-integration

# Only fast tests (exclude slow ones)
make test-fast

# Only slow tests  
make test-slow

# With coverage report
make test-cov
```

### Detailed Commands
```bash
# Unit tests with mocks (fast)
pytest tests/test_routes.py -v

# Integration tests (slow, real data)
pytest tests/test_integration_real.py -v

# Skip slow tests
pytest -m "not slow" tests/ -v

# Only slow tests
pytest -m "slow" tests/ -v

# Specific test
pytest tests/test_routes.py::TestRoutesEndpoints::test_player_search_success -v
```

## When to Use Each Type

### 🚀 Development & CI/CD
**Use unit tests** (`make test-unit`)
- Fast feedback during development
- Reliable in CI/CD pipelines  
- Don't depend on external services
- Test application logic and error handling

### 🔍 QA & Staging  
**Use integration tests** (`make test-integration`)
- Verify real data fetching works
- Test against live HLTV.org
- Catch parsing errors with real HTML
- Validate end-to-end functionality

## Test Comparison

| Aspect | Unit Tests | Integration Tests |
|--------|------------|-------------------|
| **Speed** | ~0.03s | ~30s |
| **Reliability** | 100% | Depends on HLTV.org |
| **Network** | None | Real HTTP calls |
| **Data** | Mock/Fake | Real from HLTV |
| **Purpose** | Logic testing | E2E validation |
| **CI/CD** | ✅ Always run | ⚠️ Optional/Nightly |

## Current Status

### ✅ Unit Tests (8/8 passing)
- All route endpoints tested with mocks
- 79% code coverage
- Fast and reliable

### 🟡 Integration Tests  
- Created but need HLTV.org to be available
- Test real spider execution
- Verify actual data parsing

## Answer to Your Question

**"Does it really test data fetching from HLTV?"**

- ❌ **Unit tests (`test_routes.py`)**: NO - they use mocks
- ✅ **Integration tests (`test_integration_real.py`)**: YES - they fetch real data

For **development**, use unit tests. For **validation**, run integration tests occasionally.
