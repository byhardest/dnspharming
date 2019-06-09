import configparser
import os

class config(object):
    def __init__(self,):
        self.Config = configparser.ConfigParser()
        self.Config.read(os.path.abspath(os.path.join('config',"dnspharming.conf")))

    def monitor(self,):
        return dict(self.Config.items('monitor'))

    def email(self,):
        return dict(self.Config.items('email'))

     