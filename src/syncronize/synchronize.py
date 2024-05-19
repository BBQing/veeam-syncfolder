import hashlib
import logging
import pathlib
import shutil
from stat import S_ISDIR, S_ISREG

from syncronize.config import config


class Syncronizer:

    def __init__(self):

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler(filename=config.logfile))
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def md5_of_file(path: pathlib.Path):
        with open(path, "rb") as file:
            return hashlib.file_digest(file, hashlib.md5)

    def syncronize(self):
        current_source = pathlib.Path(config.source_dir)
        current_target = pathlib.Path(config.target_dir)

        self.walksource(current_source, current_target)

    def delete_handler(self, path: pathlib.Path, is_direcory: bool):

        self.logger.info(f"DELETE {path}")
        if is_direcory:
            path.rmdir()
        else:
            path.unlink()

    def update_handler(self, path: pathlib.Path, target: pathlib.Path):
        self.logger.info(f"UPDATE {path}")
        shutil.copy2(path, target)

    def create_handler(
        self, path: pathlib.Path, target: pathlib.Path, is_directory: bool
    ):

        if not is_directory:
            self.logger.info(f"CREATE {path}")
            shutil.copy2(path, target)

        else:
            self.logger.info(f"CREATE {path}")
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

    def list_files_and_directories(
        self, path=pathlib.Path
    ) -> tuple[set[str], set[str]]:
        files = set()
        directories = set()
        for child in path.iterdir():
            mode = child.stat().st_mode
            if S_ISDIR(mode):
                directories.add(child.name)
            elif S_ISREG(mode):
                files.add(child.name)
            else:
                pass

        return files, directories

    def walksource(self, source_path: pathlib.Path, target_path: pathlib.Path):
        target_files, target_directories = self.list_files_and_directories(target_path)

        source_files, source_directories = self.list_files_and_directories(source_path)

        # remove not present in source

        for file in target_files - source_files:
            self.delete_handler(target_path / file, False)

        for directory in target_directories - source_directories:
            self.delete_handler(target_path / directory, True)

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
