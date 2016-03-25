#!/usr/bin/env python2.7.6

# This script implements the selfish mining algorithm as described by Sirer and Eyal in
# https://www.cs.cornell.edu/~ie53/publications/btcProcFC.pdf
#
# It has been modified to show the effect of head-first mining.
# See the parts of the code referring to either 'benefit' or 'blockOnOurHeaderExists' for
# how head-first mining changes the calculation

import random
import sys

# How much does it help to waste everyone else's time by publishing a header without
# following it up? 
# benefit = 0.05 corresponds to a ~30 second period before miners give up on mining our 
# block header. It means that it's 5% more likely that we'll find the next block.
benefit = 0.05  

# print the number of selfish blocks won, and total blocks
def simulate(alpha, gamma, n): 
    state = 0 # what state we're in (states are defined in the pdf above)
    stash = 0 # how many blocks we're hiding in our private chain
    chainLen = 0 # length of public chain
    wins = 0 # how many times the selfish miners won a block (accepted by everyone)

    blockOnOurHeaderExists = False

    while chainLen < n:
        r = random.random()
        if state == 0: #initial state
            blockOnOurHeaderExists = False
            if r <= alpha:
                stash += 1
                assert stash == 1
                state = 1
                # If we find a block, immediately publish a header and waste N seconds of other people's time.
                # We calculate the benefit to ourselves of others wasting time below in state 1.
                # Here we figure out if someome else finds a block on our header in those 30 seconds
                r2 = random.random()
                if r2 < (1 - alpha) * benefit: 
                    blockOnOurHeaderExists = True 
            else:
                chainLen += 1
        elif state == -1: # 0' in the paper.. we had one hidden block but a public block was just published
            # We start by publishing our one block.. now we work to extend it..
            if blockOnOurHeaderExists:
                wins += 1 # Someone had a block built on the block we just published. 
                          # Now everyone will try to extend that chain.
            elif r <= alpha: # we found another block, publish it immediately
                wins += 2
            elif r <= alpha + gamma * (1 - alpha): # Someone else found a block on our initial block
                wins += 1
            # Else someone else found a second block ontop of the block that wasn't ours. Start over.                  
            state = 0
            stash = 0
            chainLen += 2                   
        elif state == 1:
            # We have one secret block. We get a benefit to find another because we wasted people's time
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
            else: # We had two secret blocks, but someone else just found one. 
                  # So we want to publish both of our blocks immediately.
                state = 0
                if stash == 2 and blockOnOurHeaderExists: 
                    # In this situation, another miner is tied with us because he built
                    # on our previous header. So we need to see who wins the race.
                    if random.random() <= gamma:
                        wins += 2 # We win, and get rewards for our earlier header, and the new block
                    else:
                        wins += 1 # Other miner built on our header, but he wins this block
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
    gamma = float(sys.argv[2]) # % of races we win when we publish a block at the same time as someone else
    nBlocks = 10**float(sys.argv[3]) # number of blocks to simulate expressed as power of 10
    simulate(alpha, gamma, nBlocks)


main()
