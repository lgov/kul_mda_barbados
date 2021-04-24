#!/bin/sh

# Remove the output of a notebook, so that we can store it clean in git.
# To be executed before 'git add'
python -m nbconvert --clear-output *.ipynb **/*.ipynb
