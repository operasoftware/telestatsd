# telestatsd
StatsD client in Python with support for Telegraf and SRV records in DNS.

## Features
* [SRV records](https://en.wikipedia.org/wiki/SRV_record) in DNS
* Support for StatsD input plugin in [Telgraf](https://github.com/influxdata/telegraf/blob/master/plugins/inputs/statsd/README.md) and its additional features like tags
* Pluggable system of address providers with SRV or static providers supported off-the-shelf


## Examples

### INET (static) address provider

INET provider returns (host, port) tuple for [AF_INET](https://docs.python.org/2/library/socket.html#socket.AF_INET) address family where host and port are passed while creating provider object.

```python
from telestatsd.address_providers.inet import Provider
from telestatsd.clients.udp import Client

address_provider = Provider(host='localhost', port=8125)
client = Client(tags={'foo': 1}, address_provider=address_provider)
client.incr('success', 1)
```

Since inet.Provider has default host (localhost) and port (8125) its initialization can be shortened:

```
client = Client(tags={'foo': 1}, address_provider=Provider())
```

### SRVINET address provider

SRVINET provider returns (host, port) tuple for [AF_INET](https://docs.python.org/2/library/socket.html#socket.AF_INET) address family where host and port are retrieved from first [SRV](https://en.wikipedia.org/wiki/SRV_record) record returned by DNS server.

```python
from telestatsd.address_providers.srvinet import Provider
from telestatsd.clients.udp import Client

address_provider = Provider(service='telegraf-in-docker',
                            domain='marathon.mesos',
                            protocol=Provider.PROTO_UDP)

lient = Client(tags={'foo': 1}, address_provider=address_provider)
client.incr('success', 1)
```

### Logger client

```python
import logging
import sys

from telestatsd.clients.logger import Client

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
client = Client(tags={'foo': 1})
client.incr('success')
> INFO:telestatsd.clients.logger:success,foo=1:1|c
```
