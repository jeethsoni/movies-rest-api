#!/bin/sh

################################################################
# flaskenv.sh
# usage: . ./flaskenv.sh
# This script will create a virtual environment activates it
###############################################################
#!/bin/sh


echo "creating virtual environment..."
virtualenv flaskenv

echo "activating virtual environment..."
source flaskenv/bin/activate