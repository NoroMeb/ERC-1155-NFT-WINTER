//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155URIStorage.sol";
import "@openzeppelin/contracts/token/ERC1155/extensions/ERC1155Supply.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Winter is ERC1155URIStorage, ERC1155Supply, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    uint256 public maxSupply = 6000;
    mapping(address => bool) public allowed;
    bool public publicMintOpen = false;
    bool public allowListMintOpen = false;

    uint256 public publicPrice = 0.01 ether;
    uint256 public allowListPrice = 0.001 ether;

    constructor(string memory _tokenURI) ERC1155("") {
        _setURI(_tokenIds.current(), _tokenURI);
    }

    function editPurchaseWindows(bool _publicMintOpen, bool _allowListMintOpen)
        external
        onlyOwner
    {
        publicMintOpen = _publicMintOpen;
        allowListMintOpen = _allowListMintOpen;
    }

    function startNextStage(
        uint256 _publicPrice,
        uint256 _allowListPrice,
        uint256 _maxSupply,
        string memory _tokenURI
    ) external onlyOwner {
        _tokenIds.increment();
        uint256 tokenId = _tokenIds.current();
        maxSupply = _maxSupply;
        publicPrice = _publicPrice;
        allowListPrice = _allowListPrice;
        _setURI(tokenId, _tokenURI);
    }

    function publicPurchase(uint256 _amount) public payable {
        require(publicMintOpen, "Public purchase closed");
        require(msg.value >= publicPrice * _amount, "not enogh ether");

        _internalMint(_amount);
    }

    function allowListPurchase(uint256 _amount) public payable {
        require(allowListMintOpen, "Allow list purchase Closed");
        require(allowed[msg.sender], "Only allow list members can purshase");
        require(msg.value >= allowListPrice * _amount, "not enogh ether");
        _internalMint(_amount);
    }

    function _internalMint(uint256 _amount) internal {
        uint256 tokenId = _tokenIds.current();
        require(
            totalSupply(tokenId) + _amount <= maxSupply,
            "Sorry we have minted out"
        );
        _mint(msg.sender, tokenId, _amount, "");
    }

    function setAllowList(address[] calldata _allowList) public onlyOwner {
        for (uint256 i = 0; i < _allowList.length; i++) {
            allowed[_allowList[i]] = true;
        }
    }

    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        payable(msg.sender).transfer(balance);
    }

    function uri(uint256 tokenId)
        public
        view
        override(ERC1155, ERC1155URIStorage)
        returns (string memory)
    {
        return ERC1155URIStorage.uri(tokenId);
    }

    function _beforeTokenTransfer(
        address operator,
        address from,
        address to,
        uint256[] memory ids,
        uint256[] memory amounts,
        bytes memory data
    ) internal virtual override(ERC1155, ERC1155Supply) {
        super._beforeTokenTransfer(operator, from, to, ids, amounts, data);
    }
}
