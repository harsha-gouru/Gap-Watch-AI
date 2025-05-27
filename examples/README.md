# GapWatch-AI Examples

This directory contains example scripts to demonstrate the usage of GapWatch-AI.

## Dummy Training Script (`dummy_train.py`)

This script simulates a simple machine learning training process.

### Running with GapWatch-AI

You can monitor this script using the `gapwatch train` command:

```bash
# Ensure GapWatch is installed or you are in an environment where it can be run
# For development, from the project root:
python gapwatch/cli.py train examples/dummy_train.py --epochs 5 --lr 0.001

# If GapWatch were installed as a package:
# gapwatch train examples/dummy_train.py --epochs 5 --lr 0.001 
```

This will:
1. Execute the `dummy_train.py` script.
2. (Simulate) Monitor its energy consumption.
3. (Simulate) Log other relevant training metadata.

Refer to the main project README for more details on `gapwatch` commands.
