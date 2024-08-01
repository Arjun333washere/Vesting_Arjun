# vesting_app/views.py
from django.shortcuts import render
from django.http import HttpResponse
from web3 import Web3
import json

from web3 import Web3
from django.shortcuts import render, redirect
from .utils import get_contract

# Load ABI and Bytecode
with open('vesting/contracts/phb_abi.json', 'r') as f:
    abi = json.load(f)

with open('vesting/contracts/phb_bytecode.json', 'r') as f:
    bytecode = json.load(f)

# Set up Web3
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
web3.eth.defaultAccount = web3.eth.accounts[0]
contract_address = '0x76880Bc826eD30e6A484E0573bE4211e4925CbeF'  # Replace with your contract address
contract = web3.eth.contract(address=contract_address, abi=abi)

def index(request):
    return render(request, 'index.html')

def get_owner(request):
    owner = contract.functions.owner().call()
    return HttpResponse(f"Contract owner: {owner}")

""" def add_beneficiary(request):
    if request.method == 'POST':
        beneficiary_address = request.POST.get('beneficiary_address')
        role = int(request.POST.get('role'))
        tx_hash = contract.functions.addBeneficiary(beneficiary_address, role).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return HttpResponse(f"Beneficiary added. Transaction hash: {tx_hash.hex()}")
    return render(request, 'add_beneficiary.html') """


def add_beneficiary(request):
    if request.method == "POST":
        beneficiary_address = request.POST.get("beneficiary_address")
        role = int(request.POST.get("role"))
        web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

        contract = get_contract(web3)  # Assuming you have this utility function

        # Get the default account (should be one of the Ganache accounts)
        default_account = web3.eth.accounts[0]  # Use a valid account from Ganache

        try:
            tx_hash = contract.functions.addBeneficiary(beneficiary_address, role).transact({
                'from': default_account
            })
            web3.eth.waitForTransactionReceipt(tx_hash)
            return render(request, 'vesting/add_beneficiary.html', {'tx_hash': tx_hash.hex()})
        except Exception as e:
            return render(request, 'vesting/add_beneficiary.html', {'error': str(e)})

    return render(request, 'vesting/add_beneficiary.html')
