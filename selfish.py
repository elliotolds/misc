#!/usr/bin/env python2.7.6

import random
import sys

benefit = 0.05 # how much does it help to waste 30 seconds of everyone else's time?  

# print the number of selfish blocks won, and total blocks
def simulate(alpha, gamma, n): 
    state = 0 # what state we're in
    stash = 0 # how many blocks we're hiding
    chainLen = 0 # length of public chain
    wins = 0 # how many times the selfish miners won

    lengthTwoChainExists = False

    while chainLen < n:
        r = random.random()
        if state == 0: #initial state
            lengthTwoChainExists = False
            if r <= alpha:
                stash += 1
                assert stash == 1
                state = 1
                # If we find a block, immediately publish a header and waste 30 seconds of other people's time
                # We need to figure out if someome else finds a block on our header in those 30 seconds
                r2 = random.random()
                if r2 < (1 - alpha) * benefit: 
                    lengthTwoChainExists = True
            else:
                chainLen += 1
        elif state == -1: # 0' in the paper.. we had one hidden block but a public block was just published
            # We start by publishing our one block.. now we work hard to extend it..
            if lengthTwoChainExists:
                wins += 1 # Someone had a block built on our block in waiting.. 
            elif r <= alpha: # we found a block, publish it immediately
                wins += 2
            elif r <= alpha + gamma * (1 - alpha): #        they found a block on our block
                wins += 1
            #else they found a block on their block.. start over..                  
            state = 0
            stash = 0
            chainLen += 2                   
        elif state == 1:
            if r <= alpha * (1 + benefit):
                state = 2
                stash += 1
                assert stash == 2
            else:
                state = -1
        elif state == 2:
            if r <= alpha:
                state += 1
                stash += 1
            else: # publish both ASAP.... 
                state = 0
                if stash == 2 and lengthTwoChainExists: #See if the other miner wins the race
                    if random.random() <= gamma:
                        wins += 2 # We win the race
                    else:
                        wins += 1 # Other miner built on our block, but he wins
                else:
                    wins += stash
                chainLen += stash
                stash = 0
        else: # state is >= 3
            if r <= alpha:
                state += 1
                stash += 1      
            else:
                state -= 1

    print "Chain length: ", chainLen
    print "Blocks we won: ", wins
    print "Our win rate: ", float(wins)/chainLen
    print "Theoretical rate: ", (alpha * (1 - alpha)**2 * (4*alpha + gamma * (1 - 2*alpha)) - alpha**3)/(1 - alpha * (1 + (2 - alpha)*alpha))


def main():
    alpha = float(sys.argv[1]) # our fraction of total hash rate
    gamma = float(sys.argv[2]) # % of races we win
    nBlocks = 10**float(sys.argv[3]) # number of blocks to simulate expressed as power of 10
    simulate(alpha, gamma, nBlocks)


main()
