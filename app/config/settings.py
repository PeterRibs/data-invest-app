from pydantic_settings import BaseSettings
from decimal import Decimal


class Settings(BaseSettings):
    symbol: str
    open: Decimal
    higher: Decimal
    lower: Decimal
    closed: Decimal
    volume: int
