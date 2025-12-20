
import jwt

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY0Nzg4MjMxLCJ0eXBlIjoiYWNjZXNzIn0._v_QVcyn6ihLjlC0-LTx9rvNXQHWU0hPt7ltFLIFBEg"
secret = "cpORgt37bB-H1bTrhllQQ4U4EQHIPFH62y2bU80-T6E" 

try:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    print("Payload:", payload)
    user_id = int(payload.get("sub"))
    print("User ID:", user_id)
except Exception as e:
    print("Error decoding:", e)
