from flask import Flask, render_template, request, Response, jsonify
from web3 import Web3
import json

app = Flask(__name__,template_folder='templates')


@app.route('/create_user')
def create_user():
    return render_template('create_user.html')


@app.route('/create_doctor')
def create_doctor():
    return render_template('create_doctor.html')

@app.route('/interact_with_blockchain_create_user', methods=['POST'])
def interact_with_blockchain_create_user():
    # Get form data from the request

    # Specify the contract details and web3 provider
    contract_address = '0xE02d248a844CF17c9042EB722A671CD08dAa59D4'
    with open("Users_ABI.json") as f:
        contract_abi = json.load(f)
    web3_provider = 'https://sepolia.infura.io/v3/314f3f9b4c574f9ba6a18204cda5dd8d'

    # Connect to Ethereum node
    web3 = Web3(Web3.HTTPProvider(web3_provider))

    # Check connection
    if not web3.is_connected():
        raise Exception("Failed to connect to Ethereum node")

    # Load your smart contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    form_data = request.form.to_dict()

    print("Form Data:", form_data)

    # Extract user information from the form data
    name = form_data.get('name')
    physical_address = form_data.get('physical_address')
    phone_number = form_data.get('phone_number')
    user_type = form_data.get('user_type')
    public_key = form_data.get('public_key')

    print("Name:", name)
    print("Physical Address:", physical_address)
    print("Phone Number:", phone_number)
    print("User Type:", user_type)
    print("Public Key:", public_key)

    account_address = '0xf59da9813F55e39D141FF376366dDd46c1eC61B1'
    private_key = 'a5afc1ada62f160cb387869b76c019e40347c8091e27ba092d23cfc707afd25a'

    print("Account Address:", account_address)

    # Ensure the default account is set
    web3.eth.default_account = account_address

    # Prepare transaction
    add_user_txn = contract.functions.addUser(
        name, physical_address, phone_number, user_type, public_key
    ).build_transaction({
        'from': account_address,
        'nonce': web3.eth.get_transaction_count(account_address),
        'gasPrice': web3.eth.gas_price
    })

    print("Transaction:", add_user_txn)

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(add_user_txn, private_key)

    print("Signed Transaction:", signed_txn)

    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print("Transaction Hash:", tx_hash)

    # Wait for the transaction to be mined
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print("Transaction Receipt:", tx_receipt)

    return f"User added successfully with transaction hash: {tx_hash}"

@app.route('/interact_with_blockchain_create_doctor', methods=['POST'])
def interact_with_blockchain_create_doctor():
    # Specify the contract details and web3 provider
    contract_address = '0xE02d248a844CF17c9042EB722A671CD08dAa59D4'
    with open("doctor_ABI.json") as f:
        contract_abi = json.load(f)
    web3_provider = 'https://sepolia.infura.io/v3/314f3f9b4c574f9ba6a18204cda5dd8d'

    # Connect to Ethereum node
    web3 = Web3(Web3.HTTPProvider(web3_provider))

    # Check connection
    if not web3.is_connected():
        raise Exception("Failed to connect to Ethereum node")

    # Load your smart contract
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    try:
        # Get form data from the request
        form_data = request.form.to_dict()

        print("Form Data:", form_data)

        # Assuming certificateHash is obtained from the HTML form
        certifigate_hash = form_data.get('certificateHash')

        print("Certifigate Hash:", certifigate_hash)

        # Add doctor information
        first_name = form_data.get('firstName')
        last_name = form_data.get('lastName')
        specialization = form_data.get('specialization')
        public_key = form_data.get('public_key')
        location = form_data.get('location')

        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Specialization:", specialization)
        print("Public Key:", public_key)

        # Other variables
        account_address = '0xf59da9813F55e39D141FF376366dDd46c1eC61B1'
        private_key = 'a5afc1ada62f160cb387869b76c019e40347c8091e27ba092d23cfc707afd25a'

        print("Account Address:", account_address)

        # Ensure the default account is set
        web3.eth.default_account = account_address

        # Prepare transaction
        add_doctor_txn = contract.functions.addDoctor(
            first_name, last_name, certifigate_hash, specialization,location, public_key
        ).build_transaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gasPrice': web3.eth.gas_price
        })

        print("Transaction:", add_doctor_txn)

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(add_doctor_txn, private_key)

        print("Signed Transaction:", signed_txn)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print("Transaction Hash:", tx_hash)

        # Wait for the transaction to be mined
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print("Transaction Receipt:", tx_receipt)

        return f"Doctor added successfully with transaction hash: {tx_hash}"

    except Exception as e:
        # Handle exceptions appropriately
        print("Error:", str(e))
        # Render an error template or return an error response
        return render_template('error.html')

@app.route("/doctors")
def doctors():
    try:
        # Specify the contract details and web3 provider
        contract_address = '0xE02d248a844CF17c9042EB722A671CD08dAa59D4'
        with open("doctor_ABI.json") as f:
            contract_abi = json.load(f)
        web3_provider = 'https://sepolia.infura.io/v3/314f3f9b4c574f9ba6a18204cda5dd8d'

        # Connect to Ethereum node
        web3 = Web3(Web3.HTTPProvider(web3_provider))

        # Check connection
        if not web3.is_connected():
            raise Exception("Failed to connect to Ethereum node")

        # Load your smart contract
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        # Get the total number of doctors
        doctors_count = contract.functions.getDoctorsCount().call()

        # Fetch details for each doctor
        doctors = []
        for i in range(doctors_count):
            doctor_details = contract.functions.getDoctor(i).call()
            doctors.append({
                'id': doctor_details[0],
                'firstName': doctor_details[1],
                'lastName': doctor_details[2],
                'certificateHash': doctor_details[3],
                'specialization': doctor_details[4],
                'location': doctor_details[5],
                'public_key': doctor_details[6],

            })
        print(doctors)
        # Convert the doctors list to a JSON-formatted string
        doctors_json = json.dumps(doctors)

        # Create a Flask Response with the JSON data and appropriate headers
        response = Response(doctors_json, status=200, mimetype='application/json')
        return response

    except Exception as e:
        # Handle exceptions appropriately
        print("Error fetching doctors:", str(e))
        # Return an error response with JSON format
        error_response = {'error': 'Failed to fetch doctors'}
        return Response(json.dumps(error_response), status=500, mimetype='application/json')


@app.route("/match_page")
def match_page():
    return render_template("page.html")



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/match_page_result')
def match_page_result():
    try:
        # Specify the contract details and web3 provider
        contract_address = '0xE02d248a844CF17c9042EB722A671CD08dAa59D4'
        with open("doctor_ABI.json") as f:
            contract_abi = json.load(f)
        web3_provider = 'https://sepolia.infura.io/v3/314f3f9b4c574f9ba6a18204cda5dd8d'

        # Connect to Ethereum node
        web3 = Web3(Web3.HTTPProvider(web3_provider))

        # Check connection
        if not web3.is_connected():
            raise Exception("Failed to connect to Ethereum node")

        # Load your smart contract
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        # Get the total number of doctors
        doctors_count = contract.functions.getDoctorsCount().call()

        # Fetch details for each doctor
        doctors = []
        for i in range(doctors_count):
            doctor_details = contract.functions.getDoctor(i).call()
            doctors.append({
                'id': doctor_details[0],
                'firstName': doctor_details[1],
                'lastName': doctor_details[2],
                'certificateHash': doctor_details[3],
                'specialization': doctor_details[4],
                'location': doctor_details[5],
                'public_key': doctor_details[6],
            })
        print(doctors)

        # Pass the data to the template
        return render_template('match_page_result.html', doctors=doctors)

    except Exception as e:
        print("Error:", e)
        # Handle the error appropriately, for example, redirect to an error page or show an error message
        return "Error occurred while fetching doctor's data. Please try again later."


@app.route('/make_payment', methods=['POST'])
def make_payment():
    # Extract data from the request
    data = request.json
    doctor_id = data.get('id')

    # Implement the logic to interact with the blockchain and make the payment
    # This could involve calling a smart contract method, signing a transaction, etc.
    print('implement payment step here')
    # Return a response
    return jsonify({'success': True},200)



@app.route('/make_appointment', methods=['POST'])
def interact_with_blockchain_make_appointment():
    try:
        # Specify the contract details and web3 provider
        contract_address = '0xE02d248a844CF17c9042EB722A671CD08dAa59D4'
        with open("doctor_ABI.json") as f:
            contract_abi = json.load(f)
        web3_provider = 'https://sepolia.infura.io/v3/314f3f9b4c574f9ba6a18204cda5dd8d'

        # Connect to Ethereum node
        web3 = Web3(Web3.HTTPProvider(web3_provider))

        # Load your smart contract
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        # Get form data from the request
        # Get form data from the request
        form_data = request.json
        # Extract form data
        doctor_id = int(form_data.get('doctorId'))
        patient_name = form_data.get('patientName')
        appointment_details = form_data.get('appointmentDetails')

        # Other variables
        account_address = '0xf59da9813F55e39D141FF376366dDd46c1eC61B1'
        private_key = 'a5afc1ada62f160cb387869b76c019e40347c8091e27ba092d23cfc707afd25a'

        # Ensure the default account is set
        web3.eth.default_account = account_address

        # Get the latest nonce
        nonce = web3.eth.get_transaction_count(account_address)

        # Prepare transaction with updated nonce
        txn_data = contract.functions.makeAppointment(doctor_id, patient_name, appointment_details).build_transaction({
            'from': account_address,
            'nonce': nonce,  # Use the latest nonce here
            'gasPrice': web3.eth.gas_price
        })

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(txn_data, private_key)

        # Send the transaction
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Appointment made successfully with transaction hash: {tx_hash.hex()}")
        return f"Appointment made successfully with transaction hash: {tx_hash}"
    except Exception as e:
        print("Error:", str(e))
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)

