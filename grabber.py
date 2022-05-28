class PromDataGrabber():
    def __init__(self, server_url, query_lang, func="rate", func_range="1m", offset="20m", freq_sec=15, leng_min=10):
        self.server_url = server_url
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
