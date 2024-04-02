from fastapi import APIRouter, Depends, Query, Body, HTTPException
from typing import Annotated
from iu_carrige.deps import *
from iu_carrige.database.redis import RedisHelper