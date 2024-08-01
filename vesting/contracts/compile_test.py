import json
import os
from web3 import Web3
from solcx import compile_standard, install_solc

# Install a specific version of the Solidity compiler
install_solc('0.8.0')

# Define paths
ABI_FILE = 'phb_abi.json'
BYTECODE_FILE = 'phb_bytecode.json'
SOURCE_FILE = 'phb.sol'

# Define the Solidity code as a string
solidity_code = '''
pragma solidity ^0.8.0;

contract PHB {
    address public owner;
    mapping(address => Role) public roles;
    enum Role { None, User, Partner, Team }

    uint256 public constant USER_ALLOCATION = 50;
    uint256 public constant PARTNER_ALLOCATION = 25;
    uint256 public constant TEAM_ALLOCATION = 25;

    uint256 public constant USER_CLIFF = 10 * 30 days;
    uint256 public constant PARTNER_CLIFF = 2 * 30 days;
    uint256 public constant TEAM_CLIFF = 2 * 30 days;

    constructor() {
        owner = msg.sender;
    }

    function addBeneficiary(address _beneficiary, Role _role) public onlyOwner {
        roles[_beneficiary] = _role;
    }

    function claimTokens() public {
        // Implement token claiming logic based on role
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }
}
'''

def compile_contract():
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            SOURCE_FILE: {
                "content": solidity_code
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["metadata", "evm.bytecode", "evm.bytecode.sourceMap", "evm.abi"]
                }
            }
        }
    }, solc_version='0.8.0')

    # Extract ABI and bytecode
    try:
        contract_name = 'PHB'
        abi = json.loads(compiled_sol['contracts'][SOURCE_FILE][contract_name]['metadata'])['output']['abi']
        bytecode = compiled_sol['contracts'][SOURCE_FILE][contract_name]['evm']['bytecode']['object']

        # Save ABI and bytecode to files
        with open(ABI_FILE, 'w') as f:
            json.dump(abi, f)

        with open(BYTECODE_FILE, 'w') as f:
            json.dump(bytecode, f)

        print("Compiled ABI and bytecode saved to files.")

    except KeyError as e:
        print(f"KeyError: {e}. Please check the structure of the compiled output.")

def load_contract_details():
    with open(ABI_FILE, 'r') as f:
        abi = json.load(f)
    
    with open(BYTECODE_FILE, 'r') as f:
        bytecode = json.load(f)
    
    return abi, bytecode

def deploy_contract():
    blockchain_address = 'http://127.0.0.1:7545'
    web3 = Web3(Web3.HTTPProvider(blockchain_address))

    if not web3.is_connected():
        print("Failed to connect to the blockchain.")
        return

    web3.eth.default_account = web3.eth.accounts[0]
    abi, bytecode = load_contract_details()

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor().transact()
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    with open('contract_address.txt', 'w') as f:
        f.write(tx_receipt.contractAddress)
    
    print(f"Contract deployed at address: {tx_receipt.contractAddress}")


def main():
    compile_contract()
    deploy_contract()

if __name__ == "__main__":
    main()
