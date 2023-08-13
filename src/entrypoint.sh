#!/bin/sh

echo "Entering the entrypoint file"
echo "Spawning 4 process"

python3 main.py && tail -f serving.log