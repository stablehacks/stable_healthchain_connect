# test.py
from flask import Flask, render_template, request
from web3 import Web3
from solidity.helloSolidity import HelloSolidityContract
import json
from stateMachine.stateMachine import StateMachine, state_1, state_2, state_3

app = Flask(__name__)

# Load contract ABI from JSON file
with open(f'C:\\Users\\Jacob\\work\\supplychain\\contract.json') as config:
    contract_abi = json.load(config)

# Set your contract address and Ethereum node provider
contract_address = '0x4D6EF45276673AB60C10bD6716255Ea6e46F30d5'
web3_provider = 'https://sepolia.infura.io/v3/314f3f9b4c574f9ba6a18204cda5dd8d'

# Create an instance of HelloSolidityContract
hello_solidity_contract = HelloSolidityContract(contract_address, contract_abi, web3_provider)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/interact_with_blockchain', methods=['POST'])
def interact_with_blockchain():
    try:
        states = {
            '1': state_1,
            '2': state_2,
            '3': state_3
            # Add more states as needed
        }

        state_machine = StateMachine(states)

        # Set the initial state to '1'
        state_machine.set_state('1')

        # Run the state machine and capture the output
        output_logs = []
        state_machine.run(lambda log: output_logs.append(log))

        # Render the logs in the HTML page
        return render_template('index.html', logs=output_logs)

    except Exception as e:
        return f"Error getting message: {str(e)}"

@app.route('/set_message', methods=['POST'])
def set_message():
    # Implement the function to set a new message on the contract
    # You'll need the user's private key to sign the transaction
    return "Set message functionality not implemented yet"

if __name__ == '__main__':
    app.run(debug=True)
