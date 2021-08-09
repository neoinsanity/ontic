#!/usr/bin/env bash
set -x

###########################################################
##### Create virtualenv for development.
# Virtaulenv needs to be installed for this to work.
###########################################################

# Create the virtual environment
python3 -m venv .venv

echo
echo "------------------------------------------------"
echo "- Virtual environment created in directory 'venv'"
echo "------------------------------------------------"

# Activate the virtual environment
echo
echo "------------------------------------------------"
echo "----- Activating virtual env with command. -----"

source .venv/bin/activate

echo "------------------------------------------------"
echo

###########################################################
##### Install development related packages.
###########################################################
echo
echo "------------------------------------------------"
echo "------- Installing development packages --------"
echo "------------------------------------------------"
echo
python -m pip install --upgrade pip
pip install -r bin/dev_requirements.txt


###########################################################
##### Install the windmills package in development mode.
###########################################################
echo
echo "------------------------------------------------"
echo "------ Setting up development environment ------"
echo "------------------------------------------------"

python setup.py develop
