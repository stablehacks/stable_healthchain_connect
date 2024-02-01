from web3 import Web3

# Connect to a local Ethereum node or Infura (replace the URL with your Infura project ID)
w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/314f3f9b4c574f9ba6a18204cda5dd8d'))
# Or use Infura: w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Set your contract ABI
contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "newMessage",
				"type": "string"
			}
		],
		"name": "setMessage",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "getMessage",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# helloSolidity.py
from web3 import Web3

class HelloSolidityContract:
    def __init__(self, contract_address, contract_abi, web3_provider):
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)

    def get_message(self):
        try:
            message = self.contract.functions.getMessage().call()
            return message
        except Exception as e:
            raise Exception(f"Error getting message: {str(e)}")

    def set_message(self, private_key, new_message):
        # Implement the logic to set a new message on the contract using the provided private key
        # Make sure to handle the transaction signing and sending
        pass
