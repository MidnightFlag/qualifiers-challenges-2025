#!/bin/bash

# Quick and dirty script to solve the challenge
export RPC=http://localhost/rpc                                                                      
export PK=cdf7d2500c92f02e20a03ad656b503cfa611df7dc9bdfcde5c5ac88703e8f215                                                                                                                                                                                                 
export TARGET=0x685215B6aD89715Ef72EfB820C13BFa8E024401a   
cast send $TARGET "unlock(uint256[][])" '[[3, 1, 7, 4, 9, 5, 6, 8, 2],[9, 2, 6, 3, 1, 8, 7, 5, 4],[5, 4, 8, 7, 2, 6, 3, 1, 9],[4, 3, 1, 8, 5, 7, 9, 2, 6],[6, 9, 2, 1, 3, 4, 8, 7, 5],[8, 7, 5, 9, 6, 2, 4, 3, 1],[7, 8, 9, 5, 4, 1, 2, 6, 3],[1, 6, 4, 2, 8, 3, 5, 9, 7],[2, 5, 3, 6, 7, 9, 1, 4, 8]]' -r $RPC --private-key $PK