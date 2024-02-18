from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    symbol: str
    open: float
    higher: float
    lower: float
    closed: float
    volume: int
