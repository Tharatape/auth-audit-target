from fastapi import FastAPI, HTTPException, Header, Depends

from pydantic import BaseModel

from app.users import get_user

from app.auth import create_token, decode_token

 

app = FastAPI(title="Auth Audit Target", version="0.1.0")

 

class LoginRequest(BaseModel):

    username: str

    password: str

 

class LoginResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"

 

@app.post("/auth/login", response_model=LoginResponse)

def login(body: LoginRequest):

    user = get_user(body.username)

    if not user or user["password"] != body.password:

        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user["username"], user["role"])

    return LoginResponse(access_token=token)

 

def require_auth(authorization: str = Header(None)) -> dict:

    if not authorization or not authorization.startswith("Bearer "):

        raise HTTPException(status_code=401, detail="Missing or invalid auth header")

    token = authorization.split(" ", 1)[1]

    payload = decode_token(token)

    if not payload:

        raise HTTPException(status_code=401, detail="Invalid token")

    return payload

 

@app.get("/me")

def me(user: dict = Depends(require_auth)):

    return {"user": user["sub"], "role": user["role"]}

 

@app.get("/admin/dashboard")

def admin_dashboard(user: dict = Depends(require_auth)):

    if user.get("role") != "admin":

        raise HTTPException(status_code=403, detail="Admin only")

    return {"message": "Welcome to the admin panel"}