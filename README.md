# ambercalculator

**ambercalculator** is wrapper for the scientific software
[*AMBER*](http://ambermd.org/), a popular code for Molecular
Mechanics/Dynamics calculations, i.e. the numerical simulation of large
molecular systems with classical mechanics. *ambercalculator* is a library
of Python classes, that provides a python object-oriented interface to 
AMBER. 

*ambercalculator* has been developed as part of the 
[COBRAMM package](https://site.unibo.it/cobramm/en), a project
of the group of Prof. Marco Garavelli of Università di Bologna
that is designed to perform advanced theoretical chemistry simulations.

*ambercalculator* consists of five classes:
* `AmberCalculator` contains methods to
  run the programs from the AMBER suite
* `AmberInput` defines all the necessary parameters 
  for an AMBER calculation and produces the main input file
* `AmberTopology` stores and process the information
  about the topology of the molecular system (the connectivity of the
  molecule) and the interaction potentials between all the atoms 
* `AmberSnapshot` stores and process the information
  about the coordinates of the atoms, their velocities and the 
  periodic boundary conditions used in the calculation
* `AmberOutput` parses the output files produced
  by AMBER and extract some relevant results from a successful 
  calculation

Each class has its own methods to operate on the data stored within.
Furthermore, there is an interaction between the classes that allows
to realize an user-defined complete simulation workflow with AMBER.
E.g., once instances for `AmberInput`, `AmberTopology` and `AmberSnapshot`
have been created and modified in relation to the needs of the user, 
these instances can be used to start an AMBER calculation with
`AmberCalculator`. `AmberCalculator` will produce an `AmberOutput`
instance that contains the results of the calculation, and this can in turn
be reused to extract new `AmberSnapshot` instances to be used as 
initial conditions for new AMBER calculations.

## License

Copyright (c) 2019 ALMA MATER STUDIORUM - Università di Bologna

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


## Dependencies

*ambercalculator* has been tested with Python3 on an Ubuntu Linux 
distribution. The code depends on a few Python libraries, 
that are listed in the [requirements.txt](requirements.txt)
file. 

To use all the capabilities of *ambercalculator*, including the 
possibility of running molecular dynamics and molecular mechanics 
calculations, a working installation of AMBER would be necessary. 
However, AMBER is a commercial software that requires a 
manual compilation for its installation. 
For this reason we provide here a testing suite that 
does not involve the parts of the codes with external calls to AMBER.
This allows to test and run the code without a working 
AMBER installation.
 

## Installation

For the installation, the testing and the use of **ambercalculator**, we 
encourage the use of a Python *virtual environment*

     python3 -m venv ambercalculator_test
     source ambercalculator_test/bin/activate
     
First, you should get the latest version of the code
cloning the git repository from GitHub

    git clone https://github.com/matbonfanti/ambercalculator
    cd ambercalculator
    
Then enter in the project root directory and 
install **ambercalculator** with the command:

    python setup.py install
    
This command will make the package available and will
install all the necessary requirements.


## Testing

The directory `test` provides four Python files with unittest classes,
one for each of the four *ambercalculator* classes that are tested:
 `AmberInput`, `AmberTopology`, `AmberSnapshot` and `AmberOutput`. 
Each python file is named intuitively after the class that is tested.
Without a working installation of AMBER it is not possible to test
the `AmberCalculator` class, and for this reason this class is not
tested here.
 
All the test can be run by typing the command 

    python -m unittest -v test
    
from the root directory of *ambercalculator*.
Otherwise each group of tests can be called separately by 
calling each single python module

    python -m unittest -v test/amberinput.py
    python -m unittest -v test/ambersnapshot.py
    python -m unittest -v test/ambertopology.py
    python -m unittest -v test/amberoutput.py
    
The tests for `AmberOutput` will parse the output of 
two real AMBER calculations that are stored in zipped archives in the
directory `test`. During the tests of `test/amberoutput.py`, two
pdf files will be produced (`optimization.pdf` and `equilibration.pdf`) 
with the plots of the results of these two AMBER calculations. 


## Troubleshooting

In some systems the use of a virtual environment determines 
an **ImportError exception when importing matplotlib**.
This error is determined by the use of the standard Qt5 backend
and can be simply avoided by forcing the choice of 
the matplotlib backend. In practice, we suggest to change
the backend to TkAgg by using the environmental variable MPLBACKEND:

    export MPLBACKEND="TkAgg"

Further details are available in the 
[matplotlib FAQ](https://matplotlib.org/2.1.2/faq/virtualenv_faq.html)
