"This module enable runnign this application as python module"
from syncronize import Syncronizer, Configuration, parser

config = Configuration(parser.parse_args())
sync = Syncronizer(config)

sync.syncronize()
