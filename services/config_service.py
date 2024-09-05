import configparser
class ConfigService:
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = configparser.ConfigParser()

    def readConfig(self):
        self.config.read(self.configFile)

    def getTargets(self):
        return self.config.sections()

    def getData(self, target, key):
        return self.config[target][key]
