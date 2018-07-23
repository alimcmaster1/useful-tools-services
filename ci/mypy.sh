#!/bin/bash

echo "Running: $0"

RET=0

echo "Performing MyPy analysis on /app"

mypy useful_tools_services/app --ignore-missing-imports

if [ $? -ne "0" ]; then
    RET=1

fi
echo "MyPy Type checking COMPLETE"