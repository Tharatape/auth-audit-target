**VULNERABILITIES**
 
Vuln #1: Default credentials (admin/admin)
-
- Severity: Critical 
- description: password was weak could crack it with rockyou.txt file
- Proof: curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}' and we can see access token
- Fix: change password according NIST rule
  
 Vuln #2: JWT key
-
- Severity: High 
- description: weak
- Proof: curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}' to get access token
    after that using JWT to decode and forge new token and use it
- Fix: get secret key in .gitignore or env and change to something more secure

 Vuln #3: JWT token no expire
-
- Severity: Critical
- description:there is no expire time in JWT token so we can  use iat time from past and it can work
- Proof: run script and curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"admin","password":"admin"}' to
    get token and decode it after that set IAT backward to one year and try to curl in http://localhost:8000/me
- Fix: set expire time for token on payload in auth.py in payload like "exp": int((now + timedelta(minutes=30)).timestamp()) so it can be check in JWT
