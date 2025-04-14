// Author : Neoreo
// Difficulty : Medium

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract Sublocku {

    uint private size;
    uint256[][] private game;
    bool public isSolved = false;

    address public owner;
    address public lastSolver;


    constructor(uint256 _size,uint256[][] memory initialGrid) {
        owner = msg.sender;
        size = _size;
        require(initialGrid.length == size, "Grid cannot be empty");
        for (uint i = 0; i < size; i++) {
            require(initialGrid[i].length == size, "Each row must have the same length as the grid");
        }
        game = initialGrid;
    }


    function unlock(uint256[][] memory solve) public {

        require(solve.length == size, "Solution grid size mismatch");
        for (uint i = 0; i < size; i++) {
            require(solve[i].length == size, "Solution grid row size mismatch");
        }

        for (uint i = 0; i < size; i++) {
            for (uint j = 0; j < size; j++) {
                if (game[i][j] != 0) {
                    require(game[i][j] == solve[i][j], "Cannot modify initial non-zero values");
                }
            }
        }

        require(checkRows(solve),    "Row validation failed");
        require(checkColumns(solve), "Column validation failed");
        require(checkSquares(solve), "Square validation failed");
        lastSolver = tx.origin;
    }

    function checkRows(uint256[][] memory solve) private view returns (bool){
        uint256[] memory available;
        uint256 val;
        for (uint i = 0; i < size; i++) {
            available = values();
            for (uint j = 0; j < size; j++) {
                val = solve[i][j];
                if (val <= 0 || val > size){
                    return false;
                }   
                if (available[val-1] == 0){
                    return false;
                }
                available[val-1] = 0;
            }
            if (sum(available) != 0) {
                return false;
            }
        }
        return true;
    }


    function checkColumns(uint256[][] memory solve) private view returns (bool){
        uint256[] memory available;
        uint256 val;
        for (uint i = 0; i < size; i++) {
            available = values();
            for (uint j = 0; j < size; j++) {
                val = solve[j][i];
                if (val <= 0 || val > 9){
                    return false;
                }   
                if (available[val-1] == 0){
                    return false;
                }
                available[val-1] = 0;
            }

            if (sum(available) != 0) {
                return false;
            }
        }
        return true;
    }

    function checkSquares(uint256[][] memory solve) private view returns (bool) {
        uint256[] memory available;
        uint256 val;

        for (uint startRow = 0; startRow < size; startRow += 3) {
            for (uint startCol = 0; startCol < size; startCol += 3) {
                available = values();

                for (uint i = 0; i < 3; i++) {
                    for (uint j = 0; j < 3; j++) {
                        val = solve[startRow + i][startCol + j];
                        if (val <= 0 || val > 9) {
                            return false;
                        }
                        if (available[val-1] == 0) {
                            return false;
                        }
                        available[val-1] = 0;
                    }
                }

                if (sum(available) != 0) {
                    return false;
                }
            }
        }
        return true;
    }


    function values() internal pure returns (uint256[] memory){
        uint256[] memory available_values = new uint256[](9);
        available_values[0] = uint256(1);
        available_values[1] = uint256(2);
        available_values[2] = uint256(3);
        available_values[3] = uint256(4);
        available_values[4] = uint256(5);
        available_values[5] = uint256(6);
        available_values[6] = uint256(7);
        available_values[7] = uint256(8);
        available_values[8] = uint256(9);
        return available_values;
    }

    function sum(uint256[] memory array) internal pure returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < array.length; i++) {
            total += array[i];
        }
        return total;
    }
}
