import pytest


def test_config(config, source_folder, target_folder):

    configuration = config()

    assert source_folder == configuration.source_dir
    assert target_folder == configuration.target_dir
    configuration.validate()

    configuration = config(target_dir=source_folder)

    assert source_folder == configuration.target_dir

    with pytest.raises(ValueError):
        configuration.validate()
