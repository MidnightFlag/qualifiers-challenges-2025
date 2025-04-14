// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CreateFactory {
    event ContractDeployed(address indexed deployedContract);

    function deploy(uint256 amount, bytes memory bytecode) public returns (address deployedContract) {
        assembly {
            deployedContract := create(amount, add(bytecode, 0x20), mload(bytecode))
        
            if iszero(deployedContract) {
                revert(0, 0)
            }
        }
        
        emit ContractDeployed(deployedContract);
    }

    function destroy() public{
        selfdestruct(payable(msg.sender));
    }
}