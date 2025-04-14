RPC_URL = "http://localhost/rpc"

user_infos = {
    "PrivateKey": "0xca11ab1ec0ffee000002a575fa5f74540719ba065a610cba6497cdbf22cd5cdb",
    "TargetAddress": "0xDdd922941363BCa7C4E0e9486b56e393F0649227"
}


from web3 import Web3, AsyncWeb3
from solcx import compile_source, install_solc

# Connect to the RPC
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "Not connected to the blockchain"

# Compile contracts
with open('dst/Sublocku.sol','r') as f : 
    source_code = f.read() 

install_solc('0.8.26')
compiled_sol = compile_source(source_code, solc_version='0.8.26')  
print(f"Compiled classes : {compiled_sol.keys()}")

# Add account from private key
account = w3.eth.account.from_key(user_infos['PrivateKey'])
print(f"Account: {account.address}")
print(f"Balance: {Web3.from_wei(w3.eth.get_balance(account.address),'ether')}")
nonce = w3.eth.get_transaction_count(account.address)

# # Load the target contract
sublocku_contract = w3.eth.contract(address=user_infos['TargetAddress'], abi=compiled_sol['<stdin>:Sublocku']['abi'])
print(f"Contract: {sublocku_contract.all_functions()}")


def getGameState() :
    game = []

    # The slot index containing the array length (should be 32bytes long, in hex, with no 0x and as a string)
    slot_row = "0000000000000000000000000000000000000000000000000000000000000001"
    new_slot_row = w3.keccak(hexstr=slot_row)

    # Retrieve the length of the array from the slot_index
    game_row_number = int(w3.eth.get_storage_at(sublocku_contract.address, slot_row).hex(),16)

    # If the array is an array of structs or somthing else, you can multiply this value by the size of the struct
    for row_id in range(game_row_number) : 
        game.append([])
        tmp_key_row = int(new_slot_row.hex(), 16)+row_id
        game_col_number = w3.eth.get_storage_at(sublocku_contract.address, tmp_key_row)

        # print(f"Row {row_id} is in slot {hex(tmp_key_row)} with value {game_col_number.hex()};")
        
        slot_col = hex(tmp_key_row)[2:]
        new_slot_col = w3.keccak(hexstr=slot_col)
        for col_id in range(9) :
            tmp_key_col = int(new_slot_col.hex(), 16) +col_id
            storage_value = w3.eth.get_storage_at(sublocku_contract.address, tmp_key_col)
            # print(f"{row_id}{col_id} : Key : {hex(tmp_key_col)}; Storage value : {storage_value.hex()};")
            game[row_id].append(int(storage_value.hex(),16))
    return game


        
game = getGameState()
for line in game : 
    print(line)

