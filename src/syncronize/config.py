from syncronize.cli import parser


class Configuration:

    def __init__(self):
        self.args = parser.parse_args()

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


config = Configuration()
