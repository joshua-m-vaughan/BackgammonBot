# INFORMATION -------------------------------------------------------- #

# Author:  Code leveraged from COMP90054 Assignment 3.
# Date:    03/07/2024
# Purpose: Implements utility functions for Extended Form game
#          framework.

# IMPORTS ------------------------------------------------------------ #

import inspect
import sys

# CONSTANTS ---------------------------------------------------------- #


# CLASS DEF ---------------------------------------------------------- #

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)      

# END ---------------------------------------------------------------- #