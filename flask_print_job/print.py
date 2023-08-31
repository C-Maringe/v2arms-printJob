import jwt
from datetime import datetime, timedelta
from django.utils import timezone

encoded_jwt = jwt.encode({"exp": datetime.now(
    tz=timezone.utc) + timedelta(minutes=100000000)}, "R187966Q", algorithm="HS256")
decode_jwt = jwt.decode(encoded_jwt, "R187966Q", algorithms=["HS256"])
print(encoded_jwt)
print(decode_jwt)
