from blspy import PrivateKey, AugSchemeMPL

from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

SK = PrivateKey.from_bytes(bytes.fromhex("0d12b2310d40f604d57b21bd74da5a907821291f5fe6ca0be01e26c6d2d3a52b"))
COIN_ID = bytes.fromhex("155e5150652a1ab6b72c41ee9b34afa4bab7904457db3f3316f06ea112394564")
NEW_AMOUNT = int_to_bytes(1000000900)

signature = AugSchemeMPL.sign(SK, std_hash(COIN_ID + NEW_AMOUNT))

print(str(signature))