import pytest
from app.core.security import hash_password, check_password, create_access_token
from jose import jwt
from app.config import settings
from datetime import timedelta

def test_hash_password():
    """Test that hashing a password returns a string different from the original."""
    password = "mysecretpassword"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password
    # Basic check for bcrypt format ($2b$...)
    assert hashed.startswith('$2b$')

def test_check_password():
    """Test that checking a correct password returns True and incorrect returns False."""
    password = "anotherpassword123"
    hashed = hash_password(password)

    assert check_password(password, hashed) is True
    assert check_password("wrongpassword", hashed) is False
    assert check_password(password.upper(), hashed) is False # Case-sensitive 

def test_create_access_token():
    """Test creating a JWT access token."""
    subject = "testuser"
    token = create_access_token(subject)

    assert isinstance(token, str)

    # Decode without verification to check payload content
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_signature": False, "verify_aud": False, "verify_exp": False})
    assert payload["sub"] == subject
    assert "exp" in payload

def test_create_access_token_custom_expiry():
    """Test creating a JWT access token with custom expiry."""
    subject = 123 # Test with non-string subject
    delta = timedelta(minutes=5)
    token = create_access_token(subject, expires_delta=delta)

    assert isinstance(token, str)

    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_signature": False, "verify_aud": False, "verify_exp": False})
    assert payload["sub"] == str(subject)
    assert "exp" in payload
    # Note: Verifying the exact expiry time can be flaky in tests, 
    # so we mainly check if it exists and the subject is correct. 