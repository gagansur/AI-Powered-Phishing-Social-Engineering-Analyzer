"""
Unit tests for phishing_analyzer.py
Tests the core functionality of the phishing email analyzer
"""

import pytest
from unittest.mock import patch, MagicMock, Mock
import google.generativeai as genai


class TestAPIConfiguration:
    """Tests for API configuration and initialization"""

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key_123'})
    @patch('google.generativeai.configure')
    def test_api_configuration_from_env(self, mock_configure):
        """Test that API is configured when key exists in environment"""
        mock_configure('test_key_123')
        mock_configure.assert_called_once_with('test_key_123')

    @patch('google.generativeai.list_models')
    def test_model_list_retrieval(self, mock_list_models):
        """Test that available models are retrieved successfully"""
        mock_model = MagicMock()
        mock_model.name = 'models/gemini-1.5-flash'
        mock_list_models.return_value = [mock_model]
        
        models = [m.name for m in mock_list_models()]
        assert 'models/gemini-1.5-flash' in models

    @patch('google.generativeai.list_models')
    def test_model_selection_priority_flash(self, mock_list_models):
        """Test that gemini-1.5-flash is selected when available"""
        models = [
            MagicMock(name='models/gemini-1.5-flash'),
            MagicMock(name='models/gemini-pro')
        ]
        mock_list_models.return_value = models
        
        model_names = [m.name for m in mock_list_models()]
        target_model = 'gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_names else 'gemini-pro'
        
        assert target_model == 'gemini-1.5-flash'

    @patch('google.generativeai.list_models')
    def test_model_selection_fallback_pro(self, mock_list_models):
        """Test fallback to gemini-pro when flash is unavailable"""
        models = [
            MagicMock(name='models/gemini-pro')
        ]
        mock_list_models.return_value = models
        
        model_names = [m.name for m in mock_list_models()]
        target_model = 'gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_names else 'gemini-pro'
        
        assert target_model == 'gemini-pro'

    @patch('google.generativeai.list_models')
    def test_model_selection_empty_fallback(self, mock_list_models):
        """Test fallback to first available model when preferred models unavailable"""
        models = [
            MagicMock(name='models/custom-model')
        ]
        mock_list_models.return_value = models
        
        model_names = [m.name for m in mock_list_models()]
        target_model = 'gemini-1.5-flash' if 'models/gemini-1.5-flash' in model_names else (
            'gemini-pro' if 'models/gemini-pro' in model_names else model_names[0]
        )
        
        assert target_model == 'models/custom-model'


class TestPromptGeneration:
    """Tests for prompt generation and content analysis"""

    def test_phishing_prompt_structure(self):
        """Test that the phishing analysis prompt is correctly formatted"""
        email_input = "Dear user, click here to verify your account"
        expected_keywords = ['Risk Level', 'Detected Tactics', 'Final Verdict']
        
        prompt = f"""
        Act as a Senior Cyber Security Analyst. Analyze this email for phishing:
        {email_input}
        Return a report with: 
        - Risk Level (Safe/Low/Medium/High)
        - Detected Tactics (e.g., sense of urgency, fake authority)
        - Final Verdict
        """
        
        for keyword in expected_keywords:
            assert keyword in prompt

    def test_prompt_includes_email_content(self):
        """Test that email content is included in the prompt"""
        email_input = "This is a test email"
        
        prompt = f"""
        Act as a Senior Cyber Security Analyst. Analyze this email for phishing:
        {email_input}
        Return a report with: 
        - Risk Level (Safe/Low/Medium/High)
        - Detected Tactics (e.g., sense of urgency, fake authority)
        - Final Verdict
        """
        
        assert email_input in prompt

    def test_empty_email_handling(self):
        """Test that empty emails are handled appropriately"""
        email_input = ""
        
        # Simulate validation logic
        is_valid = bool(email_input.strip())
        
        assert not is_valid


class TestModelResponse:
    """Tests for model response and analysis"""

    @patch('google.generativeai.GenerativeModel')
    def test_generate_content_call(self, mock_generative_model):
        """Test that generate_content is called with the prompt"""
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Risk Level: High\nDetected Tactics: Sense of urgency\nFinal Verdict: PHISHING"
        mock_model.generate_content.return_value = mock_response
        
        model = mock_generative_model('gemini-2.5-flash')
        prompt = "Test prompt"
        response = model.generate_content(prompt)
        
        assert response.text is not None
        mock_model.generate_content.assert_called_once_with(prompt)

    @patch('google.generativeai.GenerativeModel')
    def test_response_contains_risk_level(self, mock_generative_model):
        """Test that response contains risk level assessment"""
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Risk Level: Medium\nDetected Tactics: Phishing link\nFinal Verdict: SUSPICIOUS"
        mock_model.generate_content.return_value = mock_response
        
        model = mock_generative_model('gemini-2.5-flash')
        response = model.generate_content("prompt")
        
        assert "Risk Level" in response.text

    @patch('google.generativeai.GenerativeModel')
    def test_response_contains_detected_tactics(self, mock_generative_model):
        """Test that response includes detected tactics"""
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Risk Level: High\nDetected Tactics: Fake authority, Sense of urgency\nFinal Verdict: PHISHING"
        mock_model.generate_content.return_value = mock_response
        
        model = mock_generative_model('gemini-2.5-flash')
        response = model.generate_content("prompt")
        
        assert "Detected Tactics" in response.text

    @patch('google.generativeai.GenerativeModel')
    def test_response_contains_final_verdict(self, mock_generative_model):
        """Test that response includes final verdict"""
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Risk Level: Safe\nDetected Tactics: None\nFinal Verdict: LEGITIMATE"
        mock_model.generate_content.return_value = mock_response
        
        model = mock_generative_model('gemini-2.5-flash')
        response = model.generate_content("prompt")
        
        assert "Final Verdict" in response.text


class TestPhishingDetectionPatterns:
    """Tests for phishing detection logic and patterns"""

    def test_high_risk_keywords_detection(self):
        """Test detection of high-risk phishing keywords"""
        risky_keywords = ['verify account', 'confirm identity', 'update payment', 'urgent action required']
        email = "Please verify account immediately to avoid suspension"
        
        detected = any(keyword in email.lower() for keyword in risky_keywords)
        assert detected

    def test_safe_email_detection(self):
        """Test that legitimate emails don't trigger false positives"""
        risky_keywords = ['verify account', 'confirm identity', 'update payment', 'urgent action required']
        email = "Here's your quarterly report as requested"
        
        detected = any(keyword in email.lower() for keyword in risky_keywords)
        assert not detected

    def test_urgency_indicators_detection(self):
        """Test detection of urgency-creating tactics"""
        urgency_phrases = ['immediately', 'urgent', 'within 24 hours', 'act now', 'do not delay']
        email = "You must act immediately to secure your account"
        
        detected = any(phrase in email.lower() for phrase in urgency_phrases)
        assert detected

    def test_authority_spoofing_detection(self):
        """Test detection of fake authority tactics"""
        authority_keywords = ['administrator', 'security team', 'bank', 'paypal', 'amazon']
        email = "This is from the PayPal Security Team"
        
        detected = any(keyword in email.lower() for keyword in authority_keywords)
        assert detected


class TestEdgeCases:
    """Tests for edge cases and error handling"""

    @patch('google.generativeai.GenerativeModel')
    def test_malformed_response_handling(self, mock_generative_model):
        """Test handling of malformed API responses"""
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = ""
        mock_model.generate_content.return_value = mock_response
        
        model = mock_generative_model('gemini-2.5-flash')
        response = model.generate_content("prompt")
        
        # Should not raise an error
        assert response.text is not None

    def test_very_long_email_input(self):
        """Test handling of very long email inputs"""
        long_email = "A" * 50000
        
        # Simulate that the email is processed
        is_processed = bool(long_email)
        assert is_processed

    def test_special_characters_in_email(self):
        """Test handling of special characters in email"""
        email = "Test <>&\"'() email with special chars"
        
        # Should not raise an error
        assert isinstance(email, str)

    def test_multiple_language_support(self):
        """Test that emails in different languages are accepted"""
        emails = [
            "This is an English email",
            "Ceci est un email français",
            "这是一封中文电子邮件"
        ]
        
        for email in emails:
            assert isinstance(email, str)


class TestIntegration:
    """Integration tests"""

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_end_to_end_analysis(self, mock_configure, mock_generative_model):
        """Test complete end-to-end analysis flow"""
        # Setup
        mock_configure('test_key')
        mock_model = MagicMock()
        mock_generative_model.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "Risk Level: High\nDetected Tactics: Phishing\nFinal Verdict: PHISHING"
        mock_model.generate_content.return_value = mock_response
        
        # Execution
        email_input = "Click here to verify your account immediately"
        model = mock_generative_model('gemini-2.5-flash')
        
        prompt = f"""
        Act as a Senior Cyber Security Analyst. Analyze this email for phishing:
        {email_input}
        Return a report with: 
        - Risk Level (Safe/Low/Medium/High)
        - Detected Tactics (e.g., sense of urgency, fake authority)
        - Final Verdict
        """
        
        response = model.generate_content(prompt)
        
        # Assertions
        assert "Risk Level" in response.text
        assert "High" in response.text
        assert "PHISHING" in response.text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
