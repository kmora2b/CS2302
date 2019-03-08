"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 3
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 3/8/2019
Date of last modification: 3/8/2019

Purpose of program: 
The programs purpose is to implement five more additonal features to the binary search tree(bst): display, iterative search, sorted list to bst, bst to sorted list, and print at the depth. 

To display, we utilize the matplotlib library to create a figure that will annotate the value of the node with a circle draw arround it and connect to the next node if it exists. 

Iterative search is the loop version of recurisve search that will look for an element to the left or right if it is less than or greater than the element respectively. 

Sorted list to bst will first sort the list and then create a tree by recurisvely calling from the middle element and adding this middle element to the tree. This will be done without the insert operation.

BST to sortedlist will be similar to inorder but instead it will append the tree's current node to the list

Printing at depth will recursively call and subtract from d and go to the left and right and will print the element.

"""
import numpy as np
import matplotlib.pyplot as plt
import math 
import random

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
		T =	 BST(newItem)
	elif T.item > newItem:
		T.left = Insert(T.left,newItem)
	else:
		T.right = Insert(T.right,newItem)
	return T

#################################################################################################
#UTILITY METHODS
#################################################################################################

#Sorts list with modfiied bubble sort algorithm that has a boolean flag to indicate if a swap was done 
def sortList(L):
	for i in range(len(L)):
		swapped = False
		for j in range(len(L)-1):
			if L[j] > L[j+1]:
				L[j], L[j+1] = L[j+1], L[j]
				swapped = True
		if swapped == False:
			break
	

#Traditionally inserts node to the list
def list_to_bst(L):
	T = None
	for i in range(len(L)):
		T = Insert(T,L[i])
	return T

#Counts the longest height from the node to the deepest node
#If there is no tree then it is -1
#If there is one node then it is h =0
def height(T):
	if T is None:
		return -1
	return max(height(T.left) , height(T.right)) + 1


#################################################################################################
#LAB METHODS
#################################################################################################

#1) Display the binary search tree as a figure
########################################DISPLAY###################################################
def circle(center,rad):
	n = int(4*rad*math.pi)
	t = np.linspace(0,6.3,n)
	x = center[0]+rad*np.sin(t)
	y = center[1]+rad*np.cos(t)
	return x,y

#Draws tree based on the canvas size and height of the tree
#xmin: min size which is 0 so to not work with negatives
#xmax: max size which is the line length so to not to make the canvas too big or smallest
#ymin is same size as xmax but goes slightly to the right so to move the tree nodes 
#h is ymin divided by the tree height so to adjust the canvas to how big the tree is 
def draw_trees(ax,T,xmin, xmax,ymin,h):
	#If the tree is empty then return the tree and draw nothing
	if T is None:
		return T

	#xm: x coordinate that draws the line from the node center to next node center, add max and min element to avoid overdrawing and divides by 2 to minimize distance
	xm = (xmin + xmax) / 2		
	
	#ym: y coordinate that draws the line from the node center to next node center, subtracts height to avoid overdrawing
	ym = (ymin- h)

	#xc and yc are coordinates for the center of the circle to be draw around number
	xc,yc = circle([xm,ymin],3)
	ax.fill(xc,yc, zorder=3,color='white')	#Fills circle to hide line that hits the number, uses zorder to put it as a front layer
	
	#Plot left elements on the left side of the axis
	if T.left is not None:
		ax.plot([xm,((xm+xmin)/2)],[ymin,ym],color='k',zorder=1) #Uses min since it is messing with negatives
		draw_trees(ax,T.left,xmin,xm,ym,h)
		
	#Plots right elements on the right side of the axis
	if T.right is not None:
		ax.plot([xm,(xm+xmax)/2],[ymin,ym],color='k') #Uses max since it is messing with positives
		draw_trees(ax,T.right,xm,xmax,ym,h)

	#Matplotlib function (annotate) that adds text to a coordinate and centers it 
	ax.annotate(str(T.item), xy=(xm,ymin), xycoords = 'data',ha='center',va='center')
	ax.plot(xc ,yc,color='k')		#Plots with circle element to keep it center

#Used for top down design and to seperate the main function of drawing the tree
def deploy_trees(T):
	#line_length: Same line length from the origin to the end points
	line_length = 100.0
	
	#To avoid zero error if there is only a single node in the tree
	if height(T) == 0:
		h = 0
	else:
		#This will change line length approripriately with the height of the tree
		h = (line_length-10.0)/(height(T))
	
	fig, ax = plt.subplots() 
	draw_trees(ax,T,0,line_length,line_length-5,h)

	ax.set_aspect('1')
	ax.axis('off')
	plt.show()
	fig.savefig('bst' + str(height(T)) + '.png')

##############################################################################################

#2) Iterative version of the search operation
def search(T,k):
	t = T		#Temp tree
	while t is not None:
		if t.item == k:		#If k is the same value of the current node then k is in the node
			return t.item
		elif t.item < k:	#If k is greater than the node value then go to the right
			t = t.right
		elif t.item > k:	#If k is less than the node value then go to the left
			t = t.left
	return None

##############################################################################################

#3) Building a balanced binary search tree given a sorted list as input. Note: this should not use the insert operation,
#the tree must be built directly from the list in O(n) time
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

##############################################################################################
#4) Extracting the elements in a binary search tree into a sorted list. As above, this should be done in O(n) time. 

#Uses modified version of inorder to append the current element instead of printing it
def bst_to_slist(T,s_list):
	if T is not None:
		bst_to_slist(T.left,s_list)		#Go all the way to the left to get smallest element in the list
		s_list.append(T.item)			#Add current node to the list
		print(s_list)
		bst_to_slist(T.right,s_list)
	return s_list

##############################################################################################

#5) Printing the elements in a binary tree ordered by depth. The root has depth 0, the root’s children have depth one,
#and so on. For example, for the tree in the figure, your program should output:
def print_at_depth(T,d):
	if T is None:
		return "List is Empty"
	if d == 0:
		print (T.item)
	else:
		print_at_depth(T.left,d-1)
		print_at_depth(T.right,d-1)

#################################################################################################
#MAIN
#################################################################################################
#A menu is created to allow for multiple options along with error exceptions

cont = True			#cont: Will continue the loop as long it is inputted true by the user
while cont:
	try:
		#Create randomed generated list from size n
		print("Binary Search Tree Program")

		n = int(input("Enter the size of the list \n"))
		L = random.sample(range(100), n)
		
		#L = [10,4,15,2,8,12,18,1,3,5,9,7]
		
		print("Original List: " + str(L))
		
		#First Menu: Can traditionally create BST with unsorted list or use sorted list
		print("\n1. List to BST" + "\n2. Sorted List to BST ")
		choice = int(input())
		
		if choice == 1:
			T = list_to_bst(L)
		
		elif choice == 2:
			sortList(L)
			print("Sorted L: " + str(L))
			T = slist_to_bst(L)
		
		else:
			print("ERROR: INVALID INPUT")
			break
		
		#Second Menu: Can use search, create sorted list from BST from the first menu or print at depth
		print("\n1. Search" + "\n2. BST to Sorted List" + "\n3. Print at Depth")
		choice = int(input())
		
		if choice == 1:
			print("Input Element \n")
			k = int(input())
			print("Search: " + str(search(T,k)))
		
		elif choice == 2:
			print("BST to List" + str(bst_to_slist(T,[])))

		elif choice == 3:
			print("Input Depth \n")
			d = int(input())
			print("Key at depth " + str(d) + ": ")
			print_at_depth(T,d)
		
		else:
			print("ERROR: INVALID INPUT")
			break

		
		#Displays figure to matplotlib window and saves it as a figure
		deploy_trees(T)
		
		#Ask to continue loop and keep usng the program
		print("Continue?(y/n) ")
		cont = input()
		
		if cont.lower() == 'y' or cont.lower() == 'yes':
			cont = True
		
		elif cont.lower() == 'n' or cont.lower() == 'no':
			cont = False

		else:
			print("ERROR: INVALID INPUT")
			cont = True

	except ValueError:	#Catches invalid inputs such as negative numbers, letters, and special characters
		print("ERROR: INVALID INPUT")



