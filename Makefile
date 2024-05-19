run:
	python -m syncronize --source ./source --target ./backup --logfile logfile.log

teardown:
	@rm -rf ./source && rm -rf ./backup

setup:
	@mkdir ./backup
	@cp -r ./source_template ./source

reset: teardown setup
