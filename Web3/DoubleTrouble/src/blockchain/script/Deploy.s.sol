// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

import {DoubleTrouble} from "../src/DoubleTrouble.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    DoubleTrouble public challenge;
    
    function run() public {
        vm.startBroadcast();

        challenge = new DoubleTrouble();
        console.log("Challenge deployed at :", address(challenge));

        vm.stopBroadcast();
    }
}
