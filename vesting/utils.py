# vesting/utils.py
from web3 import Web3
import json

def get_contract(web3):
    # Load ABI and Bytecode
    with open('vesting/contracts/phb_abi.json', 'r') as f:
        abi = json.load(f)
    with open('vesting/contracts/phb_bytecode.json', 'r') as f:
        bytecode = json.load(f)

    # Contract address
    contract_address = '0x76880Bc826eD30e6A484E0573bE4211e4925CbeF'

    # Create contract instance
    return web3.eth.contract(address=contract_address, abi=abi)
