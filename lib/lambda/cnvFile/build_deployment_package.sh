#!/bin/bash
poetry install
poetry export -f requirements.txt --output requirements.txt

pip install -r requirements.txt --target ./package

cd package
zip -r ../deployment-package.zip .
cd ..

zip -g deployment-package.zip index.py
