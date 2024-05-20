import pytest
import argparse
from syncronize.config import Configuration


@pytest.fixture
def target_folder(tmpdir):
    return tmpdir.mkdir("target")


@pytest.fixture
def source_folder(tmpdir):
    source = tmpdir.mkdir("source")
    for i in range(5):
        subdir = source.mkdir(f"subdir_{i}")
        for j in range(i):
            file = subdir.join(f"file{j}.txt")
            with open(file, "w") as f:
                file.write("*" * i * j)
    return source


@pytest.fixture
def config(tmpdir, target_folder, source_folder):
    def _inner(
        heartbeat=None,
        source_dir=source_folder,
        target_dir=target_folder,
        logfile="logfile.log",
    ):
        ns = argparse.Namespace()
        ns.heartbeat = 5
        ns.target = target_dir
        ns.source = source_dir
        ns.logfile = tmpdir.join("logfile.log")
        return Configuration(ns)

    return _inner
