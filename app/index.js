const { Web3 } = require('web3');
var web3 = new Web3('https://rpc.mordor.etccooperative.org');
const path = require('path');
const ethUtil = require('ethereumjs-util');

const express = require('express');
const bodyParser = require('body-parser');

const app = express();
// const PORT = 3000;

const contractData = require('./contracts/Users.json');
const contractABI = contractData;
const contractAddress = '0x2f23b3a502CB631018c095494C2DB87d7cD0c6cE'; // Your contract's deployed address
const contract = new web3.eth.Contract(contractABI, contractAddress);

async function fetchUsersCount() {
    try {
        const accounts = await web3.eth.getAccounts();
        const usersCount = await contract.methods.getUsersCount().call({ from: accounts[0] });
        return usersCount;
    } catch (error) {
        console.error('Error fetching users count:', error);
    }
}


async function addUserToContract(fromAccount, name, physical_address, phone_number, user_type) {
    try {
        const receipt = await contract.methods.addUser(name, physical_address, phone_number, user_type, fromAccount).send({ from: fromAccount });
        return receipt;
    } catch (error) {
        console.error('Error adding user:', error);
    }
}

async function fetchUser(index) {
    try {
        const accounts = await web3.eth.getAccounts();
        const user = await contract.methods.getUser(index).call({ from: accounts[0] });
        return user;
    } catch (error) {
        console.error('Error fetching user:', error);
    }
}

async function fetchUserType(public_key) {
    try {
        const accounts = await web3.eth.getAccounts();
        const userType = await contract.methods.getUserType(public_key).call({ from: accounts[0] });
        return userType;
    } catch (error) {
        console.error('Error fetching user type:', error);
    }
}

async function makePayment(fromAccount, public_key, amount) {
    try {
        const receipt = await contract.methods.payTo(public_key, amount).send({ from: fromAccount });
        return receipt;
    } catch (error) {
        console.error('Error making payment:', error);
    }
}

app.get('/users/count', async (req, res) => {
    try {
        const count = await fetchUsersCount();
        res.json({ count: count.toString() });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send('Error fetching users count.');
    }
});

app.get('/users/:index', async (req, res) => {
    try {
        const user = await fetchUser(req.params.index);
        res.json({
            id: user[0].toString(),
            name: user[1],
            physical_address: user[2],
            phone_number: user[3],
            user_type: user[4],
            public_key: user[5]
        });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send('Error fetching user.');
    }
});

app.get('/users/type/:public_key', async (req, res) => {
    try {
        const userType = await fetchUserType(req.params.public_key);
        res.json({ user_type: userType });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send('Error fetching user type.');
    }
});


async function fetchAllUsers() {
    try {
        const accounts = await web3.eth.getAccounts();
        const userCount = await fetchUsersCount();
        const allUsers = [];

        for (let i = 0; i < userCount; i++) {
            const user = await fetchUser(i);
            allUsers.push({
                id: user[0].toString(),
                name: user[1],
                physical_address: user[2],
                phone_number: user[3],
                user_type: user[4],
                public_key: user[5]
            });
        }

        return allUsers;
    } catch (error) {
        console.error('Error fetching all users:', error);
    }
}

app.get('/users', async (req, res) => {
    try {
        const users = await fetchAllUsers();
        res.json(users);
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send('Error fetching all users.');
    }
});

app.post('/pay', async (req, res) => {
    try {
        const { account, public_key, amount } = req.body;

        if (!account || !public_key || !amount) {
            return res.status(400).send('Missing account, public_key, or amount in request body.');
        }
        const receipt = await makePayment(account, public_key, parseInt(amount));
        res.json({ transactionHash: receipt.transactionHash });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send('Error making payment.');
    }
});

app.post('/users', async (req, res) => {
    try {
        const { account, name, physical_address, phone_number, user_type } = req.body;

        // Validate input
        if (!account || !name || !physical_address || !phone_number || !user_type) {
            return res.status(400).send('Missing required fields in request body.');
        }

        const receipt = await addUserToContract(account, name, physical_address, phone_number, user_type);
        res.json({ transactionHash: receipt.transactionHash });
    } catch (error) {
        console.error("Error:", error);
        res.status(500).send('Error adding user.');
    }
});


const PORT = 4000; 
const HOST = '0.0.0.0';

app.listen(PORT, HOST, () => {
    console.log(`Server is running on http://${HOST}:${PORT}`);
});