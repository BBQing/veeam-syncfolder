import pathlib
import argparse


class Configuration:

    def __init__(self, parsed_args: argparse.Namespace):
        self.args = parsed_args

    def validate(self):
        source = pathlib.Path(self.source_dir)
        target = pathlib.Path(self.target_dir)
        logfile = pathlib.Path(self.logfile)
        if target == source or target in source.parents or source in target.parents:
            raise ValueError("Self contained source and target directories")

    @property
    def heartbeat(self):
        return self.args.heartbeat

    @property
    def source_dir(self):
        return self.args.source

    @property
    def target_dir(self):
        return self.args.target

    @property
    def logfile(self):
        return self.args.logfile
