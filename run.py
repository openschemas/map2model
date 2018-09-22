#!/usr/bin/env python3

# This is an example of using map2model, a module provided by
# openschemas-python
# https://www.github.com/openschemas/openschemas-python
# pip install openschemas
from openschemas.main.map2model import main

# Here is an example to run the parser in python
spec_parser = main(config_yml='specifications/configuration.yml',
                   output='docs/spec_files',
                   folder='specifications')
