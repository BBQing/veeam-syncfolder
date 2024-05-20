"Implementation of simple command line interface"
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--heartbeat", type=int, default=5)
parser.add_argument("--target")
parser.add_argument("--source")
parser.add_argument("--logfile", help="Path to logging file")

print(type(parser))
