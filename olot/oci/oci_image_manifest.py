# generated by datamodel-codegen:
#   filename:  image-manifest-schema.json
#   timestamp: 2024-12-04T11:34:21+00:00

from __future__ import annotations

from typing import Annotated, List, Optional, Dict
import os
import subprocess
from pathlib import Path

from pydantic import BaseModel, Field

from olot.oci.oci_common import Urls, Keys, Values, MediaTypes, MediaType
from olot.utils.types import Int64, Base64, Annotations
from olot.utils.files import MIMETypes

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
        ..., description="The media type of the referenced object"
    )
    size: Int64 = Field(
        ..., description="The size in bytes of the referenced object"
    )
    digest: str = Field(
        ..., description="The cryptographic checksum digest of the object, in the pattern '<algorithm>:<encoded>'"
    )
    urls: Optional[Urls] = Field(
        None, description="A list of URLs from which this object may be downloaded"
    )
    data: Optional[Base64] = Field(
        None, description="An embedding of the targeted content (base64 encoded)"
    )
    artifactType: Optional[MediaType] = Field(
        None, description="The IANA media type of this artifact"
    )
    annotations: Optional[Dict[str, str]] = None

    class Config:
        exclude_none = True

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

def empty_config() -> ContentDescriptor:
    return ContentDescriptor(
        mediaType=MediaTypes.empty,
        size=2,
        digest=Values.empty_digest,
        data=Values.empty_data,
        urls=None,
        artifactType=None,
    )

def create_oci_image_manifest(
    schemaVersion: int = 2,
    mediaType: Optional[str] = MediaTypes.manifest,
    artifactType: Optional[str] = None,
    config: ContentDescriptor = empty_config(),
    subject: Optional[ContentDescriptor] = None,
    layers: List[ContentDescriptor] = [],
    annotations: Optional[Annotations] = None,
) -> OCIImageManifest:
    return OCIImageManifest(
        schemaVersion=schemaVersion,
        mediaType=mediaType,
        artifactType=artifactType,
        config=config,
        subject=subject,
        layers=layers,
        annotations=annotations,
    )

def get_file_media_type(file_path: os.PathLike) -> str:
    """
    Get the MIME type of a file using the `file` command.
    """
    try:
        result = subprocess.run(['file', '--mime-type', '-b', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        mime_type = result.stdout.decode('utf-8').strip()
        return mime_type
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while getting MIME type: {e}")
        return MIMETypes.octet_stream
    except Exception as e:
        print(f"Unexpected error: {e}")
        return MIMETypes.octet_stream


def create_manifest_layers(files: List[Path], blob_layers: dict) -> List[ContentDescriptor]:
    """
    Create a list of ContentDescriptor objects representing the layers of an OCI image manifest.

    Args:
        files (List[os.PathLike]): A list of file paths to be used as layers in the manifest.
    Returns:
        List[ContentDescriptor]: A list of ContentDescriptor objects representing the layers of the manifest
    """
    layers: List[ContentDescriptor] = []
    for file in files:
        precomp, postcomp = blob_layers[os.path.basename(file)]
        file_digest = postcomp if postcomp != "" else precomp
        layer = ContentDescriptor(
            mediaType=get_file_media_type(file),
            size=os.stat(file).st_size,
            digest=f"sha256:{file_digest}",
            annotations= {
                Keys.image_title_annotation: os.path.basename(file)
            },
            urls = None,
            data = None,
            artifactType = None,
        )
        layers.append(layer)
    return layers