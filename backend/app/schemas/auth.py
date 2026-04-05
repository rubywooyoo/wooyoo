from pydantic import BaseModel


class LiffLoginRequest(BaseModel):
    line_user_id: str
    display_name: str = ""
    avatar_url: str = ""


class LiffLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str
