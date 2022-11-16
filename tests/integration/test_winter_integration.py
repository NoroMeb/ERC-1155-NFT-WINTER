from scripts.utils import get_account
from brownie import accounts, config
from web3 import Web3


def test_winter_integration(skip_local_testing, winter):
    # Arrange
    skip_local_testing
    account = get_account()
    winter = winter
    public_purchaser = get_account()
    allowed_account = accounts.add(config["wallets"]["from_key_2"])
    allow_list = [allowed_account.address]
    account_initial_balance = account.balance()
    # Act
    winter.editPurchaseWindows(True, True, {"from": account})
    winter.publicPurchase(
        10, {"from": public_purchaser, "value": Web3.toWei(0.1, "ether")}
    )
    winter.setAllowList(allow_list, {"from": account})
    winter.allowListPurchase(
        20, {"from": allowed_account, "value": Web3.toWei(0.02, "ether")}
    )
    winter.withdraw({"from": account})

    # Assert
    assert winter.balanceOf(public_purchaser, 0) == 10
    assert winter.balanceOf(allowed_account, 0) == 20
    assert account.balance() > account_initial_balance
