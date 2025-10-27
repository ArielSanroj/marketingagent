"""
Input Validation System
Comprehensive validation for all user inputs with security and data integrity checks
"""
import re
import urllib.parse
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class ValidationSeverity(Enum):
    """Validation severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    """Result of validation check"""
    is_valid: bool
    message: str
    severity: ValidationSeverity
    field: str
    value: Any

class BaseValidator:
    """Base validator class with common validation methods"""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format"""
        if not email or not isinstance(email, str):
            return False
        
        # RFC 5322 compliant email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email.strip()))
    
    @staticmethod
    def is_valid_url(url: str, allowed_schemes: List[str] = None) -> bool:
        """Validate URL format and scheme"""
        if not url or not isinstance(url, str):
            return False
        
        if allowed_schemes is None:
            allowed_schemes = ['http', 'https']
        
        try:
            parsed = urllib.parse.urlparse(url.strip())
            return (
                parsed.scheme in allowed_schemes and
                parsed.netloc and
                len(parsed.netloc) <= 253  # Domain length limit
            )
        except Exception:
            return False
    
    @staticmethod
    def is_safe_string(text: str, max_length: int = 1000) -> bool:
        """Check if string is safe (no dangerous characters)"""
        if not text or not isinstance(text, str):
            return False
        
        if len(text) > max_length:
            return False
        
        # Check for dangerous patterns
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',  # JavaScript URLs
            r'data:text/html',  # Data URLs
            r'vbscript:',  # VBScript
            r'on\w+\s*=',  # Event handlers
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if re.search(pattern, text_lower):
                return False
        
        return True
    
    @staticmethod
    def sanitize_string(text: str) -> str:
        """Sanitize string by removing dangerous content"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove dangerous characters
        text = re.sub(r'[<>"\']', '', text)
        
        # Limit length
        return text[:1000]

class EmailValidator(BaseValidator):
    """Email-specific validation"""
    
    @classmethod
    def validate(cls, email: str) -> ValidationResult:
        """Validate email input"""
        if not email:
            return ValidationResult(
                is_valid=False,
                message="Email is required",
                severity=ValidationSeverity.ERROR,
                field="email",
                value=email
            )
        
        if not isinstance(email, str):
            return ValidationResult(
                is_valid=False,
                message="Email must be a string",
                severity=ValidationSeverity.ERROR,
                field="email",
                value=email
            )
        
        email = email.strip()
        
        if len(email) > 254:  # RFC 5321 limit
            return ValidationResult(
                is_valid=False,
                message="Email is too long",
                severity=ValidationSeverity.ERROR,
                field="email",
                value=email
            )
        
        if not cls.is_valid_email(email):
            return ValidationResult(
                is_valid=False,
                message="Invalid email format",
                severity=ValidationSeverity.ERROR,
                field="email",
                value=email
            )
        
        return ValidationResult(
            is_valid=True,
            message="Valid email",
            severity=ValidationSeverity.INFO,
            field="email",
            value=email
        )

class URLValidator(BaseValidator):
    """URL-specific validation"""
    
    @classmethod
    def validate(cls, url: str, field_name: str = "url") -> ValidationResult:
        """Validate URL input"""
        if not url:
            return ValidationResult(
                is_valid=False,
                message=f"{field_name} is required",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=url
            )
        
        if not isinstance(url, str):
            return ValidationResult(
                is_valid=False,
                message=f"{field_name} must be a string",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=url
            )
        
        url = url.strip()
        
        if len(url) > 2048:  # URL length limit
            return ValidationResult(
                is_valid=False,
                message=f"{field_name} is too long",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=url
            )
        
        if not cls.is_valid_url(url):
            return ValidationResult(
                is_valid=False,
                message=f"Invalid {field_name} format",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=url
            )
        
        return ValidationResult(
            is_valid=True,
            message=f"Valid {field_name}",
            severity=ValidationSeverity.INFO,
            field=field_name,
            value=url
        )

class TextValidator(BaseValidator):
    """Text input validation"""
    
    @classmethod
    def validate(cls, text: str, field_name: str = "text", 
                max_length: int = 1000, required: bool = True) -> ValidationResult:
        """Validate text input"""
        if not text and required:
            return ValidationResult(
                is_valid=False,
                message=f"{field_name} is required",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=text
            )
        
        if not text and not required:
            return ValidationResult(
                is_valid=True,
                message=f"{field_name} is optional",
                severity=ValidationSeverity.INFO,
                field=field_name,
                value=text
            )
        
        if not isinstance(text, str):
            return ValidationResult(
                is_valid=False,
                message=f"{field_name} must be a string",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=text
            )
        
        if len(text) > max_length:
            return ValidationResult(
                is_valid=False,
                message=f"{field_name} is too long (max {max_length} characters)",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=text
            )
        
        if not cls.is_safe_string(text, max_length):
            return ValidationResult(
                is_valid=False,
                message=f"{field_name} contains potentially dangerous content",
                severity=ValidationSeverity.ERROR,
                field=field_name,
                value=text
            )
        
        return ValidationResult(
            is_valid=True,
            message=f"Valid {field_name}",
            severity=ValidationSeverity.INFO,
            field=field_name,
            value=text
        )

class HotelInputValidator:
    """Comprehensive validator for hotel marketing system inputs"""
    
    @staticmethod
    def validate_analysis_request(data: Dict[str, Any]) -> Tuple[bool, List[ValidationResult]]:
        """Validate hotel analysis request"""
        results = []
        is_valid = True
        
        # Validate email
        email_result = EmailValidator.validate(data.get('email', ''))
        results.append(email_result)
        if not email_result.is_valid:
            is_valid = False
        
        # Validate hotel URL
        hotel_url = data.get('hotel_url', '')
        if hotel_url:
            hotel_url_result = URLValidator.validate(hotel_url, 'hotel_url')
            results.append(hotel_url_result)
            if not hotel_url_result.is_valid:
                is_valid = False
        
        # Validate Instagram URL
        instagram_url = data.get('instagram_url', '')
        if instagram_url:
            instagram_url_result = URLValidator.validate(instagram_url, 'instagram_url')
            # Check if it's actually an Instagram URL
            if instagram_url_result.is_valid and 'instagram.com' not in instagram_url.lower():
                instagram_url_result = ValidationResult(
                    is_valid=False,
                    message="Instagram URL must be from instagram.com",
                    severity=ValidationSeverity.ERROR,
                    field="instagram_url",
                    value=instagram_url
                )
            results.append(instagram_url_result)
            if not instagram_url_result.is_valid:
                is_valid = False
        
        # At least one URL must be provided
        if not hotel_url and not instagram_url:
            results.append(ValidationResult(
                is_valid=False,
                message="Either hotel_url or instagram_url must be provided",
                severity=ValidationSeverity.ERROR,
                field="urls",
                value=""
            ))
            is_valid = False
        
        return is_valid, results
    
    @staticmethod
    def validate_onboarding_input(data: Dict[str, Any]) -> Tuple[bool, List[ValidationResult]]:
        """Validate onboarding input"""
        results = []
        is_valid = True
        
        # Validate hotel URL (required)
        hotel_url = data.get('hotel_url', '')
        hotel_url_result = URLValidator.validate(hotel_url, 'hotel_url')
        results.append(hotel_url_result)
        if not hotel_url_result.is_valid:
            is_valid = False
        
        # Validate Instagram URL (optional)
        instagram_url = data.get('instagram_url', '')
        if instagram_url:
            instagram_url_result = URLValidator.validate(instagram_url, 'instagram_url')
            if instagram_url_result.is_valid and 'instagram.com' not in instagram_url.lower():
                instagram_url_result = ValidationResult(
                    is_valid=False,
                    message="Instagram URL must be from instagram.com",
                    severity=ValidationSeverity.ERROR,
                    field="instagram_url",
                    value=instagram_url
                )
            results.append(instagram_url_result)
            if not instagram_url_result.is_valid:
                is_valid = False
        
        # Validate user notes (optional)
        user_notes = data.get('user_notes', '')
        if user_notes:
            notes_result = TextValidator.validate(user_notes, 'user_notes', max_length=2000, required=False)
            results.append(notes_result)
            if not notes_result.is_valid:
                is_valid = False
        
        return is_valid, results
    
    @staticmethod
    def validate_campaign_data(data: Dict[str, Any]) -> Tuple[bool, List[ValidationResult]]:
        """Validate campaign data"""
        results = []
        is_valid = True
        
        # Validate campaign name
        campaign_name = data.get('name', '')
        name_result = TextValidator.validate(campaign_name, 'campaign_name', max_length=100, required=True)
        results.append(name_result)
        if not name_result.is_valid:
            is_valid = False
        
        # Validate budget
        budget = data.get('budget', 0)
        if not isinstance(budget, (int, float)) or budget < 0 or budget > 100000:
            results.append(ValidationResult(
                is_valid=False,
                message="Budget must be a number between 0 and 100,000",
                severity=ValidationSeverity.ERROR,
                field="budget",
                value=budget
            ))
            is_valid = False
        
        # Validate target ROAS
        target_roas = data.get('target_roas', 400)
        if not isinstance(target_roas, (int, float)) or target_roas < 100 or target_roas > 1000:
            results.append(ValidationResult(
                is_valid=False,
                message="Target ROAS must be between 100 and 1000",
                severity=ValidationSeverity.ERROR,
                field="target_roas",
                value=target_roas
            ))
            is_valid = False
        
        return is_valid, results

def validate_and_sanitize_input(data: Dict[str, Any], input_type: str = "analysis") -> Tuple[bool, Dict[str, Any], List[ValidationResult]]:
    """
    Validate and sanitize input data
    
    Args:
        data: Input data dictionary
        input_type: Type of input ('analysis', 'onboarding', 'campaign')
    
    Returns:
        Tuple of (is_valid, sanitized_data, validation_results)
    """
    sanitized_data = {}
    validation_results = []
    is_valid = True
    
    if input_type == "analysis":
        is_valid, validation_results = HotelInputValidator.validate_analysis_request(data)
    elif input_type == "onboarding":
        is_valid, validation_results = HotelInputValidator.validate_onboarding_input(data)
    elif input_type == "campaign":
        is_valid, validation_results = HotelInputValidator.validate_campaign_data(data)
    else:
        validation_results.append(ValidationResult(
            is_valid=False,
            message=f"Unknown input type: {input_type}",
            severity=ValidationSeverity.ERROR,
            field="input_type",
            value=input_type
        ))
        is_valid = False
    
    # Sanitize valid data
    if is_valid:
        for key, value in data.items():
            if isinstance(value, str):
                sanitized_data[key] = BaseValidator.sanitize_string(value)
            else:
                sanitized_data[key] = value
    
    return is_valid, sanitized_data, validation_results
