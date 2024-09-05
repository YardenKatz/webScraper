import configparser


class ConfigService:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

    def read_config(self):
        self.config.read(self.config_file)

    def get_targets(self):
        return self.config.sections()

    def get_data(self, target, key):
        return self.config[target][key]
