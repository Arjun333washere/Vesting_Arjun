from web3 import Web3
import json

# Connect to local Ethereum node (Ganache)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Check if connected to Ethereum node
if not web3.is_connected():
    print("Failed to connect to the Ethereum node.")
    exit()

# Load contract ABI and bytecode
with open('vesting_abi.json', 'r') as abi_file:
    abi = json.load(abi_file)

with open('vesting_bytecode.bin', 'r') as bytecode_file:
    bytecode = bytecode_file.read()

# Set the default account (optional, if needed for deployment)
web3.eth.default_account = web3.eth.accounts[0]

# Define contract
contract = web3.eth.contract(abi=abi, bytecode=bytecode)

# Deploy contract
transaction = contract.constructor().buildTransaction({
    'from': web3.eth.default_account,
    'gas': 5000000,  # Adjust as needed
    'gasPrice': web3.toWei('5', 'gwei')  # Adjust as needed
})

# Sign and send transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key='4723dfde215fa88aaf086b914513f79b392ce99fb32e8c65ada37dd836f04f05')
tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for transaction receipt
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Contract address
print(f'Contract deployed at address: {receipt.contractAddress}')

