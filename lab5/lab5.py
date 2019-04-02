"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 5
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 4/1/2019
Date of last modification: 4/1/2019

Purpose of program: 

To create a basic foundation of a natural language processing(nlp) program that finds the similarity between two words. 
This is done by calculating the cosine simularity by having the dot product of the embeddings divided by the magnitude of the two embeddings. 
Then, to either build a binary search tree(bst) or hashtable based on the user's choice.
After the data structure is built, stats are shown along with runtimes of building it and querying for the words within it.
In order to run the program with multiple words, another word doc called words.txt is used to contains pairs.
"""
import numpy as np
import matplotlib.pyplot as plt
import math 
import random
import timeit
from operator import itemgetter
import statistics
import string
#################################################################################################
#HASHTABLE (CHAINING) CLASS
#################################################################################################
class HashTableC(object):
	# Builds a hash table of size 'size'
	# Item is a list of (initially empty) lists
	# Constructor
	def __init__(self, size,num_items = 0):  
		self.item = []
		self.num_items = 0	#num_items: Counts new item so to not recalculate load factor
		
		for i in range(size):
			self.item.append([])
	
#resize_h: Resizes the table if the loadfactor is 1 or over
#Increases table by making it twice as big plus 1
def resize_h(H):
	for i in range((2 * len(H.item)) + 1):
		H.item.append([])
		
	return H
	
def InsertC(H,k,l):
	# Inserts k in appropriate bucket (list) 
	# Does nothing if k is already in the table
	H.num_items +=1
	if H.num_items / len(H.item) > 1.0:
		H = resize_h(H)
	b = h(k,len(H.item))
	H.item[b].append([k,l]) 

def FindC(H,k):
	# Returns bucket (b) and index (i) 
	# If k is not in table, i == -1
	
	b = h(k,len(H.item))
	for i in range(len(H.item[b])):
		if H.item[b][i][0] == k:
			return b, i, H.item[b][i][1]
	return b, -1, -1
 
def h(s,n):
	r = 0
	for c in s:
		#print(c)
		r = (r*n + ord(c))% n
	return r

def loadfactor(H):
	count = 0
	for i in range(len(H.item)):	#If the list is not empty then add all elements in the count
		if H.item[i] != []:
			count +=  len(H.item[i])
	return count / len(H.item)		#Return num of elements over length of list since it is chaining
		
def per_emp_l(H):
	count = 0
	
	#If the list is empty then add one to count
	for i in range(len(H.item)):	
		if H.item[i] == []:
			count += 1
	#Return num of empty lists over table size times 100 to get percentage
	return (count / len(H.item)) * 100
	

def std_dev(H):
	a = []
	
	#Get length of each slot in the table and append to list s
	for i in range(len(H.item)):
		a.append(len(H.item[i]))

	#Python statistics method (sample) to get stddev
	return statistics.stdev(a)

def debug_h(A, w):
	orig_size = 11
	H = HashTableC(orig_size)

	print("Building hash table with chaining \n")

	for i in range(len(A)):
		InsertC(H,A[i][0], A[i][1])
		#print(H.item)
	
	print("Hash table stats: \n" 
	+ "Initial table size: " + str(orig_size) + "\n"
	+ "Final table size: " + str(len(H.item)) + "\n" 
	+ "Load factor: " + str(loadfactor(H)) + "\n"
	+ "Percentage of empty lists: " + str(per_emp_l(H)) + "\n"
	+ "Standard deviation of the lengths of the lists: " + str(std_dev(H)) + "\n"
	)
	
	#Processes words.txt to run many similarities
	start = timeit.default_timer()
	for i in range(len(w)):
		e0 = FindC(H, w[i][0])[2]
		e1 = FindC(H, w[i][1])[2]
		
		if e0 == -1 or e1 == -1:
			print("No word found")
		
		else:
			print("Similarity [" + str(w[i][0]) + "," + str(w[i][1]) + "] = " + str(c_sim(e0,e1)))
		
	stop = timeit.default_timer()
	print('Running time for hash table query processing:: ', stop - start)


#################################################################################################
#BINARY SEARCH TREE CLASS
#################################################################################################
class BST(object):
	# Constructor
	def __init__(self, item, left=None, right=None):  
		self.item = item
		self.left = left 
		self.right = right		  
		
def Insert(T,newItem):
	if T == None:
		T = BST(newItem)
	elif T.item > newItem:
		T.left = Insert(T.left,newItem)
	else:
		T.right = Insert(T.right,newItem)

	return T 

def Find(T,k):
	# Returns the address of k in BST, or None if k is not in the tree

	while T is not None:
		if T.item[0] == k:
			return T.item
		elif T.item[0] < k:
			T = T.right
		else:
			T = T.left
	return -1

def height(T):
	if T is None:
		return -1
	return max(height(T.left) , height(T.right)) + 1
	
def num_nodes(T):
	if T is None:
		return 0
	else:
		return num_nodes(T.left) + num_nodes(T.right)  + 1
	
def slist_to_bst(L):
	if not L:
		return None
	#If there is only 1 element then the bst is already balanced
	if len(L) == 1:
		T = BST(L[0])
		return T
	
	mid = (len(L)) // 2		#mid: Middle element/median of sorted list
	T = BST(L[mid])			#Make mid the root 
	
	#From start until middle of the list, add the middle element for the left subtree
	T.left = slist_to_bst(L[:mid])			
	
	#From mid plus until end of the list, add the middle element for the righ subtree
	T.right = slist_to_bst(L[(mid+1):])		
	return T

def debug_bst(A,w):
	# Code to test the functions above
	start = timeit.default_timer()	
	print("Building binary search tree \n")
	T = slist_to_bst(A)
	stop = timeit.default_timer()
	
	
	print("Binary Search Tree stats: \n" 
	+ "Number of nodes: " + str(num_nodes(T)) + "\n"
	+ "Height: " + str(height(T)) + "\n"
	+ "Running time for binary search tree construction: " + str(stop-start) + "\n" 
	)
	
	#Processes words.txt to run many similarities
	start = timeit.default_timer()	
	for i in range(len(w)):
		
		e0 = Find(T,w[i][0])
		e1 = Find(T, w[i][1])
		if e0 == -1 or e1 == -1:
			print ("No words found")
			
		else:
			print("Similarity [" + str(w[i][0]) + "," + str(w[i][1]) + "] = " + str(c_sim(e0[1],e1[1])))
	
	stop = timeit.default_timer()
	print('Running time for binary search tree query processing: ', stop - start)


#################################################################################################
#LAB METHODS
#################################################################################################
def c_sim(e0, e1):
	#numpy function dot does the dot product of the embeddings (2 lists)
	if e0 == None or e1 == None:
		return 0.0
	
	dp = np.dot(e0, e1)

	#linalg.norm function is a numpy function that gets the magnitude of the embeddings(a vector)
	me0 = np.linalg.norm(e0)
	me1 = np.linalg.norm(e1)
	return dp / (me0 * me1)


def file_reader(filename,option):
	lfile = []

	#with is used to open and close the file once it is done reading
	#encoding is utf8 due to errors being generated if it is the wrong filetype
	with open(filename,"r",encoding="utf8") as f:
		for line in f:
			#Appends the string and a list(the embedding)
			#Uses map to convert string to float numbers and to only put in the numbers(excludes the string)

			if option == 'g':
				if line.split()[0] not in string.punctuation:	#Skips line if its punctuation
					lfile.append([line.split()[0], list(map(float,line.split()[1:]))] )
	
			if option == 't':
				l = line.split(',')
				lfile.append([l[0], l[1]])
	return lfile

def print_sim(w0,w1):
	print("Similarity [" + str(w0[0]) + "," + str(w1[0]) + "] = " + str(c_sim(w0[1],w1[1])))

#################################################################################################
#MAIN
#################################################################################################

fng = "glove.6B.50d.txt"
fnt = "words.txt"
print ("Reading " + fng + "...\n")
l = file_reader(fng,'g')

try:
	print("Choose table implementation: \n" 
	+ "1. Binary Search Tree\n"
	+ "2. Hash Table(Chaining)\n")
	choice = int(input())

	print ("Reading " + fnt + "...\n")
	w = file_reader(fnt,'t')

	#Binary Search Tree
	if choice == 1:
		#Sorts 2d based on alpha order so that it can be put into bst
		l.sort(key=itemgetter(0))	#Sort will only sort with first index of each column(a string) as the guideline 
		debug_bst(l,w)

	#Hash table
	elif choice == 2:
		debug_h(l,w)

	else:
		print("Incorrect Choice")

except ValueError:
	print ("Incorrect input")
