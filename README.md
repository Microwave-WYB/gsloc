# gsloc: Apple Location Service API for Python

This is a Python library and CLI application that provides a reverse engineered implementation of the Apple Location Service API.

This tool is inspired by https://github.com/zadewg/GS-LOC

## Installation

```bash
pip install gsloc
```

## Usage

Using as a Python library:

```python
from gsloc.core import query

results = query(["94:10:3e:a0:b7:bd"])
for result in results:
    print(result.model_dump())
```

Using as a command line tool:

```bash
gsloc 94:10:3e:a0:b7:bd # you can enter multiple MAC addresses separated by space
```

Ouput:

```bash
❯ gsloc 94:10:3e:a0:b7:bd
[05/14/24 22:27:22] INFO     2024-05-14 22:27:22,424 - gsloc.core - INFO - Querying Apple location service   core.py:114
                             with MAC addresses: ['94:10:3e:a0:b7:bd']
[05/14/24 22:27:23] INFO     2024-05-14 22:27:23,156 - gsloc.core - INFO - Received response from Apple      core.py:133
                             location service.
[
    WifiInfo(
        mac='94:10:3e:a0:b7:bd',
        channel=153,
        latitude=37.70825195,
        longitude=-122.45568847,
        accuracy=25,
        altitude=98,
        altitude_accuracy=4
    ),
    WifiInfo(
        mac='10:86:8c:45:bc:6e',
        channel=11,
        latitude=37.70871734,
        longitude=-122.45514678,
        accuracy=26,
        altitude=96,
        altitude_accuracy=4
    ),
    WifiInfo(
        mac='1e:9d:72:ca:be:6f',
        channel=1,
        latitude=37.70779037,
        longitude=-122.45628356,
        accuracy=27,
        altitude=105,
        altitude_accuracy=4
    ),
    ...
]
```

Or, you can provide a list of MAC addresses in a file and write the output to a GeoJSON file:

```txt
94:10:3e:a0:b7:bd
10:86:8c:45:bc:6e
...
```

```bash
gsloc -i macs.txt -o output.geojson
```
