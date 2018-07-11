#!/bin/bash

echo "Running: $0"

RET=0

echo "Linting *.py"

flake8 useful_tools_services --filename=*.py

if  $? -ne "0"; then
    RET=1
fi
echo "Linting *.py COMPLETE"
