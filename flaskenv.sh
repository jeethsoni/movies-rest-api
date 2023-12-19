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

echo "installing dependencies"
make install

echo "formatting code..."
make black 

echo "linting code..."
make lint

echo "printing lint results..."
make print-lint

echo "starting api..."
make run