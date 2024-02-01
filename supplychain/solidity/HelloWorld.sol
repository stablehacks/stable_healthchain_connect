// HelloWorld.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Helloworld {
    string private message;

    constructor() {
        message = "Hello, pycharm from Solidity!";
    }

    function getMessage() public view returns (string memory) {
        return message;
    }

    function setMessage(string memory newMessage) public {
        message = newMessage;
    }
}