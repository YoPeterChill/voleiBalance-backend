from pydantic import BaseModel, Field

class PlayerCreate(BaseModel):
    name: str = Field(..., example="Pedro Augusto")
    skill_level: float = Field(..., ge=0, le=5, example=4.5)
