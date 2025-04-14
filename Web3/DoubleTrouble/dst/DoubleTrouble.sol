// Author : Neoreo
// Difficulty : Hard

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract DoubleTrouble {
    bool public isSolved = false;
    mapping(address => bool) public validContracts;

    function validate(address _contract) public  {
        uint256 size;
        assembly {
            size := extcodesize(_contract)
        }
        if (size == 0 || size > 5) {
            revert("Invalid contract");
        }
        validContracts[_contract] = true;
    }

    function flag(address _contract) public {
        require(validContracts[_contract], "Given contract has not been validated");

        uint256 size;
        assembly {
            size := extcodesize(_contract)
        }
        bytes memory code = new bytes(size);
        assembly {
            extcodecopy(_contract, add(code, 0x20), 0, size)
        }
        bytes memory keyBytecode = hex"1f1a99ed17babe0000f007b4110000ba5eba110000c0ffee";
        
        require(keccak256(code) == keccak256(keyBytecode),"Both bytecodes don't match");

        isSolved = true;
    }

}
