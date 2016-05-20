# telestatsd
StatsD client in Python with support for Telegraf and SRV records in DNS

## Features
* [SRV records](https://en.wikipedia.org/wiki/SRV_record) in DNS
* Support for StatsD input plugin in [Telgraf](https://github.com/influxdata/telegraf/blob/master/plugins/inputs/statsd/README.md) and its additional features like tags
* Pluggable system of address providers with SRV or static (host, port) providers supported off-the-shelf
