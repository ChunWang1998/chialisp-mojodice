from typing import Dict, List, Optional

import pytest
import pytest_asyncio
from chia.types.blockchain_format.coin import Coin
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.ints import uint64

from piggybank.piggybank_drivers import (
    create_piggybank_puzzle,
    solution_for_piggybank,
    # piggybank_announcement_assertion,
)
from cdv.test import CoinWrapper
from cdv.test import setup as setup_test

class TestStandardTransaction:
    @pytest_asyncio.fixture(scope="function")
    async def setup(self):
        network, alice, bob = await setup_test()
        await network.farm_block()
        yield network, alice, bob

    async def make_and_spend_piggybank(self, network, alice, bob, CONTRIBUTION_AMOUNT,success_number, withdraw_amount,vault_after_withdraw_amount,vault_after_deposit_amount):#創建並存錢
        # Get our alice wallet some money
        await network.farm_block(farmer=alice)#給alice 存錢

        # This will use one mojo to create our piggybank on the blockchain. 
        piggybank_coin = await alice.launch_smart_coin (create_piggybank_puzzle(bob.puzzle_hash,50,10000000))#創建存錢罐,存滿會打到bob.puzzle_hash
        # This retrieves us a coin that is at least 500 mojos.
        contribution_coin = await alice.choose_coin(CONTRIBUTION_AMOUNT)#從alice 錢包內劃分出要放進去的token

        #This is the spend of the piggy bank coin.  We use the driver code to create the solution.
        piggybank_spend = await alice.spend_coin(
            piggybank_coin,
            pushtx=False,
            # solution_for_piggybank(success_number,pb_coin, withdraw_amount,vault_after_withdraw_amount,vault_after_deposit_amount):
            args=solution_for_piggybank(success_number,piggybank_coin.coin ,withdraw_amount,vault_after_withdraw_amount,vault_after_deposit_amount),
        )

        contribution_spend = await alice.spend_coin(#從alice 錢包扣錢
            contribution_coin,
            pushtx=False,
        )

        # Aggregate them to make sure they are spent together
        combined_spend = SpendBundle.aggregate([contribution_spend, piggybank_spend])#綁定在一起

        result = await network.push_tx(combined_spend)
        return result

    @pytest.mark.asyncio
    async def test_piggybank_withdraw(self, setup):
        network, alice, bob = setup
        try:
            result = await self.make_and_spend_piggybank(network, alice, bob, 30,56,40,90,140)

            assert "error" not in result #不應該有err

            filtered_result = list(filter(
                lambda addition:
                    (addition.amount == 90) and
                    (addition.puzzle_hash == create_piggybank_puzzle(bob.puzzle_hash,50,10000000).get_tree_hash())
            ,result["additions"]))
            assert len(filtered_result) == 1
        finally:
            await network.close()

    @pytest.mark.asyncio
    async def test_piggybank_deposit(self, setup):
        network, alice, bob = setup
        try:
            result = await self.make_and_spend_piggybank(network, alice, bob, 30,46,40,90,140)

            assert "error" not in result

            filtered_result = list(filter(
                lambda addition:
                    (addition.amount == 140) and
                    (addition.puzzle_hash == create_piggybank_puzzle(bob.puzzle_hash,50,10000000).get_tree_hash())
            ,result["additions"]))
            assert len(filtered_result) == 1
        finally:
            await network.close()

    # @pytest.mark.asyncio
    # async def test_piggybank_stealing(self, setup):
    #     network, alice, bob = setup
    #     try:
    #         result: Dict[str, List[Coin]] = await self.make_and_spend_piggybank(network, alice, bob, -100)
    #         assert "error" in result
    #         assert (
    #             "GENERATOR_RUNTIME_ERROR" in result["error"]
    #         )  # This fails during puzzle execution, not in driver code
    #     finally:
    #         await network.close()

