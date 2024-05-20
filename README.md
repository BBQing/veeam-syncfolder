# Folder synchronizer
CLI application that syncronizes contents of source folder i nthe target direction and logs in the provided logfile. Source and target folders should not contain each other.


## Requirements
This project uses Poetry python dependency manager

# Installation
Run 
```
poetry install 
```

# Running
This project can be run as python module with

```
python -m syncronize --heartbeat HEARTBEAT--source SOURCE --target TARGET --logfile LOGFILE
```

# testing and development
There ar eseveral useful commands in the Makefile

```
make reset # Reset developemnt folder structure tempalte
make run # Runs the module on predefined paths
make pytest # Runs the tests
make check # Performs quality checks
```
