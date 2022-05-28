
#   Copyright 2022 Carol Hsu
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


class PromDataGrabber():
    def __init__(self, server_url, query_lang, func="rate", func_range="1m", offset="20m", freq_sec=15, leng_min=10):
        self.server_url = server_url
        ## offset would keep changing while querying
        self.sql = func+"("+query_lang+"["+func_range+"] offset "+offset+")" if func else \
                   query_lang+" offset " +offset
        self.freq_sec = freq_sec
        self.leng_min = leng_min

    def getServerUrl(self):
        return self.server_url
    
    def getPromSql(self):
        return self.sql

    def getFreq(self):
        return self.freq_sec

    def getLength(self):
        return self.leng_min
