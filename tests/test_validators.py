"""
Test suite for input validation system
"""
import pytest
from utils.validators import (
    EmailValidator, URLValidator, TextValidator, HotelInputValidator,
    validate_and_sanitize_input, ValidationError, ValidationSeverity
)

class TestEmailValidator:
    """Test email validation"""
    
    def test_valid_email(self):
        """Test valid email addresses"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "test+tag@example.org"
        ]
        
        for email in valid_emails:
            result = EmailValidator.validate(email)
            assert result.is_valid, f"Email {email} should be valid"
            assert result.severity == ValidationSeverity.INFO
    
    def test_invalid_email(self):
        """Test invalid email addresses"""
        invalid_emails = [
            "",
            "invalid",
            "@example.com",
            "test@",
            "test@.com",
            "test..test@example.com"
        ]
        
        for email in invalid_emails:
            result = EmailValidator.validate(email)
            assert not result.is_valid, f"Email {email} should be invalid"
            assert result.severity == ValidationSeverity.ERROR
    
    def test_email_too_long(self):
        """Test email length validation"""
        long_email = "a" * 250 + "@example.com"
        result = EmailValidator.validate(long_email)
        assert not result.is_valid
        assert "too long" in result.message

class TestURLValidator:
    """Test URL validation"""
    
    def test_valid_url(self):
        """Test valid URLs"""
        valid_urls = [
            "https://example.com",
            "http://www.example.com",
            "https://subdomain.example.com/path"
        ]
        
        for url in valid_urls:
            result = URLValidator.validate(url)
            assert result.is_valid, f"URL {url} should be valid"
    
    def test_invalid_url(self):
        """Test invalid URLs"""
        invalid_urls = [
            "",
            "not-a-url",
            "ftp://example.com",  # Unsupported scheme
            "javascript:alert(1)",  # Dangerous scheme
            "a" * 3000  # Too long
        ]
        
        for url in invalid_urls:
            result = URLValidator.validate(url)
            assert not result.is_valid, f"URL {url} should be invalid"

class TestTextValidator:
    """Test text validation"""
    
    def test_valid_text(self):
        """Test valid text"""
        result = TextValidator.validate("Hello world", "test_text")
        assert result.is_valid
    
    def test_text_too_long(self):
        """Test text length validation"""
        long_text = "a" * 2000
        result = TextValidator.validate(long_text, "test_text", max_length=1000)
        assert not result.is_valid
        assert "too long" in result.message
    
    def test_dangerous_content(self):
        """Test dangerous content detection"""
        dangerous_texts = [
            "<script>alert('xss')</script>",
            "javascript:alert(1)",
            "onclick=alert(1)"
        ]
        
        for text in dangerous_texts:
            result = TextValidator.validate(text, "test_text")
            assert not result.is_valid, f"Text {text} should be invalid"

class TestHotelInputValidator:
    """Test hotel input validation"""
    
    def test_valid_analysis_request(self):
        """Test valid analysis request"""
        data = {
            "email": "test@example.com",
            "hotel_url": "https://example.com",
            "instagram_url": "https://instagram.com/hotel"
        }
        
        is_valid, results = HotelInputValidator.validate_analysis_request(data)
        assert is_valid
        assert all(result.is_valid for result in results)
    
    def test_invalid_analysis_request(self):
        """Test invalid analysis request"""
        data = {
            "email": "invalid-email",
            "hotel_url": "not-a-url"
        }
        
        is_valid, results = HotelInputValidator.validate_analysis_request(data)
        assert not is_valid
        assert any(not result.is_valid for result in results)
    
    def test_missing_urls(self):
        """Test request with no URLs"""
        data = {
            "email": "test@example.com"
        }
        
        is_valid, results = HotelInputValidator.validate_analysis_request(data)
        assert not is_valid
        assert any("Either hotel_url or instagram_url must be provided" in result.message for result in results)

class TestValidateAndSanitizeInput:
    """Test main validation function"""
    
    def test_analysis_input_validation(self):
        """Test analysis input validation"""
        data = {
            "email": "test@example.com",
            "hotel_url": "https://example.com"
        }
        
        is_valid, sanitized_data, results = validate_and_sanitize_input(data, "analysis")
        assert is_valid
        assert sanitized_data["email"] == "test@example.com"
        assert sanitized_data["hotel_url"] == "https://example.com"
    
    def test_onboarding_input_validation(self):
        """Test onboarding input validation"""
        data = {
            "hotel_url": "https://example.com",
            "user_notes": "Test notes"
        }
        
        is_valid, sanitized_data, results = validate_and_sanitize_input(data, "onboarding")
        assert is_valid
        assert sanitized_data["hotel_url"] == "https://example.com"
    
    def test_campaign_input_validation(self):
        """Test campaign input validation"""
        data = {
            "name": "Test Campaign",
            "budget": 1000,
            "target_roas": 400
        }
        
        is_valid, sanitized_data, results = validate_and_sanitize_input(data, "campaign")
        assert is_valid
        assert sanitized_data["name"] == "Test Campaign"
    
    def test_invalid_input_type(self):
        """Test invalid input type"""
        data = {"test": "value"}
        
        is_valid, sanitized_data, results = validate_and_sanitize_input(data, "invalid_type")
        assert not is_valid
        assert any("Unknown input type" in result.message for result in results)
