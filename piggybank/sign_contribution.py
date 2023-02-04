from blspy import PrivateKey, AugSchemeMPL

from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

SK = PrivateKey.from_bytes(bytes.fromhex(
    "3f1041e1a794d6cad188c9e61c90e53bab39aaec18eedd3c77cfc97fe5aa361a"))
# piggybank coin id
COIN_ID = bytes.fromhex(
    "f5921e8a28057056e312359a1623c9956350188e1c568b055cde88f4587fc144")
NEW_AMOUNT = int_to_bytes(900)

signature = AugSchemeMPL.sign(SK, std_hash(COIN_ID + NEW_AMOUNT))

print(str(signature))
