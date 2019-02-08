"""
Course: CS 2302 [MW 1:30-2:50] 
Author: Kimberly Morales
Assignment: Lab 1
Instructor: Olac Fuentes
TA(s): Anindita Nath , Maliheh Zargaran 
Date: 2/8/2019
Date of last modification: 2/8/2019

Purpose of program: 
To generate fractal like shapes such as circles, squares,and trees with recursive algorithms. 
This means to break down the problem into smaller pieces and build it to a bigger pictures.
For this case, breaking down the overall larger shape and utilize basic geometry to efficently produce these images. 

"""

import numpy as np
import matplotlib.pyplot as plt
import math 

#############################################################################################################################
#FIGURE 1: Nested Squares
#############################################################################################################################

def draw_nest_squares(ax,n,x,y,d):
    if n > 0:
        #Continously plots the x and y coordinates for each recursive call
        ax.plot(x[:]-d,y[:]-d, color='k')
        
		#Four recursive calls to create squares that have half the length of their predecessor and their vertexes
        #For x coordinates: Each new square is half of the predecessor and is +- with d 
		#For y coordinates: Each new square is hald of the predecessor and is +- with d
        draw_nest_squares(ax,n-1,x/2+d, y/2+d, d)   #Upper Right
        draw_nest_squares(ax,n-1,x/2+d, y/2-d, d)   #Lower Right
        draw_nest_squares(ax,n-1,x/2-d, y/2+d, d)   #Upper Left
        draw_nest_squares(ax,n-1,x/2-d, y/2-d, d)   #Lower Left


def deploy_nest_squares(level):
    orig_size = 800
    fig, ax = plt.subplots()
    
	#Seperates the 2d array into x and y components of size 800 and for the four points of the square(the fifth is for the cycle)
    p = np.array([[-orig_size, orig_size],[-orig_size,-orig_size],[orig_size,-orig_size],[orig_size,orig_size],[-orig_size,orig_size]])
    px = p[:,0]
    py = p[:,1]

    draw_nest_squares(ax,level,px,py,orig_size)
    ax.set_aspect(1.0)
    ax.axis('off')


    plt.show()
    fig.savefig('nest-squares' + str(level) + '.png')
    plt.close("all") 

#############################################################################################################################
#FIGURE 2: Concentric Circles
#############################################################################################################################

def circle(center,rad):
    n = int(4*rad*math.pi)
    t = np.linspace(0,6.3,n)
    x = center[0]+rad*np.sin(t)
    y = center[1]+rad*np.cos(t)
    return x,y

def draw_circles(ax,n,center,radius,w):
    if n>0:
        #Plots circles  based on w ratio and center point
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        draw_circles(ax,n-1,center,(radius*w),w)

def draw_con_circles(ax,n, center, radius,d):
    if n > 0:
        #d: Shifter variable and shares similar value to the radius except that it stays constant in the recursive calls
        #Draws one circle from draw_circles and recursively calls con-circles to shift to the left with d 
        draw_circles(ax,1,[radius,0],radius,.9)
        draw_con_circles(ax,n-1, [radius+d, 0],radius+d,d)

def deploy_con_circles(level):
    plt.close("all") 
    fig, ax = plt.subplots() 

    draw_con_circles(ax,level, [100, 0], 100,100)

    ax.set_aspect(1.0)
    ax.axis('off')
    plt.show()
    fig.savefig('con-circles' + str(level) + '.png')

#############################################################################################################################
#FIGURE 3: Tree
#############################################################################################################################
def draw_trees(ax,n,x,y,d,h):
    if n > 0:
        ax.plot(x[:],y[:], color='k')
        
        #d: Increment value that shifts the x values with the value of the line length
		#h: Height of the tree, shifts the y coordinates consistently
        #Two recursive calls that plots on opposite sides of the x axis with each x coordinate being half of their predecessor
        draw_trees(ax,n-1, (x/2)-d, y-(h),d, h)
        draw_trees(ax,n-1, (x/2)+d, y-(h),d, h)

def deploy_trees(level):
    #line_length: Same line length from the origin to the end points
    line_length = 50
    
	#p: 2D array composed of three lines with three coordinates. The origin is index 1 with the two endpoints being mirrored
    p = np.array([[-line_length, -line_length],[0, 0], [line_length, -line_length]]) 
    px = p[:,0]
    py = p[:,1]
    plt.close("all") 

    fig, ax = plt.subplots() 
    draw_trees(ax,level,px,py,line_length,50)

    ax.set_aspect('auto')
    ax.axis('off')
    plt.show()
    fig.savefig('trees' + str(level) + '.png')

#############################################################################################################################
#FIGURE 4: Lotus 
#############################################################################################################################
def draw_lotus(ax,n,center,radius,w):
    if n>0:
        x,y = circle(center,radius)
        ax.plot(x,y,color='k')
        
		#Recursively calls five circles that are plotted in these positions: Center, right, left, up, down
		#For x circles (left,right): Plots the x coordinate that +- to the radius/3
		#For y circles (up,down): Similar to x circles except it is done with the y coordinates
        draw_lotus(ax,n-1, center,radius*w, w)                                #Center
        draw_lotus(ax,n-1, [center[0]+2*(radius/3), center[1]],radius*w, w)   #Right
        draw_lotus(ax,n-1, [center[0]-2*(radius/3), center[1]],radius*w, w)   #Left
        draw_lotus(ax,n-1, [center[0], center[1]+2*(radius/3)],radius*w, w)   #Up
        draw_lotus(ax,n-1, [center[0], center[1]-2*(radius/3)],radius*w, w)   #Down

def deploy_lotus(level):
    plt.close("all") 
    fig, ax = plt.subplots() 

    draw_lotus(ax,level,[0, 0],100,1/3)

    ax.set_aspect(1.0)
    ax.axis('off')
    plt.show()
    fig.savefig('lotus-circles' + str(level) + '.png')

#############################################################################################################################
#MAIN INPUT/OUTPUT: Holds menu for different figures to draw 
#############################################################################################################################
try:
    choice = 0
    while choice != 5:
        print("Enter the number of which shape you want: \n" 
        + "1: Nested Squares\n" 
        + "2: Concentric Circles\n"  
        + "3: Tree\n" 
        + "4: Lotus\n"
        + "5: EXIT\n")
        
        choice = int(input())

        if choice != 5:
            level = int(input("Enter the number of levels \n"))
            if choice == 1:
                deploy_nest_squares(level)
            if choice == 2:
                deploy_con_circles(level)
            if choice == 3:
                deploy_trees(level)
            if choice == 4:
                deploy_lotus(level)

except ValueError:
    print("ERROR: Invalid input")




