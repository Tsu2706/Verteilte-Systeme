from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import or_

from models import Recipe, User, Rating, Tag
from schemas import Token, UserRegister, UserResponse
from schemas import RecipeCreate, RecipeResponse, RecipeUpdate, RatingCreate, RatingResponse, TagCreate, TagResponse
from database import SessionLocal, Base, engine, get_db


from auth import (
    DUMMY_HASH,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

# Tabellen anlegen (falls noch nicht vorhanden)

app = FastAPI(title="Mein Projekt", version="0.1.0")

#CORS aktivieren
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# option to make it safer
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Authentifizierung
# ---------------------------------------------------------------------------

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Neuen Benutzer anlegen. Passwort wird als Argon2-Hash gespeichert."""
    # 1. Prüft, ob username oder email bereits existieren (→ 400)
    # 2. Passwort hashen mit get_password_hash()
    # 3. User-Objekt anlegen, in DB speichern, zurückgeben
    existing_user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username oder Email bereits vergeben"
        )

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=get_password_hash(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



@app.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    OAuth2 Password Flow: Empfängt username + password als Formular-Daten.
    Gibt einen JWT zurück.
    """
    # 1. Benutzer anhand von form_data.username in der DB suchen
    # 2. Passwort mit verify_password() prüfen (Timing-Schutz: DUMMY_HASH nutzen)
    # 3. Bei Fehler: 401 zurückgeben (generische Meldung!)
    # 4. JWT mit create_access_token() erzeugen und zurückgeben
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        verify_password(form_data.password, DUMMY_HASH)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige Zugangsdaten",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige Zugangsdaten",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.username)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/my-profile", response_model=UserResponse)
def get_profile(
    current_username: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Gibt das Profil des eingeloggten Benutzers zurück (geschützter Endpoint)."""
    # Hinweis: current_username kommt bereits validiert aus dem JWT (via Depends)
    user = db.query(User).filter(User.username == current_username).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User nicht gefunden"
        )

    return user

# ---------------------------------------------------------------------------
# TODO: Eure eigenen Endpoints hier einfügen
# ---------------------------------------------------------------------------

# Beispiel:
# @app.get("/items")
# def get_items(db: Session = Depends(get_db)):
#     return db.query(Item).all()
#
# @app.post("/items", status_code=201)
# def create_item(data: ItemCreate, db: Session = Depends(get_db)):
#     item = Item(**data.model_dump())
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item


# get, patch, dlete recipe

@app.get("/recipes/search")
def filter_recipes(
    q: str | None = None,
    tag_ids: list[int] = Query([]),
    db: Session = Depends(get_db),
    current_username: str | None = Depends(get_current_user)
):
    query = db.query(Recipe)

    # user filter
    if current_username:
        user = db.query(User).filter(User.username == current_username).first()
        query = query.filter(
            (Recipe.is_public == True) |
            (Recipe.user_id == user.id)
        )
    else:
        query = query.filter(Recipe.is_public == True)

    # title + description filter
    if q:
        query = query.filter(
            or_(
                Recipe.title.ilike(f"%{q}%"),
                Recipe.description.ilike(f"%{q}%")
            )
        )

    # tag filtert
    if tag_ids:
        query = (
            query
            .join(Recipe.tags)
            .filter(Tag.id.in_(tag_ids))
            .group_by(Recipe.id)
            .having(func.count(Tag.id) == len(tag_ids))
        )

    return query.all()

@app.get("/recipes")
def get_recipes(
    db: Session = Depends(get_db),
    current_username: str | None = Depends(get_current_user)
):
    query = db.query(Recipe)

    if current_username:
        user = db.query(User).filter(User.username == current_username).first()

        # public + private
        return query.filter(
            (Recipe.is_public == True) |
            (Recipe.user_id == user.id)
        ).all()
    # nur public
    return query.filter(Recipe.is_public == True).all()


@app.post("/recipes", response_model=RecipeResponse)
def create_recipe(
    data: RecipeCreate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    # get user
    user = db.query(User).filter(User.username == current_username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # build recipe
    recipe = Recipe(
        title=data.title,
        description=data.description,
        ingredients=data.ingredients,
        steps=data.steps, 
        is_public=data.is_public,
        time=data.time,
        difficulty=data.difficulty,
        user_id=user.id
    )
    tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
    recipe.tags = tags

    # save db
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe


@app.patch("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe_partial(
    recipe_id: int,
    data: RecipeUpdate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    user = db.query(User).filter(User.username == current_username).first()
    if not user or recipe.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(recipe, key, value)

    db.commit()
    db.refresh(recipe)

    return recipe

@app.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    user = db.query(User).filter(User.username == current_username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if recipe.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(recipe)
    db.commit()

    return None

# ratings
@app.post("/recipes/{recipe_id}/ratings", response_model=RatingResponse)
def rate_recipe(
    recipe_id: int,
    data: RatingCreate,
    db: Session = Depends(get_db),
    current_username: str = Depends(get_current_user)
):

    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    user = db.query(User).filter(User.username == current_username).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(Rating).filter(
        Rating.user_id == user.id,
        Rating.recipe_id == recipe_id
    ).first()

    if existing:
        existing.rating = data.rating
        db.commit()
        db.refresh(existing)
        return existing

    rating = Rating(
        user_id=user.id,
        recipe_id=recipe_id,
        rating=data.rating
    )

    db.add(rating)
    db.commit()
    db.refresh(rating)

    return rating


#tags

@app.post("/tags", response_model=TagResponse)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    existing = db.query(Tag).filter(Tag.name == data.name).first()

    if existing:
        raise HTTPException(status_code=400, detail="Tag exists already")

    tag = Tag(name=data.name)

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag

@app.get("/tags", response_model=list[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()

