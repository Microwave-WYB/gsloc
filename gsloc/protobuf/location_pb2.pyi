# type: ignore
# pylint: disable=all
from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Response(_message.Message):
    __slots__ = ("wifis",)

    class ResponseWifi(_message.Message):
        __slots__ = ("mac", "location", "channel")

        class WifiLocation(_message.Message):
            __slots__ = (
                "latitude",
                "longitude",
                "accuracy",
                "zeroField4",
                "altitude",
                "altitudeAccuracy",
                "unknown11",
                "unknown12",
            )
            LATITUDE_FIELD_NUMBER: _ClassVar[int]
            LONGITUDE_FIELD_NUMBER: _ClassVar[int]
            ACCURACY_FIELD_NUMBER: _ClassVar[int]
            ZEROFIELD4_FIELD_NUMBER: _ClassVar[int]
            ALTITUDE_FIELD_NUMBER: _ClassVar[int]
            ALTITUDEACCURACY_FIELD_NUMBER: _ClassVar[int]
            UNKNOWN11_FIELD_NUMBER: _ClassVar[int]
            UNKNOWN12_FIELD_NUMBER: _ClassVar[int]
            latitude: int
            longitude: int
            accuracy: int
            zeroField4: int
            altitude: int
            altitudeAccuracy: int
            unknown11: int
            unknown12: int
            def __init__(
                self,
                latitude: _Optional[int] = ...,
                longitude: _Optional[int] = ...,
                accuracy: _Optional[int] = ...,
                zeroField4: _Optional[int] = ...,
                altitude: _Optional[int] = ...,
                altitudeAccuracy: _Optional[int] = ...,
                unknown11: _Optional[int] = ...,
                unknown12: _Optional[int] = ...,
            ) -> None: ...

        MAC_FIELD_NUMBER: _ClassVar[int]
        LOCATION_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_FIELD_NUMBER: _ClassVar[int]
        mac: str
        location: Response.ResponseWifi.WifiLocation
        channel: int
        def __init__(
            self,
            mac: _Optional[str] = ...,
            location: _Optional[_Union[Response.ResponseWifi.WifiLocation, _Mapping]] = ...,
            channel: _Optional[int] = ...,
        ) -> None: ...

    WIFIS_FIELD_NUMBER: _ClassVar[int]
    wifis: _containers.RepeatedCompositeFieldContainer[Response.ResponseWifi]
    def __init__(
        self, wifis: _Optional[_Iterable[_Union[Response.ResponseWifi, _Mapping]]] = ...
    ) -> None: ...

class Request(_message.Message):
    __slots__ = ("wifis", "noise", "signal", "source")

    class RequestWifi(_message.Message):
        __slots__ = ("mac",)
        MAC_FIELD_NUMBER: _ClassVar[int]
        mac: str
        def __init__(self, mac: _Optional[str] = ...) -> None: ...

    WIFIS_FIELD_NUMBER: _ClassVar[int]
    NOISE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    wifis: _containers.RepeatedCompositeFieldContainer[Request.RequestWifi]
    noise: int
    signal: int
    source: str
    def __init__(
        self,
        wifis: _Optional[_Iterable[_Union[Request.RequestWifi, _Mapping]]] = ...,
        noise: _Optional[int] = ...,
        signal: _Optional[int] = ...,
        source: _Optional[str] = ...,
    ) -> None: ...
