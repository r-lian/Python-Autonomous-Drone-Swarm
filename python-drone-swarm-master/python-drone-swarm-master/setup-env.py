#!/usr/bin/python3

import sys
import os

print("before append")
print(sys.path)
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
print("after append")
print(os.path.dirname(__file__))
print(sys.path)
sys.path.insert(1, os.path.dirname(__file__))
print(sys.path)
