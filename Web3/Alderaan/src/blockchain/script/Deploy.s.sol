// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import {Alderaan} from "../src/Alderaan.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    Alderaan public challenge;
    
    function run() public {
        vm.startBroadcast();

        Alderaan challenge = new Alderaan{value: 1 ether}();
        console.log("Challenge deployed at :", address(challenge));

        vm.stopBroadcast();
    }
}
