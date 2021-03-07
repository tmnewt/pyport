from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# change to relocate where you'd like your pyport files to be saved.
YOUR_PYPORT_STORAGE = BASE_DIR/'your_pyport'


# storage location of pyport_examples
EXAMPLES_DIR = BASE_DIR/'pyport_examples'
LAZY_DATASET = EXAMPLES_DIR/'data/silly.pkl'
LAZY_INSTRUCTIONS = EXAMPLES_DIR/'instructions/silly.json'
