

#!/usr/bin/env python2.7.6

import random
import sys
import datetime
import numpy
import math

# compute whether it's worth it to be an AMM, assuming a geometric random walk in price and no drift

# Run one simulation beginning with myFunds money, an ETH price, an AMM fee, and a number of random price movement steps
 
def runSim(myFunds, price, fee, steps, stepsize):
			
	numETH = (myFunds/2)/price
	numUSDC = (myFunds/2)

	initialPrice = price
	marketPrice = price
	ammPrice = price

	k = numETH * numUSDC # k is the constant for the AMM
	totalfees = 0 # total amount of fees collected over all the steps
	i = 1

	upsteps = 0
	downsteps = 0

	while i <= steps:
		if random.random() < 0.5: # price decrease
			downsteps = downsteps + 1 
			marketPrice = marketPrice * (1-stepsize)
			if marketPrice < ammPrice / (1+fee):
				#arbitrage opportunity.. buy ETH on the market and sell to the AMM until ammPrice / (1+fee) equals market price
				ammPrice = marketPrice * (1+fee)
				newUSDC = math.sqrt(ammPrice*k)
				newETH = k / newUSDC
				totalfees = totalfees + (newETH - numETH) * marketPrice * fee #sell the fee ETH on the market immediately for the new price	
				numETH = newETH
				numUSDC = newUSDC		
			
		else: # price increase
			upsteps = upsteps + 1 # sent in USDC, got out ETH
			marketPrice = marketPrice * (1+stepsize)
			if marketPrice > ammPrice * (1+fee):
				#arbitrage opportunity.. buy ETH from the AMM and sell to the market until ammPrice * (1+fee) equals market price
				ammPrice = marketPrice / (1+fee)
				newUSDC = math.sqrt(ammPrice*k)
				newETH = k / newUSDC
				totalfees = totalfees + (newUSDC - numUSDC) * fee 
				numETH = newETH
				numUSDC = newUSDC		

		i=i+1
			
			
	endValue = numUSDC + marketPrice*numETH
	hodlValue = (myFunds/initialPrice) * marketPrice
	fiftyValue = marketPrice * (myFunds/2)/initialPrice + (myFunds/2)
	loss = fiftyValue - endValue

	#print "Upsteps: " + str(upsteps)
	#print "Downsteps: " + str(downsteps)		
	#print "Ending marketprice is " + str(marketPrice)
	#print "Ending ammPrice is " + str(ammPrice)
	#print "Ending AMM value is " + str(endValue)
#	print "If AMM had just held ETH, value would be " + str(hodlValue)
#	print "If AMM had just held USDC, value would be " + str(myFunds)
	#print "If AMM had just done 50/50, value would be " + str(fiftyValue)
	#print "Impermanent loss was " + str(loss)
	#print "Total fees is " + str(totalfees)

	#if totalfees > loss:
	#	print "WORTH IT"
	#else:
	#	print "REKT"
		
	#print ""
		
	#return a bucketized and scaled down pair of (impermanent loss plus fees, total assets)	
	return [int((totalfees - loss)/1000), int((endValue + totalfees)/1000)]



if len(sys.argv) != 7:
  print "Needs 6 args: myContribution, current price, fee, steps, stepsize, outersteps"
  exit()
  
myFunds = float(sys.argv[1])
price = float(sys.argv[2])
fee = float(sys.argv[3])
steps = float(sys.argv[4])
stepsize = float(sys.argv[5])
outersteps = float(sys.argv[6])

j = 0

#create a histogram of the impermanent loss, bucketed into thousands of dollars
OFFSET = 1000000
histogram = []
histogram = [0 for i in range(OFFSET + OFFSET)]

#create a histogram of the total asset value including fees, bucketed into thousands of dollars
abshistogram = []
abshistogram = [0 for i in range(OFFSET + OFFSET)]

while j < outersteps:
	vals = runSim(myFunds, price, fee, steps, stepsize)
	val = vals[0]
	print "outer step " + str(j) + ".. trying to write hisogram value to " + str(val + OFFSET)
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
			lostmoney = lostmoney + histogram[j]
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
			lostabsmoney = lostabsmoney + abshistogram[j]
	j = j + 1	

print "Average IL gain is " + str(totalgain/outersteps)
print "Lost IL money in this many cases: " + str(lostmoney)
print "Average absolute cash is " + str(totalabscash/outersteps)
print "Lost absolute money in this many cases: " + str(lostabsmoney)

