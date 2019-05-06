#/bin/bash

echo "Removing local version"

make clean
rm -rf _build
rm -rf api/generated
