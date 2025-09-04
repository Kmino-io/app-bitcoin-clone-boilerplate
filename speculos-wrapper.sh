#!/bin/bash

# Wrapper script to run Speculos properly in Docker container
# This fixes the interactive terminal issue

if [ "$1" = "--model" ] && [ "$3" = "build/nanos2/bin/app.elf" ]; then
    # This is the extension trying to run the emulator
    exec speculos --model "$2" --display headless --apdu-port 9999 --api-port 5000 /app/build/nanos2/bin/app.elf
else
    # Pass through other commands
    exec speculos "$@"
fi
