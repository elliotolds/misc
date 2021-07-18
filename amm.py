

#!/usr/bin/env python2.7.6

import random
import sys
import datetime
import numpy
import math

def runSim(myFunds, price, fee, steps):
	
		
	numETH = (myFunds/2)/price
	numUSDC = (myFunds/2)

	initialPrice = price

#	print "numETH is " + str(numETH)
#	print "numUSDC is " + str(numUSDC)
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
	loss = fiftyValue - endValue

	print "Upsteps: " + str(upsteps)
	print "Downsteps: " + str(downsteps)		
	print "Ending price is " + str(price)
	print "Ending AMM value is " + str(endValue)
#	print "If AMM had just held ETH, value would be " + str(hodlValue)
#	print "If AMM had just held USDC, value would be " + str(myFunds)
	print "If AMM had just done 50/50, value would be " + str(fiftyValue)
	print "Impermanent loss was " + str(loss)
	print "Total fees is " + str(totalfees)

	if totalfees > loss:
		print "WORTH IT"
	else:
		print "REKT"
		
	print ""
		
	return [int((totalfees - loss)/1000), int((endValue + totalfees)/1000)]



if len(sys.argv) != 6:
  print "Needs 5 args: myContribution, current price, fee, steps, outersteps"
  exit()
  
myFunds = float(sys.argv[1])
price = float(sys.argv[2])
fee = float(sys.argv[3])
steps = float(sys.argv[4])
outersteps = float(sys.argv[5])

j = 0

OFFSET = 20000
histogram = []
histogram = [0 for i in range(OFFSET + OFFSET)]

abshistogram = []
abshistogram = [0 for i in range(OFFSET + OFFSET)]

while j < outersteps:
	vals = runSim(myFunds, price, fee, steps)
	val = vals[0]
	print "step " + str(j) + ".. trying to write hisogram value to " + str(val + OFFSET)
	histogram[val + OFFSET] = histogram[val + OFFSET] + 1	
	absval = vals[1]
	abshistogram[absval] = abshistogram[absval] + 1 
	j = j + 1

totalgain = 0
j = 0
lostmoney = 0
while j < OFFSET + OFFSET:
	if histogram[j] > 0:
		print str(j - OFFSET) + " --> " + str(histogram[j])
		totalgain = totalgain + (j - OFFSET) * histogram[j]
		if j - OFFSET < 0:
			lostmoney = lostmoney + 1
	j = j + 1	
	
print ""

j = 0
lostabsmoney=0
totalabscash = 0

while j < OFFSET + OFFSET:
	if abshistogram[j] > 0:
		print str(j) + " --> " + str(abshistogram[j])
		totalabscash = totalabscash + j * abshistogram[j]
		if  j < myFunds/1000:
			lostabsmoney = lostabsmoney + 1
	j = j + 1	

print "Average IL gain is " + str(totalgain/outersteps)
print "Lost IL money in this many cases: " + str(lostmoney)
print "Average absolute cash is " + str(totalabscash/outersteps)
print "Lost absolute money in this many cases: " + str(lostabsmoney)

