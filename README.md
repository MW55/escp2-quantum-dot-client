# escp2-quantum-dot-client
Create commands to print quantum dots using an epson ET 2750 / ET 2720 printer.

The tool uses the esc_functions.py and hex_functions.py from [https://github.com/Wyss/escp2-client](https://github.com/Wyss/escp2-client),
and the method for accessing individual printer nozzles at DOI: [10.1039/C8RA00756J](https://pubs.rsc.org/en/content/articlelanding/2018/ra/c8ra00756j#!divAbstract)

## Installation
Build the container:
docker-compose build

move the printing notebook:
docker cp escp2-client_qdots_1:/app/printing.ipynb /srv/docker/escp2-client/notebooks/

run the container, mounting host folders
docker run -p 8888:8888 -v </path/to/notebooks/>:/opt/notebooks -v </path/to/output/>:/app/output escp2-client_qdots

## Tutorial
### Printer parameters

These parameters describe the basic page units. There might be circumstances where it is necessary to change these parameters

qd.pmgmt = 720
sets the page management units to 1/720 inch

qd.vert = 720
sets the vertical units to 1/720 inch

qd.hor = 720
sets the horizontal units to 1/720 inch

qd.mbase = 2880
sets the base units to 1/2880 inch

qd.nozzles = 60
sets the number of nozzles per block to 60

# Creating single dots

A single dot is printed using the following command:
qd.create_single_dot(qd.color, size, x, y)
with qd.color is one of: qd.black, qd.black2, qd.black3, qd.cyan, qd.magenta, qd.yellow
size describes the size of the dot, 1=small, 2=medium, 3=large. Larger sized dots can be created by printing multiple dots of the same color to the same position
x = horizonal position, absolute
y = vertical position, relative to the last position of the printhead!

It is also important to note that the x and y positioning are for the printhead itself, not the nozzle group, meaning that you have to account for the position of the color/nozzle group on the printhead

# Creating matrices

A Matrix represents dots of a single color that are to be printed in close proximity
The matrix is created using a list of lists in Python, with each nested list representing all nozzles of the choosen color, for the ET-2750/2720, each nozzle group (color) has 59 nozzles, with black having three groups with 59 nozzles (black, black2, black3). Each element of the matrix represents a single nozzle, with 0 = no printing, 1 = small dot, 2 = medium dot, 3 = large dot.

As an example, for a printer with 3 nozzles per color, a matrix that would print 3 small dots in a diagonal line would look like this:  [[100], [010] ,[001]]

The amount of nested lists inside the main list are the amount of nozzles needed in the printhead travel direction
The function to generate printer commands using a matrix is as follows:
qd.create_dot_matrix(x, y ,qd.color, matrix)

- with x,y the coordinates (y is relative to the last printhead position). You also have to account for the nozzlegroup / color position on the printhead
- qd.color the color you want (black, black2, black3, cyan, magenta, yellow)
- matrix: the matrix in the form of a list of lists

# Printing
The raw print files (.prn) can be directly send to the printer. On Linux, the command is:
lp -oraw output/printfile.prn with oraw telling the program, that we want to print using the commands inside the file