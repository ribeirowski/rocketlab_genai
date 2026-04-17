from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str
    db_connected: bool
    db_tables: list[str]
    model: str
    