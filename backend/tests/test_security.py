import pytest
from app.core.security import hash_password, check_password, create_access_token, verify_token
from jose import jwt, JWTError
from app.config import settings
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status

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

@pytest.fixture
def credentials_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def test_verify_token_valid(credentials_exception):
    """Test verifying a valid token."""
    subject = "verifyuser"
    token = create_access_token(subject)
    verified_subject = verify_token(token, credentials_exception)
    assert verified_subject == subject

def test_verify_token_invalid_signature(credentials_exception):
    """Test verifying a token with an invalid signature."""
    subject = "invalidsiguser"
    token = create_access_token(subject)
    # Tamper with the token slightly or use a different secret
    invalid_token = token + "tamper"
    with pytest.raises(HTTPException) as excinfo:
        verify_token(invalid_token, credentials_exception)
    assert excinfo.value.status_code == 401

def test_verify_token_expired(credentials_exception):
    """Test verifying an expired token."""
    subject = "expireduser"
    # Create a token that expired 1 minute ago
    expired_delta = timedelta(minutes=-1)
    expired_token = create_access_token(subject, expires_delta=expired_delta)
    with pytest.raises(HTTPException) as excinfo:
        verify_token(expired_token, credentials_exception)
    assert excinfo.value.status_code == 401

def test_verify_token_no_sub(credentials_exception):
    """Test verifying a token with missing 'sub' claim."""
    # Manually create a token without 'sub'
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire} # Missing 'sub'
    no_sub_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        verify_token(no_sub_token, credentials_exception)
    assert excinfo.value.status_code == 401 