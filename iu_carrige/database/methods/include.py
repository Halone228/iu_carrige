from .base import BaseDatabaseDep, Mineral, MineralTag, insert, MineralAttachment
from typing import override, Any
from itertools import chain
from asyncio import gather, create_task