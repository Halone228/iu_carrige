from asyncio import gather
import loguru
from .include import *
from iu_carrige.utils import deserialize
from base64 import b64decode
from iu_datamodels import MineralAndAttachmentsShort
from iu_carrige.events import new_mineral_event
from iu_carrige.deps import file_storage_dep
from types_aiobotocore_s3 import S3Client
from uuid import uuid4
from os import getenv
from pydantic import BaseModel
from pydantic import TypeAdapter

core_router = APIRouter(
    tags=['Minerals', 'Attachments']
)
new_mineral_adapter = TypeAdapter(list[MineralAndAttachmentsShort])

BUCKET_NAME = getenv('BUCKET_NAME')


class AddedAttachments(BaseModel):
    created_ids: dict[str, str]


@core_router.post(
    '/add_attachments'
)
async def add_attachments(
    s3_client: Annotated[S3Client, Depends(file_storage_dep)],
    files: list[UploadFile]
) -> AddedAttachments:
    loguru.logger.info(files)
    files_id = list(zip(files, (uuid4().hex for _ in range(len(files)))))
    await gather(
        *(
            s3_client.upload_fileobj(
                file.file,
                BUCKET_NAME,
                _id,
                {
                    'ContentType': file.headers['content-type'],
                    'ContentDisposition': file.headers['content-disposition']
                }
            )
            for file, _id in files_id
        )
    )
    return AddedAttachments(
        created_ids={
            file.filename: i for file, i in files_id
        }
    )


@core_router.post('/new_minerals')
async def new_minerals(
    serialization_type: Annotated[str, Body()],
    binary_minerals: Annotated[str, Body()]
): 
    binary = b64decode(binary_minerals)
    data = deserialize(serialization_type, binary)
    minerals = new_mineral_adapter.validate_python(data)
    await new_mineral_event.send_async(
        minerals
    )

__all__ = [
    'core_router'
]