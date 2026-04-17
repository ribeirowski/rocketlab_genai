from pydantic import BaseModel, Field, field_validator

class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Pergunta em linguagem natural sobre os dados",
        examples=["Quais os 10 produtos mais vendidos?"],
    )
    
    @field_validator("question")
    @classmethod
    def strip_question(cls, v: str) -> str:
        return v.strip()
    
class QueryResponse(BaseModel):
    question_id: int
    question: str
    sql: str
    data: list[dict]
    analysis: str
    row_count: int