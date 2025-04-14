// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Transient1 {
    constructor() {
        bytes memory bytecode = hex"33ff"; // caller; selfdestruct;
        assembly {
            return (add(bytecode, 0x20), mload(bytecode))
        }
    }
}