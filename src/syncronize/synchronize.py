import pathlib
from syncronize.config import config, Configuration
from stat import S_ISDIR, S_ISREG
import logging
import hashlib
import shutil


class Syncronizer:

    def __init__(self, configuration: Configuration):
        self.config = configuration

    @staticmethod
    def md5_of_file(path: pathlib.Path):
        with open(path, "rb") as file:
            return hashlib.file_digest(file, hashlib.md5)

    def syncronize(self):
        current_source = pathlib.Path(self.config.source_dir)
        current_target = pathlib.Path(self.config.target_dir)

        self.walksource(current_source, current_target)

    def delete_handler(self, path: pathlib.Path, is_direcory: bool):

        logging.info(f"DELETE {path}")
        if is_direcory:
            path.rmdir()
        else:
            path.unlink()

    def update_handler(self, path: pathlib.Path, target: pathlib.Path):
        logging.info(f"UPDATE {path}")
        shutil.copy2(path, target)

    def create_handler(
        self, path: pathlib.Path, target: pathlib.Path, is_directory: bool
    ):

        if not is_directory:
            logging.info(f"CREATE {path}")
            shutil.copy2(path, target)

        else:
            logging.info(f"CREATE {path}")
            shutil.copytree(path, target, copy_function=shutil.copy2)

    def compare_file(
        self, source_path: pathlib.Path, target_path: pathlib.Path, path: str
    ):
        source_stat = (source_path / path).stat()
        target_stat = (target_path / path).stat()
        if source_stat.st_size != target_stat.st_size:
            return False
        if source_stat.st_mtime != target_stat.st_mtime:
            return False
        if self.md5_of_file(source_path / path) != self.md5_of_file(target_path / path):
            return False
        return True

    def walksource(self, source_path: pathlib.Path, target_path: pathlib.Path):
        target_files = set()
        target_directories = set()
        for child in target_path.iterdir():
            mode = child.stat().st_mode
            if S_ISDIR(mode):
                target_directories.add(child.name)
            elif S_ISREG(mode):
                target_files.add(child.name)
            else:
                pass

        source_files = set()
        source_directories = set()
        for child in source_path.iterdir():
            mode = child.stat().st_mode
            if S_ISDIR(mode):
                source_directories.add(child.name)
            elif S_ISREG(mode):
                source_files.add(child.name)
            else:
                pass

        # remove not present in source

        for file in target_files - source_files:
            self.delete_handler(target_path / file, False)

        for directory in target_directories - source_directories:
            self.delete_handler(target_path / file, True)

        for file in target_files & source_files:
            if not self.compare_file(source_path, target_path, file):
                self.update_handler(source_path / file, target_path / file)

        for directory in target_directories & source_directories:
            self.walksource(
                source_path=source_path / directory, target_path=target_path / directory
            )

        for file in source_files - target_files:
            self.create_handler(source_path / file, target_path / file, False)
        for directory in source_directories - target_directories:
            self.create_handler(source_path / directory, target_path / directory, True)
