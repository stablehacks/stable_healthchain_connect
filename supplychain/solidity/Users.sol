// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Usertoken is ERC20 {
    constructor() ERC20("User", "UserToken") {
        _mint(msg.sender, 1000000 * (10 ** uint256(decimals())));
    }
}

contract Users {

    struct User {
        uint id;
        string name;
        string physical_address;
        string phone_number;
        string user_type;
        string public_key;
    }

    User[] public users;
    Usertoken public tokenContract;
    uint public latestId = 1;
    mapping(string => string) public publicKeyToUserType;

    function addUser(string memory name, string memory physical_address, string memory phone_number, string memory user_type, string memory public_key) public {
        User memory newUser = User({
            id: latestId,
            name: name,
            physical_address: physical_address,
            phone_number: phone_number,
            user_type: user_type,
            public_key: public_key
        });

        users.push(newUser);
        latestId++;
        publicKeyToUserType[public_key] = user_type;
    }

    function getUser(uint _index) public view returns (uint, string memory, string memory, string memory, string memory, string memory) {
        require(_index < users.length, "User does not exist");
        User memory user = users[_index];
        return (user.id, user.name, user.physical_address, user.phone_number, user.user_type, user.public_key);
    }

    function getUsersCount() public view returns (uint) {
        return users.length;
    }
    function getUserType(string memory public_key) public view returns (string memory) {
        return publicKeyToUserType[public_key];
    }



    constructor(address _tokenAddress) {
        tokenContract = Usertoken(_tokenAddress);
    }

    function payTo(string memory public_key, uint amount) public {
    // Check allowance
    require(tokenContract.allowance(msg.sender, address(this)) >= amount, "Insufficient allowance");

    // Transfer tokens from user to contract
    tokenContract.transferFrom(msg.sender, address(this), amount);

    // Emit Payment event
    emit Payment(public_key, amount);
}
    event Payment(string public_key, uint amount);
}
