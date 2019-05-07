#/bin/bash

echo "Removing local version"

make clean
rm -rf build
rm -rf api/generated
