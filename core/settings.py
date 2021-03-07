from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EXAMPLES_DIR = BASE_DIR/'pyport_examples'

LAZY_DATASET = EXAMPLES_DIR/'data/silly.pkl'
LAZY_INSTRUCTIONS = EXAMPLES_DIR/'instructions/silly.json'