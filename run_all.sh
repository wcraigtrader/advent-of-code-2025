#! /bin/bash

TOP="$( cd "$(dirname "$0")" >/dev/null 2>&1 && pwd -P )"

export PYTHONPATH=${TOP}/src

for day in 01 02 03 04 05 06 07 08 09 10 11 12 ; do
    python3 ${TOP}/src/day${day}/puzzle${day}.py 
done