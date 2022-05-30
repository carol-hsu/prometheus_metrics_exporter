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


import requests
import sys
from grabber import PromDataGrabber


"""
Input paramters

1. URL of Prometheus
2. query language
3. rate or irate or none. If none, just get raw data
4. range of data points for number calculation (e.g. rate, average..)
5. querying frequency (sec)
6. the starting point of getting data, how many minutes ago from now on (min).
7. the length of querying time (min).

Execution example: python3 prom_query.py $PROM_SERVER_URL '$QUERY_LANG' rate/irate/none $RANGE $START_OFFSET $FREQ $LENGTH
$ python3 prom_query.py http://10.102.36.94:9090 'container_cpu_usage_seconds_total{namespace="default"}' irate 1m 30m 15 10
"""


if len(sys.argv) < 7:
    print('#Parameters is not correct.')
    print('Usage: {0} http://prometheus:9090 $QUERY_LANG rate/irate/none $RANGE $START_OFFSET $FREQ $LENGTH'.format(sys.argv[0]))
    sys.exit(1)

## check parameters and replace default values
g = PromDataGrabber(sys.argv[1], sys.argv[2], None, None, int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])) \
    if sys.argv[3] == "none" else\
    PromDataGrabber(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
#print(g.get_prom_sql())

if g.is_period_valid():
    # list of strings
    offset = g.get_offset()
    url =  g.get_server_url() + '/api/v1/query'

    # the offset of quering string will keep less and less = from the earliest data to the latest one
    for ts in range(offset, offset - g.get_length(), -g.get_freq()):
        ### getting metrics by query frequency
        response = requests.get(url, params={'query': g.get_prom_sql().replace('{0}', str(ts))})
        results = response.json()['data']['result']
        ### based on the PromSQL we sent, should only get one result
        if len(results) > 1:
            print('Get more than one value, or more values... please update your PromSQL.')
            sys.exit(1)
        elif len(results) < 1:
            print(str(ts)+",0")
            continue
 
        print(str(ts)+","+results[0]['value'][1])

    print(str(offset)+"  "+str(offset-g.get_length()))
else:
    print('Invaild query period from {0} seconds ago until {1} seconds ago'.format(str(g.get_offset()),\
                                                                                   str(g.get_offset() - g.get_length())))
