#!/bin/sh
rm -rf dist build *.egg-info
python setup.py bdist_egg
