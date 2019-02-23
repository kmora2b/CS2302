"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 2
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 2/22/2019
Date of last modification: 2/22/2019

Purpose of program: 
To implement the sorting algorithms to sort a singly linked list: quick, merge, bubble, and a modified version of quick sort. 
Then, after the list is sorted, a method called median will find the middle element in the sorted list.
The program will attempt to count the number of comparisions in each algorithm.

"""
import timeit
import random

#################################################################################################
#NODE CLASS
#################################################################################################
class Node(object):
	# Constructor
	def __init__(self, item, next=None):
		self.item = item
		self.next = next 

#################################################################################################
#LINKED LIST CLASS
#################################################################################################
class List(object):
	# Constructor
	def __init__(self): 
		self.head = None
		self.tail = None

def IsEmpty(L):
	return L.head == None

def append_list(L,x): 
	#Appends an item to the end of the list
	if IsEmpty(L):
		L.head = Node(x)
		L.tail = L.head

	else:
		L.tail.next = Node(x)
		L.tail = L.tail.next

def print_list(title,L):
	# Prints list L's items in order using a loop
	temp = L.head
	print(title)

	while temp is not None:
		print(str(temp.item), end=' ')
		temp = temp.next
	print()# New line 

#METHOD get_length: Gets the length of the linked list by counting the number of nodes within a while loop
def get_length(L):
	temp = L.head
	size_list = 0

	while temp is not None:
		size_list += 1
		temp = temp.next

	return size_list

#METHOD element_at: Finds the node reference with an index
def element_at(L,e):
	temp = L.head
	n = get_length(L)

	#If the index is out of bounds then return the head
	if e >= n :
		return L.head
	
	for i in range(n):
		if i == e:
			return temp
		temp = temp.next

#################################################################################################
#SORTING METHODS
#################################################################################################

#Num of comparisions for each algorithm
BCOUNT  =  0		#Bubble Sort
MCOUNT  =  0		#Merge Sort
QCOUNT  =  0		#Quick Sort
QMCOUNT =  0		#Modified Quick Sort

############################################Bubble Sort###########################################
def bubble_sort(L):
	global BCOUNT

	if L.head is None:
		return L
		
	i = L.head
	j = L.head.next
	
	#Stay in i while comparing with j until it hits none
	while i is not None:

		while j is not None:
			BCOUNT+=1
			
			if i.item > j.item:
				swap(i,j)
			
			j = j.next
		#move the i node to the next one
		i = i.next
		
		#j is assigned the ref to i
		j = i

	return L

############################################Merge Sort###########################################
def merge_sort(h):
	global MCOUNT

	if h is None or h.next is None:
		return h
	MCOUNT+=1
	L1, L2 = split_list(h)  #split the list into two different lists
	L1 = merge_sort(L1)		
	L2 = merge_sort(L2)	
	h = merge_list(L1,L2)

	return h

#Merges the left and right lists into a single list
def merge_list(L1,L2):
	temp = None

	#If the left list is empty then return the right list only
	if L1 is None:
		return L2

	#If the right list is empty then return the left list only
	if L2 is None:
		return L1

	#If the left list node value  is right list node value then append the 
	if L1.item <= L2.item:
		temp = L1
		temp.next = merge_list(L1.next,L2)
	else:
		temp = L2
		temp.next = merge_list(L1, L2.next)

	return temp

#Splits list into two halves based on the middle index
def split_list(L):
	l = L	#Left/ slow pointer
	r = L	#right/ fast pointer
	
	#If r is not none then shift r to the next node
	if r:
		r = r.next
	
	#While r is not none then shift r to the next node and if r is not none still then shift r again and l to the next node
	while r:
		r = r.next
		
		if r:
			r = r.next
			l = l.next

	#mid is the reference to the start of the right l
	mid = l.next
	l.next = None
	return L, mid

############################################Quick Sort###########################################

#Method quick_sort: Handles partition and pivot functions and is seperated for legibility
def quick_sort(L):
	quick_sort_pivot(L,0,get_length(L)-1)
	

#Method quick_sort_pivot: Based on the pivots position, will sort from the left and right 
def quick_sort_pivot(L, start, end):
	if start < end:
		global QCOUNT
		QCOUNT+=1
		
		pivot = partition(L,start,end)
		quick_sort_pivot(L,start,pivot-1)
		quick_sort_pivot(L,pivot+1,end)

#Method partition: moves elements to the left or right sublist based on if its less than or greather than the pivot
def partition(L,start,end):
	global QCOUNT
	l = start + 1						#Should initially start after pivot
	r = end	
	pivot = element_at(L,start).item	#pivot: is the start of the list
	fin = False							#fin: boolean flag that indicates that all elements in a list was sorted
	
	while not fin:
		#While the l pointer is behind then shift element to the left

		while l <= r and element_at(L,l).item <= pivot:
			l = l+1
			#QCOUNT+=1
			
		#While the r pointer is ahead then shift element to the right by one less
		while element_at(L,r).item >= pivot and r >= l:
			#QCOUNT+=1
			r = r-1
			
		#If r list less than pivot and l list more than pivot then partition is done
		if r < l:
			#QCOUNT+=1
			fin = True
		
		#Swap the l and r pointers in the list 
		else:
			swap(element_at(L,l), element_at(L,r))

	swap(element_at(L,start),element_at(L,r))

	return r

########################################Modified Quick  Sort#####################################
def mod_quick_sort(L,l,r,n):
	#Return the left point if the array is one element
	global QMCOUNT
	
	QMCOUNT+=1
	if l == r:
		return element_at(L,l)

	pivot = random.randint(l,r)			#Randomize the pivot between left and right point
	pivot = partition_r(L,l,r,pivot)	#Move pivot based on elements
	
	#If n is equal to pivot then return the element at n
	QMCOUNT+=1
	if n == pivot:
		return element_at(L,n)
		
	#If n is less than or greater than pivot then recurse one sublist
	QMCOUNT+=1
	if n < pivot:
		return mod_quick_sort(L,l,pivot-1,n)

	else:
		return mod_quick_sort(L,pivot+1,r,n)

#Modified partition that also swaps with a specified pivot index
def partition_r(L,l,r, pivot):
	pivot_val = element_at(L,pivot).item			#Value of the pivot
	swap(element_at(L,pivot),element_at(L,r))		#move pivot to the end
	temp = l										#Stores l temporarily
	fin = False										#flag that indicates that partition is done
	i = l											#Index to swap
	
	while i < r:
		if element_at(L,i).item < pivot_val:		#If i val is less than pivot then store moves
			swap(element_at(L,i), element_at(L,temp))
			temp+=1
		i+=1

	swap(element_at(L,r), element_at(L,temp))		#Swap store and r to place pivot appropriately
	return temp

#################################################################################################
#UTILITY METHODS
#################################################################################################
#Generate random ints and appeand to the list
def gen_rand_list(n):
	L = List()
	#Creates a python native list of size n with distinct elements
	r = random.sample(range(1000), n)

	for i in range(n):
		#Append the r list to the list
		append_list(L,r[i])
	return L

#Swap two nodes with each other
def swap(i,j):
	k = Node(i.item,None)
	i.item = j.item
	j.item = k.item

#Copys a list into a new one 
def copy_list(L):
	temp = L.head
	c_list = List()

	while temp is not None:
		append_list(c_list,temp.item)
		temp = temp.next

	return c_list

#Method Median: Finds the median in each sorted list, prints time when running, and the number of comparisions
def median(L,a_num):
	c_list = copy_list(L)
	if L is None:
		return None
	
	#Error message
	if a_num > 3 or a_num < 0:
		return "ERROR: Menu choice is over 3 or less than 0"

	#Bubble Sort 
	if a_num == 0:
		start = timeit.default_timer()
		bubble_sort(c_list)
		stop = timeit.default_timer()
	
		print_list("Bubble Sort: ", c_list)
		print('Time: ', stop - start) 
		print("COUNT: " + str(BCOUNT))

	#Merge Sort 
	if a_num == 1:
		start = timeit.default_timer()
		c_list.head = merge_sort(c_list.head)
		stop = timeit.default_timer()
		
		print_list("Merge Sort: ", c_list)
		print('Time: ', stop - start) 
		print("COUNT: " + str(MCOUNT))

	#Quick Sort 
	if a_num == 2:
		start = timeit.default_timer()
		quick_sort(c_list)
		stop = timeit.default_timer()
		
		print_list("Quick Sort: ", c_list)
		print('Time: ', stop - start)
		print("COUNT: " + str(QCOUNT))

	#Mod Quick Sort 
	if a_num == 3:
		start = timeit.default_timer()
		mod_quick_sort(c_list,0,get_length(c_list)-1,get_length(c_list)//2)
		stop = timeit.default_timer()
	
		print_list("Mod Quick Sort: ", c_list)
		print('Time: ', stop - start)
		print("COUNT: " + str(QMCOUNT))
	
	#Get median from the list
	med = element_at(c_list, get_length(c_list) //2)
	return med

#################################################################################################
#MAIN
#################################################################################################
try:
	size_list = int(input('Enter the size of the list: \n'))
	
	#Generate list of random numbers and copy it
	L = gen_rand_list(size_list)
	c_list = copy_list(L)

	print_list("Original List: ", L)
	print()

	print("Enter the sorting algorithm\n" 
	+ "\n0: Bubble Sort " 
	+ "\n1: Merge Sort" 
	+ "\n2: Quick Sort" 
	+ "\n3: Mod Quick Sort" )
	#choice = int(input()) 

	#Print the medians of the methods
	print(str(median(L,0).item) + "\n")		#Bubble sort
	print(str(median(L,1).item) + "\n")		#Merge Sort
	print(str(median(L,2).item) + "\n")		#Quick Sort
	print(str(median(L,3).item) + "\n")		#M Quick Sort

except ValueError:
	print("ERROR: Invalid input")