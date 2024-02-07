README

This Flask application allows users to interact with a blockchain-based smart contract to create users and doctors, and make appointments with doctors. Below are the steps to start and use the application:

Starting the Application

Make sure you have Python installed on your system.
Clone or download the project repository.
Navigate to the project directory in your terminal or command prompt.
Install the required Python packages by running pip install -r requirements.txt.
Start the Flask application by running python main.py.
The application will be running on http://127.0.0.1:5000. Access this URL in your web browser to use the application.
Creating a Doctor

Before creating a doctor, ensure that the smart contract has been deployed. Update the contract address in the main.py script to match the deployed contract address.
Navigate to the "Create Doctor" page by clicking on the respective link.
Fill in the required details for the doctor, including first name, last name, certificate hash, specialization, public key, and location.
Click the submit button to create the doctor.
Navigating to the Home Page and Clicking the Matching Button

After creating the doctor, navigate back to the home page by clicking on the logo or home link.
Click the "Matching" button to initiate the process of finding a doctor based on specific criteria.
Making an Appointment

The application will locate the doctor in the smart contract based on predefined criteria (e.g., doctor type = Family Medicine and location = Saskatoon) and provide a page to make an appointment.
Fill in the required details for the appointment, including doctor ID, patient name, and appointment details.
Click the submit button to make the appointment.
Note that payment functionality has not been implemented but can be implied by making an appointment. A script could easily be generated to facilitate this.
Database

Appointments are stored in the database. For the minimum viable product, the same appointment cannot be duplicated.
Note: This is a basic version of the application, and certain details need to be spelled exactly as specified. Ensure that the doctor type and location match the predefined criteria for the matching process to work correctly.

For any issues or further assistance, feel free to contact the developer.

Developer:
Jacob Cyr
jacobncyr@outlook.com