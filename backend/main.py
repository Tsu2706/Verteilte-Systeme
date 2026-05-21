from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import Recipe, User
from schemas import RecipeCreate, RecipeResponse
from database import SessionLocal

from auth import (
    DUMMY_HASH,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from database import Base, engine, get_db
from models import User
from schemas import Token, UserRegister, UserResponse

# Tabellen anlegen (falls noch nicht vorhanden)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mein Projekt", version="0.1.0")

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
    # TODO: Implementiert diese Funktion
    # 1. Prüft, ob username oder email bereits existieren (→ 400)
    # 2. Passwort hashen mit get_password_hash()
    # 3. User-Objekt anlegen, in DB speichern, zurückgeben
    raise HTTPException(status_code=501, detail="Noch nicht implementiert")


@app.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    """
    OAuth2 Password Flow: Empfängt username + password als Formular-Daten.
    Gibt einen JWT zurück.
    """
    # TODO: Implementiert diese Funktion
    # 1. Benutzer anhand von form_data.username in der DB suchen
    # 2. Passwort mit verify_password() prüfen (Timing-Schutz: DUMMY_HASH nutzen)
    # 3. Bei Fehler: 401 zurückgeben (generische Meldung!)
    # 4. JWT mit create_access_token() erzeugen und zurückgeben
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Noch nicht implementiert",
    )


@app.get("/my-profile", response_model=UserResponse)
def get_profile(
    current_username: Annotated[str, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """Gibt das Profil des eingeloggten Benutzers zurück (geschützter Endpoint)."""
    # TODO: Implementiert diese Funktion
    # Hinweis: current_username kommt bereits validiert aus dem JWT (via Depends)
    raise HTTPException(status_code=501, detail="Noch nicht implementiert")


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

"""
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

"""

@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).filter(Recipe.is_public == True).all()

"""
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
        ingredients=[i.model_dump() for i in data.ingredients],
        steps=data.steps,
        is_public=data.is_public,
        user_id=user.id
    )

    # save db
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe
"""
@app.post("/recipes", response_model=RecipeResponse)
def create_recipe(
    data: RecipeCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == "testuser").first()
    if not user:
        raise HTTPException(status_code=404, detail="Dummy user not found")

    recipe = Recipe(
        title=data.title,
        description=data.description,
        ingredients=[i.model_dump() for i in data.ingredients],
        steps=data.steps,
        is_public=data.is_public,
        user_id=user.id
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe

# dummy user
@app.on_event("startup")
def create_dummy_user():
    db = SessionLocal()

    user = db.query(User).filter(User.username == "testuser").first()

    if not user:
        user = User(
            username="testuser",
            email="test@test.com",
            hashed_password="dummy"
        )
        db.add(user)
        db.commit()

    db.close()