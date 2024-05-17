import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--heartbeat", type=int, default=5)
parser.add_argument("--target")
parser.add_argument("--source")