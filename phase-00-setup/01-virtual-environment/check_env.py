import sys

print("Python version :", sys.version.split()[0])
print("Interpreter    :", sys.executable)
print("sys.prefix     :", sys.prefix)
print("sys.base_prefix:", sys.base_prefix)

in_venv = sys.prefix != sys.base_prefix
print("Inside a venv? :", in_venv)
