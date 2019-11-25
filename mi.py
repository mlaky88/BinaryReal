#!/usr/bin/env python # -*- coding: UTF-8 -*-

import cgi
import cgitb
import math
import string

InputFilename = 'signals.txt'

# MI(X,Y) = 1/N Sum_i,j c(x=Xi,y=Yj) * (log2(N) + log2(c(x=Xi,y=Yj) / (c(x=Xi) * c(y=Yj))))
def info_orig(x, y):
	if len(x) != len(y):
		print 'mutual_info(x,y): x and y must be the same length, but are not'
		print 'len(x) =', len(x), ', len(y) =', len(y)
		exit()
	n = len(x)
	n_inv = 1.0 / n
	x_counts = dict()
	y_counts = dict()
	xy_counts = dict()
	for i in range(n):
		xi = x[i]
		yi = y[i]
		xyi = (x[i], y[i])
		if xi in x_counts.keys():
			x_counts[xi] += 1.0
		else:
			x_counts[xi] = 1.0
		if yi in y_counts.keys():
			y_counts[yi] += 1.0
		else:
			y_counts[yi] = 1.0
		if xyi in xy_counts.keys():
			xy_counts[xyi] += 1.0
		else:
			xy_counts[xyi] = 1.0
	mi = 0.0
	for xyi in xy_counts.keys():
		xi, yi = xyi
		log_term = n * xy_counts[xyi] / (x_counts[xi] * y_counts[yi])
		mi_term = xy_counts[xyi] * math.log(log_term, 2)
		#print '[%g,%g]: n=%g xc=%g yc=%g xyc=%g lt=%g mit=%g' % (xi, yi, n, x_counts[xi], y_counts[yi], xy_counts[xyi], log_term, mi_term)
		mi += mi_term
	mi = mi * n_inv
	hx = 0.0
	for xi in x_counts.keys():
		hx -= x_counts[xi] * math.log(x_counts[xi] * n_inv, 2)
	hx = hx * n_inv
	hy = 0.0
	for yi in y_counts.keys():
		hy -= y_counts[yi] * math.log(y_counts[yi] * n_inv, 2)
	hy = hy * n_inv

	return mi, hx, hy

# MI(X,Y) = log2(N) + 1/N Sum_i,j c(x=Xi,y=Yj) * (log2(c(x=Xi,y=Yj)) - log2(c(x=Xi)) - log2(c(y=Yj)))
def info(x, y):
	if len(x) != len(y):
		print 'mutual_info(x,y): x and y must be the same length, but are not'
		print 'len(x) =', len(x), ', len(y) =', len(y)
		exit()
	n = len(x)
	n_inv = 1.0 / n
	x_counts = dict()
	y_counts = dict()
	xy_counts = dict()
	for i in range(n):
		xi = x[i]
		yi = y[i]
		xyi = (x[i], y[i])
		if xi in x_counts.keys():
			x_counts[xi] += 1.0
		else:
			x_counts[xi] = 1.0
		if yi in y_counts.keys():
			y_counts[yi] += 1.0
		else:
			y_counts[yi] = 1.0
		if xyi in xy_counts.keys():
			xy_counts[xyi] += 1.0
		else:
			xy_counts[xyi] = 1.0
        print x_counts
        print y_counts
        print xy_counts
	mi = 0.0
	for xyi in xy_counts.keys():
		xi, yi = xyi
		log_term_1 = math.log(xy_counts[xyi], 2)
		log_term_2 = math.log(x_counts[xi], 2)
		log_term_3 = math.log(y_counts[yi], 2)
		log_term = log_term_1 - log_term_2 - log_term_3
		mi_term = xy_counts[xyi] * log_term
		#print '[%g,%g]: n=%g xc=%g yc=%g xyc=%g lt=%g mit=%g' % (xi, yi, n, x_counts[xi], y_counts[yi], xy_counts[xyi], log_term, mi_term)
		mi += mi_term
	mi = mi * n_inv + math.log(n, 2)
	hx = 0.0
	for xi in x_counts.keys():
		hx -= x_counts[xi] * math.log(x_counts[xi] * n_inv, 2)
	hx = hx * n_inv
	hy = 0.0
	for yi in y_counts.keys():
		hy -= y_counts[yi] * math.log(y_counts[yi] * n_inv, 2)
	hy = hy * n_inv

	return mi, hx, hy


def read_signals(input_file):
	signals = list()
	for line in input_file:
		if ':' in line:
			signal_name = line[:line.find(':')]
			signal_strings = string.split(line[len(signal_name)+2:])
			signal_floats = list()
			for value in signal_strings:
				signal_floats.append(float(value))
			signals.append((signal_name, signal_floats))
	return signals



def print_mi(signals, avoid, succinct):
        
	if succinct:		
		for signal in signals:
			print '%s:' % (signal[0])
			for value in signal[1]:
				print ' ' + value,
			
	for i in range(len(signals)):
		for j in range(i+1, len(signals)):
			x = signals[i]
			y = signals[j]
			if not avoid or x[0][0] != y[0][0]:  # only cross signals with different leading characters
                                print ("Doing {} and {}".format(x[1],y[1]))
				mi, hx, hy = info(x[1], y[1])
				h_max = max(hx, hy)
				h_avg = 0.5 * (hx + hy)
				h_sqr = math.sqrt(hx * hy)
				h_min = min(hx, hy)
				h_red = math.pow(2, hx + hy)
				nmi_max = float('inf') if h_max == 0.0 else mi / h_max
				nmi_avg = float('inf') if h_avg == 0.0 else mi / h_avg
				nmi_sqr = float('inf') if h_sqr == 0.0 else mi / h_sqr
				nmi_min = float('inf') if h_min == 0.0 else mi / h_min
				nmi_pow = mi / h_red
				if succinct:
					print '%s,%s: MI=%7.5f, H(%s)=%7.5f, H(%s)=%7.5f, NMI_max=%7.5f, NMI_avg=%7.5f, NMI_sqr=%7.5f, NMI_min=%7.5f, NMI_pow=%7.5f\n</p>' % \
						  (x[0], y[0], mi, x[0], hx, y[0], hy, nmi_max, nmi_avg, nmi_sqr, nmi_min, nmi_pow)
				else:
					x_space = ''
					y_space = ''
					print '%s%s:' % (x_space, x[0]),
					for value in x[1]:
						print ' ' + str(value),
					print ''
					print '%s%s:' % (y_space, y[0]),
					for value in y[1]:
						print ' ' + str(value),
					
					x_space = ''
					y_space = ''
					print 
					print 'H(%s)%s = %g' % (x[0], x_space, hx)
					print 'H(%s)%s = %g' % (y[0], y_space, hy)
					print 'MI = %g' % mi
					print 'NMI_max = %g' % (nmi_max)
					print 'NMI_avg = %g' % (nmi_avg)
					print 'NMI_sqr = %g' % (nmi_sqr)
					print 'NMI_min = %g' % (nmi_min)
					print 'NMI_pow = %g' % (nmi_pow)

def main():
	avoid = False
	succinct = False
	f = open(InputFilename, "r")
	signals = read_signals(f)
	print_mi(signals, avoid, succinct)



def multi_entropy(X, log_base, debug = False):
    	"""
	Calculate the entropy of a random variable
	"""
	# Variable to return entropy
	n_cols = len(X)
	summation = 0.0
	# Get uniques values of random variables
	values_x = set(X)
	# Print debug info
	if debug:
		print 'Entropy of'
		print X
	# For each random
	for value_x in values_x:
		px = float(shape(where(X==value_x))[1]) / n_cols
		if px > 0.0:
			summation += px * math.log(px, log_base)
		if debug:
			print '(%d) px:%f' % (value_x, px)
	if summation == 0.0:
		return summation
	else:
		return - summation


def single_entropy(X, log_base, debug = False):
	"""
	Calculate the entropy of a random variable
	"""
	# Variable to return entropy
	n_cols = len(X)
	summation = 0.0
	# Get uniques values of random variables
	values_x = set(X)
	# Print debug info
	if debug:
		print 'Entropy of'
		print X
	# For each random
	for value_x in values_x:
		px = float(shape(where(X==value_x))[1]) / n_cols
		if px > 0.0:
			summation += px * math.log(px, log_base)
		if debug:
			print '(%d) px:%f' % (value_x, px)
	if summation == 0.0:
		return summation
	else:
		return - summation


def mutual_information(X, Y, log_base, debug = False):
	
	"""
	Calculate and return Mutual information between two random variables
	"""
	# Check if index are into the bounds
	n_cols = len(X)
	# Variable to return MI
	summation = 0.0
	# Get uniques values of random variables
	values_x = set(X)
	values_y = set(Y)
	# Print debug info
	if debug:
		print 'MI between'
		print X
		print Y
	# For each random
	for value_x in values_x:
		for value_y in values_y:
			#print(shape(where(X==value_x))[1])
			#print(shape(where(Y==value_y))[1])
			px = float(shape(where(X==value_x))[1]) / n_cols
			py = float(shape(where(Y==value_y))[1]) / n_cols
			pxy = float(len(where(in1d(where(X==value_x)[0],where(Y==value_y)[0])==True)[0])) / n_cols
			if pxy > 0.0:
				summation += pxy * math.log((pxy / (px*py)), log_base)
				print(math.log((pxy / (px*py)), log_base))
			if debug:
				print '(%d,%d) px:%f py:%f pxy:%f' % (value_x, value_y, px, py, pxy)
	return summation

from numpy import array, shape, where, in1d

def test():
    	
	print(mutual_information(array([0,0,1,1,0,0,1,1]),array([0,1,1,1,1,1,0,1]),2,True))
	exit(1)
	import csv
	from sklearn.feature_selection import *
	X = []
	with open('Data/weka-discrete/vehicle-train-processed.arff') as csv_file:
		reader= csv.reader(csv_file, delimiter=',')
		for row in reader:
    			rr = []
			for v in row:
				rr.append(int(v))
			X.append(rr)
		#print X

		
		Y = [row[17] for row in X]
		

		for i in range(18):
			Xi = [row[i] for row in X]
			print("F{}-F{}".format(i+1,18)),
			mi = mutual_information(array(Xi),array(Y),2)
			se = single_entropy(array(Xi),2,False)
			print(mi,se)



exit(1)
test()
#main()
