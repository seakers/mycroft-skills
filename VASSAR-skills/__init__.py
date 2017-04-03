# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import dirname
import requests

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.configuration import ConfigurationManager

__author__ = 'bang'

LOGGER = getLogger(__name__)
config = ConfigurationManager.get().get("daphne").get("http")

class VASSARSkill(MycroftSkill):

    def __init__(self):
        port = config.get("port")
        host = config.get("host")
        route = "/server/vassar/"
        self.url = "http://" + host + ":" + str(port) + route
        super(VASSARSkill, self).__init__(name="VASSARSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))
        
        eval_arch_intent = IntentBuilder("EvalArchIntent").\
            require("EvalArchKeyword").build()
        self.register_intent(eval_arch_intent, self.handle_eval_arch_intent)

        initialize_jess_intent = IntentBuilder("InitializeJessIntent").\
            require("InitializeJessKeyword").build() 
        self.register_intent(initialize_jess_intent, self.handle_initialize_jess_intent)
        
        
        

    def handle_eval_arch_intent(self, message):
        resp = requests.post(self.url + "evaluate-architecture/")
        self.speak_dialog("eval.arch",resp.json())
        

    def handle_initialize_jess_intent(self, message):
        r = requests.post(self.url + "initialize-jess/")
        self.speak_dialog("initialize.jess")

    def stop(self):
        pass


def create_skill():
    return VASSARSkill()
