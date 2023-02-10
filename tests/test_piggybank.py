from typing import Dict, List, Optional

import pytest
import pytest_asyncio
import hashlib
import hmac
from chia.types.blockchain_format.coin import Coin
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64
from datetime import datetime

from piggybank.piggybank_drivers import (
    create_piggybank_puzzle,
    solution_for_piggybank,
    # piggybank_announcement_assertion,
)
from cdv.test import CoinWrapper
from cdv.test import setup as setup_test

PROBABILITY = 50
GAME_LIMIT = 10000000
VAULT_BALANCE = 100
WITHDRAW_MULTIPLIER = 2


def gen_success_number(user_name, secret_key):
    # encoding as per other answers
    byte_key = bytes(secret_key, "UTF-8")  # key.encode() would also work in this case
    message = user_name.encode()

    # now use the hmac.new function and the hexdigest method
    h = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

    last_two_bytes = h[len(h) - 2 : len(h)]
    # str to bytes
    byte_val = bytes(last_two_bytes, "utf-8")
    # bytes to int
    int_val = int.from_bytes(byte_val, "big")

    # print the output
    return int_val % 100


class TestStandardTransaction:
    @pytest_asyncio.fixture(scope="function")
    async def setup(self):
        network, alice, bob = await setup_test()
        await network.farm_block()
        yield network, alice, bob

    async def make_and_spend_piggybank(
        self,
        network,
        alice,
        bob,
        contribution_amount,
        success_number,
        withdraw_amount,
        vault_after_withdraw_amount,
        vault_after_deposit_amount,
    ): 
        # Get our alice wallet some money
        await network.farm_block(farmer=alice)  

        # This will use one mojo to create our piggybank on the blockchain.
        piggybank_coin = await alice.launch_smart_coin(
            create_piggybank_puzzle(bob.puzzle_hash, PROBABILITY, GAME_LIMIT)
        )  # 創建存錢罐,存滿會打到bob.puzzle_hash

        contribution_coin = await alice.choose_coin(contribution_amount) 

        # This is the spend of the piggy bank coin.  We use the driver code to create the solution.
        piggybank_spend = await alice.spend_coin(
            piggybank_coin,
            pushtx=False,
            # solution_for_piggybank(success_number,pb_coin, withdraw_amount,vault_after_withdraw_amount,vault_after_deposit_amount):
            args=solution_for_piggybank(
                success_number,
                piggybank_coin.coin,
                withdraw_amount,
                vault_after_withdraw_amount,
                vault_after_deposit_amount,
            ),
        )

        contribution_spend = await alice.spend_coin(  
            contribution_coin,
            pushtx=False,
        )

        # Aggregate them to make sure they are spent together
        combined_spend = SpendBundle.aggregate([contribution_spend, piggybank_spend]) 

        result = await network.push_tx(combined_spend)
        return result

    @pytest.mark.asyncio
    async def test_piggybank_withdraw(self, setup):
        network, alice, bob = setup
        try:
            contribution_amount = 30
            success_number = 56  # larger then 50, so withdraw
            withdraw_amount = contribution_amount * WITHDRAW_MULTIPLIER
            vault_after_withdraw_amount = VAULT_BALANCE + contribution_amount - withdraw_amount
            vault_after_deposit_amount = VAULT_BALANCE + contribution_amount
            result = await self.make_and_spend_piggybank(
                network,
                alice,
                bob,
                contribution_amount,
                success_number,
                withdraw_amount,
                vault_after_withdraw_amount,
                vault_after_deposit_amount,
            )
            assert "error" not in result  # 不應該有err

            filtered_result = list(
                filter(
                    lambda addition: (addition.amount == vault_after_withdraw_amount)
                    and (
                        addition.puzzle_hash
                        == create_piggybank_puzzle(bob.puzzle_hash, PROBABILITY, GAME_LIMIT).get_tree_hash()
                    ),
                    result["additions"],
                )
            )
            assert len(filtered_result) == 1
        finally:
            await network.close()

    @pytest.mark.asyncio
    async def test_piggybank_deposit(self, setup):
        network, alice, bob = setup
        try:
            contribution_amount = 30
            success_number = 46  # smaller then 50, so deposit
            withdraw_amount = contribution_amount * WITHDRAW_MULTIPLIER
            vault_after_withdraw_amount = VAULT_BALANCE + contribution_amount - withdraw_amount
            vault_after_deposit_amount = VAULT_BALANCE + contribution_amount
            result = await self.make_and_spend_piggybank(
                network,
                alice,
                bob,
                contribution_amount,
                success_number,
                withdraw_amount,
                vault_after_withdraw_amount,
                vault_after_deposit_amount,
            )

            assert "error" not in result

            filtered_result = list(
                filter(
                    lambda addition: (addition.amount == vault_after_deposit_amount)
                    and (
                        addition.puzzle_hash
                        == create_piggybank_puzzle(bob.puzzle_hash, PROBABILITY, GAME_LIMIT).get_tree_hash()
                    ),
                    result["additions"],
                )
            )
            assert len(filtered_result) == 1
        finally:
            await network.close()

    @pytest.mark.asyncio
    async def test_piggybank_secret_number(self, setup):
        network, alice, bob = setup
        try:
            user_name = "Leo"
            # secret_key =  # "20230202"
            secret_key = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            contribution_amount = 30
            success_number = gen_success_number(user_name, secret_key)
            withdraw_amount = contribution_amount * WITHDRAW_MULTIPLIER
            vault_after_withdraw_amount = VAULT_BALANCE + contribution_amount - withdraw_amount
            vault_after_deposit_amount = VAULT_BALANCE + contribution_amount

            result = await self.make_and_spend_piggybank(
                network,
                alice,
                bob,
                contribution_amount,
                success_number,
                withdraw_amount,
                vault_after_withdraw_amount,
                vault_after_deposit_amount,
            )

            assert "error" not in result

            if success_number > PROBABILITY:
                filtered_result = list(
                    filter(
                        lambda addition: (addition.amount == vault_after_withdraw_amount)
                        and (
                            addition.puzzle_hash
                            == create_piggybank_puzzle(bob.puzzle_hash, PROBABILITY, GAME_LIMIT).get_tree_hash()
                        ),
                        result["additions"],
                    )
                )
                assert len(filtered_result) == 1
            else:
                filtered_result = list(
                    filter(
                        lambda addition: (addition.amount == vault_after_deposit_amount)
                        and (
                            addition.puzzle_hash
                            == create_piggybank_puzzle(bob.puzzle_hash, PROBABILITY, GAME_LIMIT).get_tree_hash()
                        ),
                        result["additions"],
                    )
                )
            assert len(filtered_result) == 1
        finally:
            await network.close()

