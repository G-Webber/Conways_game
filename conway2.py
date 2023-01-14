
# Python code to implement Conway's Game Of Life
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
 
# setting up the values for the grid
ON = 250
OFF = 0
STEP = 20# must be even
vals = [ON, OFF]
 
def randomGrid(xN, yN):
 
    """returns a grid of NxN random values"""
    return np.random.choice(vals, xN*yN, p=[0.2, 0.8]).reshape(xN, yN)
 
def addGlider(i, j, grid):
 
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[OFF,    OFF, ON],
                       [ON,  OFF, ON],
                       [OFF,  ON, ON]])
    grid[i:i+3, j:j+3] = glider
 
def addGosperGliderGun(i, j, grid):
 
    """adds a Gosper Glider Gun with top left
       cell at (i, j)"""
    gun = np.zeros(11*38).reshape(11, 38)
 
    gun[5][1] = gun[5][2] = ON
    gun[6][1] = gun[6][2] = ON
 
    gun[3][13] = gun[3][14] = ON
    gun[4][12] = gun[4][16] = ON
    gun[5][11] = gun[5][17] = ON
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = ON
    gun[7][11] = gun[7][17] = ON
    gun[8][12] = gun[8][16] = ON
    gun[9][13] = gun[9][14] = ON
 
    gun[1][25] = ON
    gun[2][23] = gun[2][25] = ON
    gun[3][21] = gun[3][22] = ON
    gun[4][21] = gun[4][22] = ON
    gun[5][21] = gun[5][22] = ON
    gun[6][23] = gun[6][25] = ON
    gun[7][25] = ON
 
    gun[3][35] = gun[3][36] = ON
    gun[4][35] = gun[4][36] = ON
 
    grid[i:i+11, j:j+38] = gun

def update(frameNum, img, grid, xN, yN):
    newGrid = grid.copy()
    if (len(np.unique(grid)) == 2):
        return ldupdate(frameNum, img, grid, xN, yN)
    else:    
        for i in range(xN):
            for j in range(yN):
                currentval = grid[i, j]
                if (currentval > OFF) & (currentval%2 == 1): #going up
                    newGrid[i, j] = min((currentval + STEP),ON)
                elif (currentval < ON) & (currentval%2 == 0): #going down
                    newGrid[i, j] = max((currentval - STEP),OFF)
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

    #newGrid = grid.copy()

def ldupdate(frameNum, img, grid, xN, yN):
    # copy grid since we require 8 neighbors
    # for calculation and we go line by line
    newGrid = grid.copy()
    for i in range(xN):
        for j in range(yN):
            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulation takes place on a toroidal surface.
            total = int((grid[i, (j-1)%yN] + grid[i, (j+1)%yN] +
                         grid[(i-1)%xN, j] + grid[(i+1)%xN, j] +
                         grid[(i-1)%xN, (j-1)%yN] + grid[(i-1)%xN, (j+1)%yN] +
                         grid[(i+1)%xN, (j-1)%yN] + grid[(i+1)%xN, (j+1)%yN])/ON)
 
            # apply Conway's rules
            if grid[i, j]  == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = ON - STEP
            else:
                if total == 3:
                    newGrid[i, j] = OFF + STEP +1 #odd goes up to know which direction the flow is going
 
    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,
 
# main() function
def main():
 
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
 
    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--grid-x', dest='Nx', required=False)
    parser.add_argument('--grid-y', dest='Ny', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    parser.add_argument('--inputfile', dest='infile', required=False)
    args = parser.parse_args()
     
    # set grid size
    N = 50
    if args.N and int(args.N) > 8:
        N = int(args.N)

    xN = 25
    if args.N and int(args.N) > 8:
        xN = int(args.xN)
    
    yN = 36
    if args.N and int(args.N) > 8:
        yN = int(args.yN)
         
    # set animation update interval
    updateInterval = 1
    if args.interval:
        updateInterval = int(args.interval)
 
    # declare grid
    grid = np.array([])
 
    # check if "glider" demo flag is specified
    if args.glider:
        grid = np.zeros(xN*yN).reshape(xN, yN)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(xN*yN).reshape(xN, yN)
        addGosperGliderGun(10, 10, grid)
    elif args.infile:
        try:
            ingrid = pd.read_csv(args.infile)
            my_data = np.genfromtxt(args.infile, delimiter=',',skip_header=1)
            my_data = my_data.T
            my_data = my_data[1:].T
            for y in range(len(my_data)):
                for x in range(len(my_data[y])):
                    if my_data[y,x]>0:
                        my_data[y,x] = ON
        except Exception as e:
            print(e)
        grid = my_data
    else:   # populate grid with random on/off -
            # more off than on
        grid = randomGrid(xN,yN)
 
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest',cmap='Greys_r')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, xN, yN, ),
                                  frames = 10,
                                  interval=updateInterval,
                                  save_count=50)
 
    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=100, extra_args=['-vcodec', 'libx264'])
 
    plt.show()
 
# call main
if __name__ == '__main__':
    main()