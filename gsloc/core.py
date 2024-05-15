"""Core functionality for querying the Apple location service."""

import logging
import struct
from dataclasses import asdict, dataclass
from typing import List

import requests

from gsloc.protobuf.location_pb2 import Request, Response  # pylint: disable=no-name-in-module

logger = logging.getLogger(__name__)


class NoResultsError(Exception):
    """Raised when no results are returned from the Apple location service."""

    def __init__(self, mac: str):
        super().__init__(f"No results found for MAC address: {mac}")


@dataclass
class WifiInfo:
    """Information about a WiFi network."""

    mac: str
    channel: int
    latitude: float
    longitude: float
    accuracy: int
    altitude: int
    altitude_accuracy: int

    def validate(self) -> None:
        """Validates the WifiInfo object."""
        assert 0 <= self.channel <= 255, "Channel must be between 0 and 255."
        assert -90 <= self.latitude <= 90, "Latitude must be between -90 and 90."
        assert -180 <= self.longitude <= 180, "Longitude must be between -180 and 180."
        assert self.accuracy >= 0, "Accuracy must be greater than or equal to 0."
        assert self.altitude >= 0, "Altitude must be greater than or equal to 0."
        assert self.altitude_accuracy >= 0, "Altitude accuracy must be greater than or equal to 0."

    @classmethod
    def from_response_wifi(cls, response_wifi: Response.ResponseWifi) -> "WifiInfo":
        """Creates a WifiInfo object from a ResponseWifi object."""
        try:
            return cls(
                mac=response_wifi.mac,
                channel=response_wifi.channel,
                latitude=response_wifi.location.latitude / 1e8,
                longitude=response_wifi.location.longitude / 1e8,
                accuracy=response_wifi.location.accuracy,
                altitude=response_wifi.location.altitude,
                altitude_accuracy=response_wifi.location.altitudeAccuracy,
            )
        except AssertionError as e:
            # Fields are invalid if Apple doesn't know this wifi access point
            raise NoResultsError(response_wifi.mac) from e

    def to_feature(self) -> dict:
        """Converts the WifiInfo object to a GeoJSON feature."""
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.longitude, self.latitude],
            },
            "properties": asdict(self),
        }


@dataclass
class PayloadHeader:
    """Header for the request's payload."""

    nul_sqh = b"\x00\x01"
    nul_nul = b"\x00\x00"
    llength = b"\x00\x05"
    locale = b"\x65\x6e\x5f\x55\x53"
    ilength = b"\x00\x13"
    identifier = b"\x63\x6f\x6d\x2e\x61\x70\x70\x6c\x65\x2e\x6c\x6f\x63\x61\x74\x69\x6f\x6e\x64"
    vlength = b"\x00\x0c"
    version = b"\x38\x2e\x34\x2e\x31\x2e\x31\x32\x48\x33\x32\x31"

    def build(self) -> bytes:
        """Builds the header for the request's payload."""
        return b"".join(
            (
                self.nul_sqh,
                self.llength,
                self.locale,
                self.ilength,
                self.identifier,
                self.vlength,
                self.version,
                self.nul_nul,
                self.nul_sqh,
                self.nul_nul,
            )
        )


class Payload:
    """Payload for the request."""

    def __init__(
        self, header: PayloadHeader, mac_addresses: List[str], noise: int = 0, signal: int = 100
    ):
        self.header = header
        self.request = Request()
        self.request.noise = noise
        self.request.signal = signal
        for mac in mac_addresses:
            self.request.wifis.add(mac=mac)

    def build(self) -> bytes:
        """Builds the payload for the request."""
        message = self.request.SerializeToString()
        size = struct.pack(">h", len(message))
        return self.header.build() + size + message


def query(macs: List[str]) -> List[WifiInfo]:
    """Queries the Apple location service with the given payload."""
    logger.info("Querying Apple location service with MAC addresses: %s", macs)
    payload = Payload(PayloadHeader(), macs)
    response = requests.post(
        url="https://gs-loc.apple.com/clls/wloc",
        data=payload.build(),
        headers={
            "User-Agent": "locationd/221 (com.apple.locationd/1.0)",
            "Content-Type": "application/octet-stream",
        },
        timeout=60,
    )
    raw_data = response.content
    if not raw_data:
        logger.error("Empty response received from Apple location service.")
        return []
    data_buffer = raw_data[raw_data.find(b"\x00\x00\x00\x01\x00\x00") + 8 :]
    response = Response()
    response.ParseFromString(data_buffer)

    logger.info("Received response from Apple location service.")

    return [WifiInfo.from_response_wifi(wifi) for wifi in response.wifis]
