# Testing Guide

This document describes the test suite for the AI-Powered Phishing & Social Engineering Analyzer.

## Overview

The test suite includes comprehensive unit tests, integration tests, and fixtures to ensure the phishing analyzer works correctly. Tests mock the Google Generative AI API to avoid making actual API calls during testing.

## Test Structure

### Test Files

- **test_phishing_analyzer.py** - Main test file containing all test cases
- **conftest.py** - Pytest configuration and reusable fixtures
- **pytest.ini** - Pytest configuration settings

### Test Classes

1. **TestAPIConfiguration**
   - API key setup and configuration
   - Model availability detection
   - Model selection priority logic
   - Fallback mechanisms

2. **TestPromptGeneration**
   - Prompt formatting and structure
   - Email content inclusion
   - Empty email validation

3. **TestModelResponse**
   - Content generation calls
   - Response structure validation
   - Risk level assessment
   - Tactic detection
   - Final verdict inclusion

4. **TestPhishingDetectionPatterns**
   - High-risk keyword detection
   - Legitimate email validation
   - Urgency indicator detection
   - Authority spoofing detection

5. **TestEdgeCases**
   - Malformed response handling
   - Long email inputs
   - Special characters support
   - Multi-language support

6. **TestIntegration**
   - End-to-end analysis flow

## Running Tests

### Prerequisites

Install test dependencies:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

### Run Specific Test Class

```bash
pytest test_phishing_analyzer.py::TestAPIConfiguration -v
```

### Run Specific Test

```bash
pytest test_phishing_analyzer.py::TestAPIConfiguration::test_api_configuration_from_env -v
```

### Run Tests with Markers

```bash
# Run only API tests
pytest -m api -v

# Run all except integration tests
pytest -m "not integration" -v
```

### Run with Verbose Output

```bash
pytest -v
```

## Test Coverage

The test suite covers:

- ✅ API configuration and initialization
- ✅ Model selection and fallback logic
- ✅ Prompt generation and formatting
- ✅ API response handling
- ✅ Phishing detection pattern recognition
- ✅ Edge cases (empty input, special characters, long text)
- ✅ Multi-language support
- ✅ Error handling
- ✅ End-to-end integration flow

## Fixtures

Available pytest fixtures (in conftest.py):

- **mock_generative_model** - Mocked Google GenerativeModel
- **mock_api_key** - Mocked API key in environment
- **sample_phishing_email** - Sample phishing email for testing
- **sample_legitimate_email** - Sample legitimate email for testing
- **mock_api_response** - Mocked API response object

## Mocking Strategy

All Google Generative AI API calls are mocked using `unittest.mock` to:
- Avoid consuming API quota during testing
- Ensure tests run offline
- Allow deterministic test results
- Test error handling without actual failures

## CI/CD Integration

To integrate these tests into a CI/CD pipeline, run:

```bash
pytest --junitxml=test-results.xml --cov=. --cov-report=xml
```

## Continuous Improvement

- Add more edge case tests as new features are added
- Increase coverage for specific detection patterns
- Add performance benchmarks for large email analysis
- Add integration tests for actual API calls (in separate test suite)
