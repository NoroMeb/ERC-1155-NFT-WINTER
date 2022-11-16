from scripts.utils import get_account
from brownie import Winter


def main():
    deploy()


def deploy():
    account = get_account()
    winter = Winter.deploy(
        "https://ipfs.io/ipfs/QmSGpwUpV25Y8ZGufYU5d7FxtduWxLi1pUREK3JUxBbBnf",
        {"from": account},
    )

    return winter
