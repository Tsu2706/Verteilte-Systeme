from pydantic import BaseModel


# --- Auth-Schemas ---

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


# TODO: Fügt hier eure eigenen Schemas hinzu
# class ItemCreate(BaseModel):
#     name: str
#     price: int
#
# class ItemResponse(BaseModel):
#     id: int
#     name: str
#     price: int
#     model_config = {"from_attributes": True}

class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str

# recipe
class RecipeCreate(BaseModel):
    title: str
    description: str | None = None
    ingredients: list[Ingredient]
    steps: list[str]
    is_public: bool = True

class RecipeResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    ingredients: list[Ingredient]
    steps: list[str]
    is_public: bool
    model_config = {"from_attributes": True}

# recipe update?
"""
class RecipeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    ingredients: list[Ingredient] | None = None
    steps: list[str] | None = None
    is_public: bool | None = None
"""

# rating
class RatingCreate(BaseModel):
    rating: int

class RatingResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    rating: int

    model_config = {"from_attributes": True}