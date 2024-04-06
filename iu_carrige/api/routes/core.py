from asyncio import gather
import loguru
from .include import *
from iu_carrige.utils import deserialize
from base64 import b64decode
from iu_datamodels import MineralAndAttachments
from iu_carrige.events import new_mineral_event
from iu_carrige.deps import file_storage_dep
from types_aiobotocore_s3 import S3Client
from uuid import uuid4
from os import getenv
from pydantic import BaseModel

core_route = APIRouter(
    tags=['Minerals', 'Attachments']
)


BUCKET_NAME = getenv('BUCKET_NAME')


class AddedAttachments(BaseModel):
    created_ids: dict[str, str]


@core_route.post(
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


@core_route.post('/new_minerals')
async def new_minerals(
    serialization_type: Annotated[str, Body()],
    binary_minerals: Annotated[str, Body()]
): 
    binary = b64decode(binary_minerals)
    data = deserialize(serialization_type, binary)
    await gather(
        *(
            new_mineral_event.send_async(MineralAndAttachments.model_validate(i, from_attributes=True)) for i in data
        )
    )


__all__ = [
    'core_route'
]