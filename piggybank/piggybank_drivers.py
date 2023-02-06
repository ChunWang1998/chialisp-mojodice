from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.blockchain_format.program import Program
from chia.types.condition_opcodes import ConditionOpcode
from chia.util.ints import uint64
from chia.util.hash import std_hash

from clvm.casts import int_to_bytes

from cdv.util.load_clvm import load_clvm

PIGGYBANK_MOD = load_clvm("piggybank.clsp","piggybank")

# Create a piggybank
def create_piggybank_puzzle( cash_out_puzhash,probability:uint64, game_limit:uint64):
    return PIGGYBANK_MOD.curry( cash_out_puzhash,probability, game_limit)

# Generate a solution to contribute to a piggybank
def solution_for_piggybank(success_number, pb_coin, withdraw_amount,vault_after_withdraw_amount,vault_after_deposit_amount):
    return Program.to([success_number, pb_coin.amount, pb_coin.puzzle_hash, withdraw_amount,vault_after_withdraw_amount,vault_after_deposit_amount])

# Return the condition to assert the announcement
def piggybank_announcement_assertion(pb_coin, contribution_amount):#for CREATE_COIN_ANNOUNCEMENT
    return [ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT, std_hash(pb_coin.name() + int_to_bytes((pb_coin.amount + contribution_amount)))]
