# Prometheus data grabber

I take reference and update the script from [RobustPerception](https://github.com/RobustPerception/python_examples/tree/master/csv).

The purpose of this tool is to export the metrics data in Prometheus within certain time period and granularity, then we can use these values to plot the suitable visualzation by cases.


## Parameters Introduction
To get each data point, tool needs to send single API request. 
Therefore, to drawing a line/graph for variability, we will need to send several API requests.

Four "timing" keywords are important parameters when using this tool:
   1. `$RANGE`: The range for rate function. **E.g. 1m**. Two data points in this range would be picked for counting the change per second.

   2. `$START_OFFSET`: The starting offset time for querying. **E.g. 20m**, to start grabbing data from 20 minutes ago. 

   3. `$FREQ`: The time difference, in second, between each datastores (of rate). **E.g. 15**. This effects how detail the graph would look like.

   4. `$LENGTH`: The length of time, in minute, for the datastores you want to grab.


Our Prometheus's scrape interval is 15 seconds, which is also the minimum value of monitoring (based on the default value of Kubelet's cAdvisor).
This is a critical value for us to know when setting up these parameters and gathering the data points.

Also, althought there are delays for querying data in Prometheus. 
Like we expect to get data from `$START_OFFSET` to `$START_OFFSET+$LENGTH`, and turns out the data is from `$START_OFFSET` to `$START_OFFSET+$LENGTH+delays`.
We can ignore these delays by the specific timestamps we get when drawing graph.

Another keyword is to indicate which rate functions to use: **rate** or **irate**.
   - rate: the difference per second between first and last data points in certain range.
   - irate: the instant rate, the difference per second between last two data points in certain range.
For comparsion, "rate" shows more view points on average; "irate" keeps sudden spikes and drops.

## Usage
Refer to following command for using this tool:

```
$ python3 ./query_csv.py $PROM_SERVER_URL '$QUERY_LANG' rate/irate/none $RANGE $START_OFFSET $FREQ $LENGTH
```

For example:

```
$ python3 query_csv.py http://10.102.36.94:9090 'container_cpu_usage_seconds_total{namespace="default"}' irate 1m 30m 15 10
```

This command will get values of CPU usage rate by "irate" in range of 1 minute, starting from 30 minutes ago to 20 minutes ago, and with 15-second interval.
We can add query details in `{}` of `$QUERY_LANG` to get specific data.

You can also check the script `collect_metrics.sh` for our usage example.
