

#!/usr/bin/env python2.7.6

# compute whether it's worth it to be an AMM, assuming a geometric random walk in price and no drift

import random
import sys
import datetime
import numpy
import math

if len(sys.argv) != 5:
  print "Needs 4 args: myContribution, current price, fee, steps"
  exit()
  
myFunds = float(sys.argv[1])
price = float(sys.argv[2])
fee = float(sys.argv[3])
steps = float(sys.argv[4])

numETH = (myFunds/2)/price
numUSDC = (myFunds/2)

initialPrice = price

print "numETH is " + str(numETH)
print "numUSDC is " + str(numUSDC)
#print "price is " + str(price)

k = numETH * numUSDC
totalfees = 0
i = 1

upsteps = 0
downsteps = 0

while i <= steps:
	if random.random() < 0.5:
		downsteps = downsteps + 1 # sent in ETH, got out USDC
		newprice = price * (1-fee)
		newUSDC = math.sqrt(newprice*k)
		newETH = k / newUSDC
		#midprice = (price + newprice) / 2
		totalfees = totalfees + (newETH - numETH) * newprice * fee #sell the fee ETH immediately for the new price
		
		
		
	else:
		upsteps = upsteps + 1 # sent in USDC, got out ETH
		newprice = price * (1+fee)
		newUSDC = math.sqrt(newprice*k)
		newETH = k / newUSDC
		totalfees = totalfees + (newUSDC - numUSDC) * fee 

	price = newprice
	numETH = newETH
	numUSDC = newUSDC

	i=i+1
		
		
endValue = numUSDC + price*numETH
hodlValue = (myFunds/initialPrice) * price
fiftyValue = price * (myFunds/2)/initialPrice + (myFunds/2)

print "Upsteps: " + str(upsteps)
print "Downsteps: " + str(downsteps)		
print "Ending price is " + str(price)
print "Ending AMM value is " + str(endValue)
print "If AMM had just held ETH, value would be " + str(hodlValue)
print "If AMM had just held USDC, value would be " + str(myFunds)
print "If AMM had just done 50/50, value would be " + str(fiftyValue)
print "Impermanent loss was " + str(fiftyValue - endValue)
print "Total fees is " + str(totalfees)

if totalfees > fiftyValue - endValue:
	print "WORTH IT"
else:
	print "REKT"

