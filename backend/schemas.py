from pydantic import BaseModel
from pydantic import Field


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TagCreate(BaseModel):
    name: str


class TagResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class RecipeCreate(BaseModel):
    title: str
    description: str | None = None
    ingredients: list[str]
    steps: list[str]
    is_public: bool = True
    time: str | None = None
    difficulty: str | None = None
    tag_ids: list[int] | None = None


class RecipeResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    ingredients: list[str]
    steps: list[str]
    is_public: bool
    tags: list[TagResponse]
    time: str | None = None
    difficulty: str | None = None

    model_config = {"from_attributes": True}


class RecipeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    ingredients: list[str] | None = None
    steps: list[str] | None = None
    is_public: bool | None = None
    time: str | None = None
    difficulty: str | None = None
    tag_ids: list[int] | None = None


class RatingCreate(BaseModel):
    rating: int = Field(ge=1, le=5)


class RatingResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    rating: int

    model_config = {"from_attributes": True}


class RatingSummary(BaseModel):
    average: float
    count: int
    my_rating: int | None = None

