from .base import BaseDatabaseDep, Mineral, MineralTag, insert, MineralAttachment, Tag
from typing import override, Any
from itertools import chain
from asyncio import gather, create_task