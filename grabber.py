
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
    def __init__(self, server_url, query_lang, func="rate", func_range="1m", freq_sec=15, offset=20, leng_min=10):
        self.server_url = server_url

        ## offset would keep changing while querying
        self.sql = func+"("+query_lang+"["+func_range+"] offset {0}s )" if func else \
                   query_lang+" offset {0}s"
        self.offset_min = offset
        self.freq_sec = freq_sec
        self.leng_min = leng_min

    def get_server_url(self):
        return self.server_url
    
    def get_prom_sql(self):
        return self.sql

    def get_offset(self):
        return self.offset_min*60

    def get_freq(self):
        return self.freq_sec

    def get_length(self):
        return self.leng_min*60

    def is_period_valid(self):
        # query would be invalid because
        # 1. offset or leng_min <= 0
        # 2. leng_min > offset
        if self.offset_min <= 0 or self.leng_min <= 0:
            return False
        elif self.leng_min > self.offset_min:
            return False

        return True
        
