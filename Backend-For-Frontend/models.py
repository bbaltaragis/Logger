from pydantic import BaseModel


class Comment(BaseModel):
    anomaly_id: int
    comment: str
    username: str

class RootCause(BaseModel):
    id: int
    root_cause: str

class ResolutionSteps(BaseModel):
    id: int
    resolution_steps: str