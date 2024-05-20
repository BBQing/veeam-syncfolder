from syncronize import Syncronizer


def test_syncronize(config, source_folder, target_folder):
    configuration = config()
    sync = Syncronizer(config=configuration)
    sync.syncronize()

    assert len(source_folder.listdir()) == len(target_folder.listdir())
    assert len((target_folder / "subdir_1").listdir()) == 1
    with open(source_folder / "subdir_1" / "file0.txt", "a") as f:
        f.write("bb")
