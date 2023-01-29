from blspy import PrivateKey, AugSchemeMPL

from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

SK = PrivateKey.from_bytes(bytes.fromhex(
    "0d12b2310d40f604d57b21bd74da5a907821291f5fe6ca0be01e26c6d2d3a52b"))
# piggybank coin id
COIN_ID = bytes.fromhex(
    "e283591608b63d2a8381a5caeecd510e4a6a3267a4e136d7759a18553307629e")
NEW_AMOUNT = int_to_bytes(1000)

signature = AugSchemeMPL.sign(SK, std_hash(COIN_ID + NEW_AMOUNT))

print(str(signature))
