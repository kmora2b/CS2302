
#p/n is makes it smaller
#draw_squares(ax,1,p/6, 2) and draw_squares(ax,1,p/6, 1) or draw_squares(ax,1,p/6, any num)  is a square and vice versa
#T SQUARE ALGO
import numpy as np
import matplotlib.pyplot as plt

def draw_squares(ax,n,p,w):
    if n>0:
        #i1 = [1,2,3,0,1]
        i1 = [1,2,3,0,1]
        q = p*w + p[i1]*(1-w)
        #ax.plot(p[:,0],p[:,1],color='k')
        ax.plot(p[:0],p[:1],color='k')
        draw_squares(ax,n-1,q,w)


plt.close("all") 
orig_size = 800
fig, ax = plt.subplots()

p = np.array([[-orig_size, orig_size],[-orig_size,-orig_size],[orig_size,-orig_size],[orig_size,orig_size],[-orig_size,orig_size]])
print("p in 2: " + str(p[:,0]/2))

def recurse_square(ax,n,p,w,level):
    if level > 0:
        print("p in recurse_square: " + str(p))
        draw_squares(ax,n,p,.8)
        

        recurse_square(ax,n,(p/2) + (orig_size),w,level-1) #Upper right
        recurse_square(ax,n,(p/2) + (-orig_size) ,w,level-1) #lower left
        recurse_square(ax,n,(p/2) + (orig_size),w,level-1) #Upper right
        recurse_square(ax,n,(p/2) + (-orig_size) ,w,level-1) #lower left


pY = np.copy(p[:,1])
pX = np.copy(p[:,0])

recurse_square(ax,1,pY,.8, 3)
recurse_square(ax,1,pX,.8, 3)


ax.set_aspect(1.0)
ax.axis('on')
plt.show()
fig.savefig('squares.png')


#n: the number of squares generates
#ax: plots it on matplotlib
#p: Coordinates the correlate a length for each side of the square
#w: the line length


#1. Start with a square
#2. At each convex the put another square with the corner as a center
#	Make a bigger image
#	Repeat 2

