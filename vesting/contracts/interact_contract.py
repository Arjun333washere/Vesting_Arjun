import json
from web3 import Web3

# Define paths
ABI_FILE = 'phb_abi.json'
BYTECODE_FILE = 'phb_bytecode.json'
CONTRACT_ADDRESS_FILE = 'contract_address.txt'

# Connect to the blockchain
blockchain_address = 'http://127.0.0.1:7545'
web3 = Web3(Web3.HTTPProvider(blockchain_address))

if not web3.is_connected():
    print("Failed to connect to the blockchain.")
    exit()

# Load ABI and contract address
with open(ABI_FILE, 'r') as f:
    abi = json.load(f)

with open(CONTRACT_ADDRESS_FILE, 'r') as f:
    contract_address = f.read().strip()

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Example function to call a view function
def get_owner():
    owner = contract.functions.owner().call()
    print(f"Contract owner: {owner}")

# Example function to send a transaction
def add_beneficiary(beneficiary_address, role):
    # Convert address to checksum format
    beneficiary_address = web3.to_checksum_address(beneficiary_address)
    
    # Make sure the account sending the transaction is unlocked
    web3.eth.default_account = web3.eth.accounts[0]
    
    tx_hash = contract.functions.addBeneficiary(beneficiary_address, role).transact()
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"Transaction receipt: {tx_receipt}")

# Example usage
get_owner()

# Add a beneficiary (use appropriate address and role)
beneficiary_address = '0x1234567890abcdef1234567890abcdef12345678'  # Replace with actual address
role = 1  # Replace with the desired role (e.g., 1 for Partner)
add_beneficiary(beneficiary_address, role)
