import os
import requests
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jwt.algorithms import RSAAlgorithm

security = HTTPBearer()

COGNITO_REGION = os.getenv("COGNITO_REGION", "ap-southeast-1")
COGNITO_USERPOOL_ID = os.getenv("COGNITO_USERPOOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USERPOOL_ID}/.well-known/jwks.json"

# Cache JWKS keys
_jwks = requests.get(JWKS_URL).json()

def verify_cognito_jwt(token: str):
    try:
        header = jwt.get_unverified_header(token)
        key = next(k for k in _jwks['keys'] if k['kid'] == header['kid'])
        public_key = RSAAlgorithm.from_jwk(key)
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=COGNITO_APP_CLIENT_ID
        )
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(credentials=Depends(security)):
    token = credentials.credentials
    payload = verify_cognito_jwt(token)
    return payload  # includes email, sub, and custom attributes

def admin_required(payload=Depends(get_current_user)):
    role = payload.get("custom:role") or payload.get("role")
    if role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return payload
