from scripts.deploy import deploy
from scripts.utils import get_account
from brownie import exceptions
import pytest
from web3 import Web3


def test_edit_purchase_windows(skip_live_testing, winter):
    # Arrange
    skip_live_testing
    account = get_account()
    non_owner = get_account(index=1)
    winter = winter

    # Assert
    assert winter.publicMintOpen() == False
    assert winter.allowListMintOpen() == False

    # Act
    winter.editPurchaseWindows(True, True, {"from": account})

    # Assert
    assert winter.publicMintOpen() == True
    assert winter.allowListMintOpen() == True
    with pytest.raises(exceptions.VirtualMachineError):
        winter.editPurchaseWindows(True, True, {"from": non_owner})

    return winter


def test_next_stage(skip_live_testing, winter, token_zero_uri):
    # Arrange
    skip_live_testing
    account = get_account()
    non_owner = get_account(index=1)
    winter = winter
    next_public_price = Web3.toWei(0.5, "ether")
    next_allow_list_price = Web3.toWei(0.2, "ether")
    next_max_supply = 1000
    next_token_uri = (
        "https://ipfs.io/ipfs/Qmd77YzwGCbkxNF3pahRfGSB33eXTwS2g37cEYnVMozrX3"
    )

    # Assert
    assert winter.publicPrice() == Web3.toWei(0.01, "ether")
    assert winter.allowListPrice() == Web3.toWei(0.001, "ether")
    assert winter.maxSupply() == 6000
    assert winter.uri(0) == token_zero_uri

    # Act
    winter.startNextStage(
        next_public_price,
        next_allow_list_price,
        next_max_supply,
        next_token_uri,
        {"from": account},
    )

    # Assert
    assert winter.publicPrice() == next_public_price
    assert winter.allowListPrice() == next_allow_list_price
    assert winter.maxSupply() == next_max_supply
    assert winter.uri(1) == next_token_uri
    with pytest.raises(exceptions.VirtualMachineError):
        winter.startNextStage(
            next_public_price,
            next_allow_list_price,
            next_max_supply,
            next_token_uri,
            {"from": non_owner},
        )


def test_public_purchase(skip_live_testing, winter):
    # Arrange
    skip_live_testing
    account = get_account()
    purchaser = get_account(index=1)
    winter = test_edit_purchase_windows(skip_live_testing, winter)
    value = Web3.toWei(0.2, "ether")
    not_enough_value = Web3.toWei(0.01, "ether")
    amount = 20
    # Act
    winter.publicPurchase(amount, {"from": purchaser, "value": value})

    # Assert
    assert winter.balanceOf(purchaser, 0) == amount
    with pytest.raises(exceptions.VirtualMachineError):
        winter.editPurchaseWindows(False, True, {"from": account})
        winter.publicPurchase(amount, {"from": purchaser, "value": value})
    with pytest.raises(exceptions.VirtualMachineError):
        winter.publicPurchase(amount, {"from": purchaser, "value": not_enough_value})
    with pytest.raises(exceptions.VirtualMachineError):
        winter.publicPurchase(
            6001, {"from": purchaser, "value": Web3.toWei(60.01, "ether")}
        )

    return winter


def test_set_allow_list(skip_live_testing, winter):
    # Arrange
    skip_live_testing
    account = get_account()
    winter = winter
    non_owner = get_account(index=1)
    allow_list = []
    for i in range(1, 3):
        allow_list.append(get_account(index=i))

    # Act
    winter.setAllowList(allow_list, {"from": account})
    # Assert
    for allowed_address in allow_list:
        assert winter.allowed(allowed_address) == True

    with pytest.raises(exceptions.VirtualMachineError):
        winter.setAllowList(allow_list, {"from": non_owner})

    return winter


def test_allow_list_purchase(skip_live_testing, winter):
    # Arrange
    skip_live_testing
    account = get_account()
    winter = test_set_allow_list(skip_live_testing, winter)
    allowed_account = get_account(index=1)
    not_allowed_account = get_account(index=4)
    value = Web3.toWei(0.02, "ether")
    not_enough_value = Web3.toWei(0.01, "ether")
    amount = 20
    winter.editPurchaseWindows(False, True, {"from": account})
    # Act
    winter.allowListPurchase(amount, {"from": allowed_account, "value": value})

    # Assert
    assert winter.balanceOf(allowed_account, 0) == amount
    with pytest.raises(exceptions.VirtualMachineError):
        winter.editPurchaseWindows(False, False, {"from": account})
        winter.allowListPurchase(amount, {"from": allowed_account, "value": value})
    with pytest.raises(exceptions.VirtualMachineError):
        winter.allowListPurchase(
            amount, {"from": allowed_account, "value": not_enough_value}
        )
    with pytest.raises(exceptions.VirtualMachineError):
        winter.allowListPurchase(amount, {"from": not_allowed_account, "value": value})

    with pytest.raises(exceptions.VirtualMachineError):
        winter.allowListPurchase(
            6001, {"from": allowed_account, "value": Web3.toWei(6.001, "ether")}
        )


def test_withdraw(skip_live_testing, winter):
    # Arrange
    skip_live_testing
    account = get_account()
    winter = test_public_purchase(skip_live_testing, winter)
    initial_winter_balance = winter.balance()
    initial_account_balance = account.balance()
    non_owner = get_account(index=1)
    # Act
    winter.withdraw({"from": account})

    # Assert
    assert initial_winter_balance == Web3.toWei(0.2, "ether")
    assert winter.balance() == 0
    assert account.balance() == initial_account_balance + Web3.toWei(0.2, "ether")
    with pytest.raises(exceptions.VirtualMachineError):
        winter.withdraw({"from": non_owner})


def test_uri(skip_live_testing, winter, token_zero_uri):
    # Arrange
    skip_live_testing

    # Act / Assert
    winter.uri(0) == token_zero_uri
