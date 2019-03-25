"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 4
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 3/15/2019
Date of last modification: 3/24/2019

Purpose of program: 
To create a more substantial b tree program with specific b tree operations that follow certain problem solving approaches.

"""
#################################################################################################
#B TREE CLASS
#################################################################################################
import random
class BTree(object):
	# Constructor
	def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
		self.item = item
		self.child = child 
		self.isLeaf = isLeaf
		if max_items <3: #max_items must be odd and greater or equal to 3
			max_items = 3
		if max_items%2 == 0: #max_items must be odd and greater or equal to 3
			max_items +=1
		self.max_items = max_items

def FindChild(T,k):
	# Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree	
	for i in range(len(T.item)):
		if k < T.item[i]:
			return i
	return len(T.item)
			 
def InsertInternal(T,i):
	# T cannot be Full
	if T.isLeaf:
		InsertLeaf(T,i)
	else:
		k = FindChild(T,i)	 
		if IsFull(T.child[k]):
			m, l, r = Split(T.child[k])
			T.item.insert(k,m) 
			T.child[k] = l
			T.child.insert(k+1,r) 
			k = FindChild(T,i)	
		InsertInternal(T.child[k],i)   
			
def Split(T):
	#print('Splitting')
	#PrintNode(T)
	mid = T.max_items//2
	if T.isLeaf:
		leftChild = BTree(T.item[:mid]) 
		rightChild = BTree(T.item[mid+1:]) 
	else:
		leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
		rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
	return T.item[mid], leftChild,	rightChild	 
	  
def InsertLeaf(T,i):
	T.item.append(i)  
	T.item.sort()

def IsFull(T):
	return len(T.item) >= T.max_items

def Insert(T,i):
	if not IsFull(T):
		InsertInternal(T,i)
	else:
		m, l, r = Split(T)
		T.item =[m]
		T.child = [l,r]
		T.isLeaf = False
		k = FindChild(T,i)	
		InsertInternal(T.child[k],i)   
		
		
def Search(T,k):
	# Returns node where k is, or None if k is not in the tree
	if k in T.item:
		return T
	if T.isLeaf:
		return None
	return Search(T.child[FindChild(T,k)],k)
				  
def Print(T):
	# Prints items in tree in ascending order
	if T.isLeaf:
		for t in T.item:
			print(t,end=' ')
	else:
		for i in range(len(T.item)):
			Print(T.child[i])
			print(T.item[i],end=' ')
		Print(T.child[len(T.item)])	   
 
def PrintD(T,space):
	# Prints items and structure of B-tree
	if T.isLeaf:
		for i in range(len(T.item)-1,-1,-1):
			print(space,T.item[i])
	else:
		PrintD(T.child[len(T.item)],space+'	  ')  
		for i in range(len(T.item)-1,-1,-1):
			print(space,T.item[i])
			PrintD(T.child[i],space+'	')
	
def SearchAndPrint(T,k):
	node = Search(T,k)
	if node is None:
		print(k,'not found')
	else:
		print(k,'found',end=' ')
		print('node contents:',node.item)
	


#################################################################################################
#LAB METHODS
#################################################################################################
#1. Compute the height of the tree
def height(T):
	if T.isLeaf:
		return 0
	return 1 + height(T.child[0])


#2. Extract the items in the B-tree into a sorted list.
def bt_to_slist(T,s_list):
	#Just append all items to the new list
	if T.isLeaf:
		for t in T.item:
			s_list.append(t)
		return s_list
	#Go through each child and add items into the new list
	else:
		for i in range(len(T.item)):
			bt_to_slist(T.child[i],s_list)
			s_list.append(T.item[i])
	
	#Go to next child in the current node
		return bt_to_slist(T.child[len(T.item)],s_list)	   

#3. Return the minimum element in the tree at a given depth d.
def min_ele(T,d):
	if d > height(T) or d < 0:
		return "ERROR: Out of depth"
	
	if d == 0:
		return T.item[0]
	
	if T.isLeaf:
		return T.item[0]

	
	return min_ele(T.child[0],d-1)

#4. Return the maximum element in the tree at a given depth d.
def max_ele(T,d):
	if d > height(T) or d < 0:
		return "ERROR: Out of depth"

	if d == 0:
		return T.item[-1]
	
	if T.isLeaf:
		return T.item[-1]

	return max_ele(T.child[-1],d-1)

#5. Return the number of nodes in the tree at a given depth d.
def num_nodes(T,d):
	c = 0
	if d > height(T) or d < 0:
		return "ERROR: Out of depth"

	if T.isLeaf:
		c += len(T.item)

	if d == 0:
		return len(T.item)
	
	#Traverse through list and add one to the count until d is 0
	else:
		for i in range(len(T.child)):
			c += num_nodes(T.child[i],d-1)
	return c

#6. Print all the items in the tree at a given depth d.
def print_at_d(T,d):
	if d > height(T) or d < 0:
		print ("ERROR: Out of depth")
		return 

	#Print current item in tree and do not add new line
	if d == 0:
		print(T.item, end=' ')

	if T.isLeaf:
		return 
	
	#Traverse through the current node and print each node
	for i in range(len(T.child)):
		print_at_d(T.child[i],d-1)

#7. Return the number of nodes in the tree that are full.
def full_nodes(T):
	if len(T.item) == T.max_items:
		return 1
	else:
		c = 0
		for i in range(len(T.child)):
			c+= full_nodes(T.child[i])

		return c

#8. Return the number of leaves in the tree that are full.
def full_leaves(T):
	#Check if t is currently a leaf and if exceeds max items then return 1
	if T.isLeaf:
		if len(T.item) == T.max_items:
			return 1
		else:
			return 0
	
	#Traverse through each node and add one to the count
	else:
		c = 0
		for i in range(len(T.child)):
			c += full_leaves(T.child[i])
		return c

#9. Given a key k, return the depth at which it is found in the tree, of -1 if k is not in the tree.
def k_at_d(T,d,k):
	if k in T.item: #If k in current depth or root is k then return the depth
		return d

	if T.isLeaf:	#Since the previous check was false then return not found
		return "Not Found"

	else:			#Use FindChild to check subtree if k is in it and if not found then add 1 to d
		return k_at_d(T.child[FindChild(T,k)], d+1, k)


#################################################################################################
#MAIN
#################################################################################################
#L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
#L = [6,3,16,11,7,17,14,8,5,19,15,1,2,4,18,13,9,20,10,12,21]

#Try and catch errors if input is not an integer
try:
	n = int(input("Enter the size of the list \n"))
	L = random.sample(range(n+100), n)	#Creates random list 

	T = BTree()	   

	#Build b tree from the generated list and insert with b tree insert and print the order
	for i in L:
		print('Inserting',i)
		Insert(T,i)
		PrintD(T,'') 
		#Print(T)
		print('\n####################################')

	d = int(input("Enter the depth \n"))
	k = int(input("Enter the key \n"))

	print("Height: " + str(height(T)))
	print("Min Element in depth " + str(d) + ": " + str(min_ele(T,d)) + "\n")
	print("Max Element in depth " + str(d) + ": " + str(max_ele(T,d)) + "\n")
	print("B-Tree to Sorted List: " + str(bt_to_slist(T,[]))+ "\n")
	print("Num of nodes in depth " + str(d) + ": " + str(num_nodes(T,d))+ "\n")

	print("Print items in depth "+ str(d) + ": ")
	print_at_d(T,d)
	print("\n")

	print("Num of full Nodes: " + str(full_nodes(T))+ "\n")
	print("Num of full Leaves: " + str(full_leaves(T))+ "\n")
	print("Key " + str(k) + " at depth: " + str(k_at_d(T,0,k)))

except IndexError:
	print("Invalid input")

except ValueError:
	print("Invalid input")
