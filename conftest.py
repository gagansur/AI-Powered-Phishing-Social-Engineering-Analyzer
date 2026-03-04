"""
Pytest fixtures and configuration for phishing analyzer tests
"""

import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_generative_model():
    """Fixture for mocked Google Generative Model"""
    with patch('google.generativeai.GenerativeModel') as mock:
        yield mock


@pytest.fixture
def mock_api_key():
    """Fixture for mocked API key configuration"""
    with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key_123'}):
        yield 'test_key_123'


@pytest.fixture
def sample_phishing_email():
    """Sample phishing email for testing"""
    return """
    Dear Valued Customer,
    
    Your account has been compromised. Click here immediately to verify your identity.
    
    Best regards,
    PayPal Security Team
    """


@pytest.fixture
def sample_legitimate_email():
    """Sample legitimate email for testing"""
    return """
    Hi John,
    
    Here's the quarterly report you requested. Please review and let me know if you have any questions.
    
    Best regards,
    Sarah
    """


@pytest.fixture
def mock_api_response():
    """Fixture for mocked API response"""
    mock_response = MagicMock()
    mock_response.text = "Risk Level: High\nDetected Tactics: Phishing\nFinal Verdict: PHISHING"
    return mock_response
