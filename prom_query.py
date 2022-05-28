import csv
import requests
import sys
from grabber import PromDataGrabber

"""
A simple program to print the result of a Prometheus query as CSV.
"""


"""
Input paramters

1. URL of Prometheus
2. query language
3. rate or irate or none. If none, just get raw data
4. range of data points for number calculation (e.g. rate, average..)
5. querying frequency
6. the starting point of getting data, how many minutes ago from now on.
7. the length of querying time

Execution example: python3 ./query_csv.py $PROM_SERVER_URL '$QUERY_LANG' rate/irate/none $RANGE $START_OFFSET $FREQ $LENGTH
$ python3 query_csv.py http://10.102.36.94:9090 'container_cpu_usage_seconds_total{namespace="default"}' irate 1m 30m 15 10
"""


if len(sys.argv) < 7:
    print('#Parameters is not correct.')
    print('Usage: {0} http://prometheus:9090 $QUERY_LANG rate/irate/none $RANGE $START_OFFSET $FREQ $LENGTH'.format(sys.argv[0]))
    sys.exit(1)

## check parameters and replace default values
g = PromDataGrabber(sys.argv[1], sys.argv[2], None, None, sys.argv[5], sys.argv[6], sys.argv[7]) \
    if sys.argv[3] == "none" else\
    PromDataGrabber(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
print(g.getPromSql())
    
### getting metrics by query frequency
response = requests.get('{0}/api/v1/query'.format(g.getServerUrl()), params={'query': g.getPromSql()})
results = response.json()['data']['result']
### based on the PromSQL we sent, should only get one result
if len(results) != 1:
    print('Get more than one value, or more values... please update your PromSQL.')
    sys.exit(1)

writer = csv.writer(sys.stdout)
writer.writerow(results[0]['value'])

## Build a list of all labelnames used.
#labelnames = set()
#for result in results:
#      labelnames.update(result['metric'].keys())
#
## Canonicalize
#labelnames.discard('__name__')
#labelnames = sorted(labelnames)
#
#writer = csv.writer(sys.stdout)
## Write the header,
#writer.writerow(['name', 'timestamp', 'value'] + labelnames)
#
## Write the samples.
#for result in results:
#    l = [result['metric'].get('__name__', '')] + result['value']
#    for label in labelnames:
#        l.append(result['metric'].get(label, ''))
#    writer.writerow(l)
