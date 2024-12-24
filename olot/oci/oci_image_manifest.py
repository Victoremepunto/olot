# generated by datamodel-codegen:
#   filename:  image-manifest-schema.json
#   timestamp: 2024-12-04T11:34:21+00:00

from __future__ import annotations

from typing import Annotated, List, Optional

from pydantic import BaseModel, Field

from olot.oci.oci_common import MediaType, Digest, Urls
from olot.utils.types import Int64, Base64, Annotations

# class MediaType(BaseModel):
#     __root__: constr(
#         regex=r'^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]{0,126}$'
#     )


# class Digest(BaseModel):
#     __root__: constr(regex=r'^[a-z0-9]+(?:[+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+$') = Field(
#         ...,
#         description="the cryptographic checksum digest of the object, in the pattern '<algorithm>:<encoded>'",
#     )


# class Urls(BaseModel):
#     __root__: List[AnyUrl] = Field(
#         ..., description='a list of urls from which this object may be downloaded'
#     )


# class MapStringString(BaseModel):
#     __root__: Dict[constr(regex=r'.{1,}'), str]


# class Int8(BaseModel):
#     __root__: conint(ge=-128, le=127)


# class Int16(BaseModel):
#     __root__: conint(ge=-32768, le=32767)


# class Int32(BaseModel):
#     __root__: conint(ge=-2147483648, le=2147483647)


# class Int64(BaseModel):
#     __root__: conint(ge=-9223372036854776000, le=9223372036854776000)


# class Uint8(BaseModel):
#     __root__: conint(ge=0, le=255)


# class Uint16(BaseModel):
#     __root__: conint(ge=0, le=65535)


# class Uint32(BaseModel):
#     __root__: conint(ge=0, le=4294967295)


# class Uint64(BaseModel):
#     __root__: conint(ge=0, le=18446744073709552000)


# class Uint16Pointer(BaseModel):
#     __root__: Optional[Uint16]


# class Uint64Pointer(BaseModel):
#     __root__: Optional[Uint64]


# class Base64(BaseModel):
#     __root__: str


# class StringPointer(BaseModel):
#     __root__: Optional[str]


# class MapStringObject(BaseModel):
#     __root__: Dict[constr(regex=r'.{1,}'), Dict[str, Any]]


# class Annotations(BaseModel):
#     __root__: MapStringString


class ContentDescriptor(BaseModel):
    mediaType: MediaType = Field(
        ..., description='the mediatype of the referenced object'
    )
    size: Int64 = Field(..., description='the size in bytes of the referenced object')
    digest: Digest = Field(
        ...,
        description="the cryptographic checksum digest of the object, in the pattern '<algorithm>:<encoded>'",
    )
    urls: Optional[Urls] = Field(
        None, description='a list of urls from which this object may be downloaded'
    )
    data: Optional[Base64] = Field(
        None, description='an embedding of the targeted content (base64 encoded)'
    )
    artifactType: Optional[MediaType] = Field(
        None, description='the IANA media type of this artifact'
    )
    annotations: Optional[Annotations] = None


class OCIImageManifest(BaseModel):
    schemaVersion: Annotated[int, Field(ge=2, le=2)] = Field(
        ...,
        description='This field specifies the image manifest schema version as an integer',
    )
    mediaType: Optional[MediaType] = Field(
        None, description='the mediatype of the referenced object'
    )
    artifactType: Optional[MediaType] = Field(
        None, description='the artifact mediatype of the referenced object'
    )
    config: ContentDescriptor
    subject: Optional[ContentDescriptor] = None
    layers: List[ContentDescriptor] = Field(..., min_length=1)
    annotations: Optional[Annotations] = None
