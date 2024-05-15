# gsloc: Apple Location Service API for Python

gsloc is a Python library and CLI tool that provides a reverse-engineered interface to Apple's Location Service API. This project is inspired by the work found at [GS-LOC](https://github.com/zadewg/GS-LOC) on GitHub and aims to simplify querying Apple's location services using MAC addresses of Wi-Fi networks.

### What is Apple's GS-LOC Service?
Apple's GS-LOC service is a part of Apple's broader location services, which help in determining the geographical position of a device based on various data sources, including Wi-Fi networks. By providing the MAC addresses of nearby Wi-Fi access points, you can retrieve location data such as latitude, longitude, and accuracy. This service is typically used in devices for enhancing location accuracy especially when GPS data is inadequate or unavailable.

### Purpose of the gsloc Tool
The gsloc tool is designed to allow developers and researchers to interact with Apple's Location Service through a Python library or a command-line interface. It is particularly useful for applications and services where location data is critical, such as in geospatial analysis, tracking systems, and in any context where understanding the physical location context is beneficial.

### Use Cases
Geospatial Analysis: Analysts and developers can integrate location data into their applications for enhanced spatial analysis.
Device Tracking: Useful in scenarios where the geographical tracking of devices is necessary, enhancing capabilities in logistics and fleet management.
Augmented Reality and Gaming: Provides backend support for location-based services in AR applications and games, offering a richer user experience by integrating real-world data.
Research and Development: Enables researchers to gather and analyze location data for various experimental and developmental purposes.
By utilizing gsloc, users can leverage Apple's robust location infrastructure to enhance their applications and services with accurate geospatial data.

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
