from blspy import PrivateKey, AugSchemeMPL

from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

SK = PrivateKey.from_bytes(bytes.fromhex(
    "3f1041e1a794d6cad188c9e61c90e53bab39aaec18eedd3c77cfc97fe5aa361a"))
# piggybank coin id
COIN_ID = bytes.fromhex(
    "197b53fd936b7f25283fd3127d77914aad5b55f16b6a3fb0e3b0cdf7ff3fbf60")
NEW_AMOUNT = int_to_bytes(900)

signature = AugSchemeMPL.sign(SK, std_hash(COIN_ID + NEW_AMOUNT))

print(str(signature))
