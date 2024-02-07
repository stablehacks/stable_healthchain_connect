// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DoctorCoin is ERC20 {
    constructor() ERC20("DoctorCoin", "DCTC") {
        _mint(msg.sender, 1000000 * (10 ** uint256(decimals())));
    }
}

contract Doctors {

    struct Doctor {
        uint id;
        string firstName;
        string lastName;
        string certificateHash;
        string specialization;
        string public_key;
        string location;
    }

    address public usertokenContractAddress;
    Doctor[] public doctors;
    uint public latestId = 1;
    mapping(string => string) public publicKeyToSpecialization;

    event DoctorAdded(uint id, string firstName, string lastName, string certificateHash, string specialization, string public_key, string location);
    event AppointmentLogged(uint indexed doctorId, string patientName, string appointmentDetails, uint timestamp);
    event PaymentReceived(address indexed from, address indexed to, uint amount, uint timestamp);

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

    function makeAppointment(uint doctorId, string memory patientName, string memory appointmentDetails) public {
        require(doctorId > 0 && doctorId <= doctors.length, "Invalid doctor ID");
        emit AppointmentLogged(doctorId, patientName, appointmentDetails, block.timestamp);
    }

    function receivePayment(uint amount) public payable {
        require(amount > 0, "Invalid amount");
        IERC20 usertokenContract = IERC20(usertokenContractAddress);
        usertokenContract.transferFrom(msg.sender, address(this), amount);
        emit PaymentReceived(msg.sender, address(this), amount, block.timestamp);
    }
}
