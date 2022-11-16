import pytest
from brownie import network, Winter
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

TOKEN_ZERO_URI = "https://ipfs.io/ipfs/QmSGpwUpV25Y8ZGufYU5d7FxtduWxLi1pUREK3JUxBbBnf"


@pytest.fixture
def skip_live_testing():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing !")


@pytest.fixture
def skip_local_testing():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for live testing !")


@pytest.fixture
def winter():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        winter = Winter.deploy(TOKEN_ZERO_URI, {"from": account}, publish_source=True)
    elif network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        winter = Winter.deploy(TOKEN_ZERO_URI, {"from": account})

    return winter


@pytest.fixture
def token_zero_uri():
    return TOKEN_ZERO_URI
