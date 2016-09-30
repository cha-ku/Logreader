#!/bin/bash

# fanout.sh scp's the files
./fanout.sh

# chperm.sh changes the permissions
./chperm.sh

# rmscript.sh removes the previous instance
./rmscript.sh

# Declinechk.sh is the actual one that will work. But we will leave it out now
#./Declinechk.sh
