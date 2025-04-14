// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Transient2 {
    constructor() {
        bytes memory bytecode = hex"1f1a99ed17babe0000f007b4110000ba5eba110000c0ffee";
        assembly {
            return (add(bytecode, 0x20), mload(bytecode))
        }
    }
}

