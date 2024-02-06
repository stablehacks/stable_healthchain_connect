// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Doctors {

    struct Doctor {
        uint id;
        string firstName;
        string lastName;
        string certificateHash; // Assuming certificate is stored off-chain and only hash is kept
        string specialization;
        string public_key;
        string location; // New field for the doctor's location
    }

    address public usertokenContractAddress;
    Doctor[] public doctors;
    uint public latestId = 1;
    mapping(string => string) public publicKeyToSpecialization;

    event DoctorAdded(uint id, string firstName, string lastName, string certificateHash, string specialization, string public_key, string location);

    function addDoctor(
        string memory firstName,
        string memory lastName,
        string memory certificateHash,
        string memory specialization,
        string memory public_key,
        string memory location
    ) public {
        Doctor memory newDoctor = Doctor({
            id: latestId,
            firstName: firstName,
            lastName: lastName,
            certificateHash: certificateHash,
            specialization: specialization,
            public_key: public_key,
            location: location
        });

        doctors.push(newDoctor);
        latestId++;
        publicKeyToSpecialization[public_key] = specialization;

        emit DoctorAdded(latestId, firstName, lastName, certificateHash, specialization, public_key, location);
    }

    function getDoctor(uint _index) public view returns (uint, string memory, string memory, string memory, string memory, string memory, string memory) {
        require(_index < doctors.length, "Doctor does not exist");
        Doctor memory doctor = doctors[_index];
        return (doctor.id, doctor.firstName, doctor.lastName, doctor.certificateHash, doctor.specialization, doctor.public_key, doctor.location);
    }

    function getDoctorsCount() public view returns (uint) {
        return doctors.length;
    }

    function getSpecialization(string memory public_key) public view returns (string memory) {
        return publicKeyToSpecialization[public_key];
    }

    function getDoctorBalance(address public_key) public view returns (uint) {
        // Access the ERC-20 contract using the IERC20 interface
        IERC20 usertokenContract = IERC20(usertokenContractAddress);

        // Query the balance associated with the doctor's Ethereum address
        uint balance = usertokenContract.balanceOf(public_key);

        return balance;
    }
}
