# Runs an anvil blockchain as well as a Flask application

import subprocess
from os import environ
from eth_account.hdaccount import generate_mnemonic
from eth_account import Account
from flask import Flask, Response, request, abort, render_template
import requests
from web3 import Web3
from time import sleep
from re import findall
from random import choice
Account.enable_unaudited_hdwallet_features()


CHALLNAME = "Sublocku"
DESCRIPTION_HTML = "To get the flag, unlock the vault !<br>But, wait ? Where is the grid ?"
FLAG = 'MCTF{2f5c0a0afcae1a1c5c0eadc25345f2f3}'


mnemonic = generate_mnemonic(12, 'english')
player_account = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/0")

PLAYER_ADDRESS = player_account.address
PLAYER_KEY = player_account._private_key.hex()
PLAYER_ETH = '10'

HARDFORK = "latest" # Can be latest, cancun, shanghai, london, paris, ...

CHALL_NOT_SOLVED_MESSAGES = [
    "Try again...",
    "Nope. Hack harder!",
    "Skill issue detected!",
    "Wrong answer, or is it? (Hint: It is.)",
    "Bruh... seriously?",
    "You tried. That’s what matters... kinda.",
    "Hmm... nope!",
    "Hah! Not today!",
    "Incorrect, but I admire your spirit!",
    "That ain’t it, chief!",
    "Are you even trying?",
    "C'mon, you got this… probably.",
    "That’s a hard no from me.",
    "Nope. But at least you didn’t segfault!",
    "L + ratio + no flag",
    "Even ChatGPT wouldn’t fall for that attempt!",
    "Issue detected at OSI Layer 8.",
    "Hack the planet! …or at least try again.",
    "Are you randomly typing?",
    "99% of hacking is figuring out what you did wrong.",
    "Your solution was sent to /dev/null and nobody noticed.",
    "You’re trying… and that’s cute.",
    "I’ve seen bots with better logic than that."
]

# DO NOT EDIT
RPC_URL = 'http://127.0.0.1:8545'
BIN = '/challenge/.foundry/bin'
CWD = "/challenge/blockchain"
CHAINID = '1337'



mnemonic = generate_mnemonic(12, 'english')

deployer_account = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/0")
deployer_key = deployer_account._private_key.hex()
deployer_address = deployer_account.address

contracts = {}

# Runs an anvil in the background
proc = subprocess.Popen(
    args=[
        f'{BIN}/anvil',
        '--accounts',
        '1',
        '--balance',
        '1000',
        '--mnemonic',
        mnemonic,
        '--chain-id',
        CHAINID,
        '--rpc-url',
        'https://ethereum-sepolia-rpc.publicnode.com'
    ],
)

web3 = Web3(Web3.HTTPProvider(RPC_URL))
while True:
    if proc.poll() is not None:
        exit(1)
    if web3.is_connected():
        break
    sleep(0.1)

# Deployed beforehand on the sepolia testnet
contracts['Challenge'] = "0x685215B6aD89715Ef72EfB820C13BFa8E024401a"

# Gives ETH from the Deployer to the Player
faucet = subprocess.Popen(
    args=[
        f'{BIN}/cast',
        'send', 
        PLAYER_ADDRESS,
        '--value',
        PLAYER_ETH + 'ether',
        '--rpc-url',
        RPC_URL,
        '--private-key',
        deployer_key
    ],
)

app = Flask(__name__)

ALLOWED_NAMESPACES = ['web3', 'eth', 'net']

@app.route('/')
def index():
    return render_template('index.html', 
                           key=PLAYER_KEY, 
                           address=PLAYER_ADDRESS, 
                           challenge=contracts['Challenge'],
                           challname=CHALLNAME,
                           description=DESCRIPTION_HTML,
                           hardfork=HARDFORK.title(),
                           chainid=CHAINID
                        )

# proxies requests to the blockchain after parsing it
@app.route('/rpc', methods=['POST'])
def rpc():
    body = request.get_json()

    allowed = (
        any(body['method'].startswith(namespace)
            for namespace in ALLOWED_NAMESPACES)
        and body['method'] != 'eth_sendUnsignedTransaction'
    )

    if allowed:
        resp = requests.post(RPC_URL, json=body)
        response = Response(resp.content, resp.status_code,
                            resp.raw.headers.items())
        return response

    abort(403)

@app.route('/flag')
def flag():
    solve_proc = subprocess.run([
        f'{BIN}/cast',
        'call',
        contracts['Challenge'],
        'lastSolver()(address)',
        '--rpc-url',
        RPC_URL
    ], stdout=subprocess.PIPE)

    lastSolver = solve_proc.stdout.decode().strip()

    if lastSolver == PLAYER_ADDRESS:
        return FLAG
    else:
        return choice(CHALL_NOT_SOLVED_MESSAGES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
