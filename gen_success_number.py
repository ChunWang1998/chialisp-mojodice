import hashlib
import hmac

user_name = "Leo"
secret_key = "20230202"

# encoding as per other answers
byte_key = bytes(secret_key, 'UTF-8')  # key.encode() would also work in this case
message = user_name.encode()

# now use the hmac.new function and the hexdigest method
h = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

last_two_bytes= h[len(h)-2:len(h)]
#str to bytes
byte_val = bytes(last_two_bytes, 'utf-8')
#bytes to int
int_val = int.from_bytes(byte_val, "big")

# print the output
print(int_val%100)