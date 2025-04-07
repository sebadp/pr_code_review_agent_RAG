from pydantic import BaseModel


class LoadPRRequest(BaseModel):
    owner: str
    repo: str
    pr_number: int


class ReviewPRRequest(BaseModel):
    question: str = (
        "Please review this pull request in the context of the existing codebase"
    )


class QuestionRequest(BaseModel):
    question: str
