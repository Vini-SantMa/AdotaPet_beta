"""Preferências e favoritos de demonstração; este serviço é dono do seu SQLite."""

import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.getenv("PREFERENCES_DB_PATH", ROOT / "data" / "preferences.sqlite3"))


class PreferencesInput(BaseModel):
    species: Literal["any", "dog", "cat"] = "any"
    size: Literal["any", "small", "medium", "large"] = "any"
    activity_level: Literal["low", "medium", "high"] = "medium"
    home_type: Literal["apartment", "house"] = "apartment"
    has_children: bool = False


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with connect() as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS preferences (
                visitor_id TEXT PRIMARY KEY,
                species TEXT NOT NULL,
                size TEXT NOT NULL,
                activity_level TEXT NOT NULL,
                home_type TEXT NOT NULL,
                has_children INTEGER NOT NULL
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS favorites (
                visitor_id TEXT NOT NULL,
                pet_id INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (visitor_id, pet_id)
            )"""
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Patinhas — Microserviço de Preferências e Favoritos",
    description="Persiste preferências e pets favoritos para a demonstração, sem conta de usuário.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["Operação"])
def health() -> dict:
    return {"status": "ok", "service": "preferences"}


@app.get("/preferences/{visitor_id}", tags=["Preferências"])
def get_preferences(visitor_id: str) -> dict:
    with connect() as db:
        row = db.execute(
            "SELECT * FROM preferences WHERE visitor_id = ?", (visitor_id,)
        ).fetchone()
    if row is None:
        return {
            "visitor_id": visitor_id,
            "species": "any",
            "size": "any",
            "activity_level": "medium",
            "home_type": "apartment",
            "has_children": False,
        }
    preferences = dict(row)
    preferences["has_children"] = bool(preferences["has_children"])
    return preferences


@app.put("/preferences/{visitor_id}", tags=["Preferências"])
def save_preferences(visitor_id: str, preferences: PreferencesInput) -> dict:
    values = preferences.model_dump()
    with connect() as db:
        db.execute(
            """INSERT INTO preferences
               (visitor_id, species, size, activity_level, home_type, has_children)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(visitor_id) DO UPDATE SET
                 species=excluded.species,
                 size=excluded.size,
                 activity_level=excluded.activity_level,
                 home_type=excluded.home_type,
                 has_children=excluded.has_children""",
            (
                visitor_id,
                values["species"],
                values["size"],
                values["activity_level"],
                values["home_type"],
                int(values["has_children"]),
            ),
        )
    return {"visitor_id": visitor_id, **values}


@app.get("/favorites/{visitor_id}", tags=["Favoritos"])
def list_favorites(visitor_id: str) -> dict:
    with connect() as db:
        rows = db.execute(
            "SELECT pet_id FROM favorites WHERE visitor_id = ? ORDER BY created_at DESC",
            (visitor_id,),
        ).fetchall()
    return {"visitor_id": visitor_id, "pet_ids": [row["pet_id"] for row in rows]}


@app.put("/favorites/{visitor_id}/{pet_id}", tags=["Favoritos"])
def add_favorite(visitor_id: str, pet_id: int) -> dict:
    with connect() as db:
        db.execute(
            "INSERT OR IGNORE INTO favorites (visitor_id, pet_id) VALUES (?, ?)",
            (visitor_id, pet_id),
        )
    return {"visitor_id": visitor_id, "pet_id": pet_id, "saved": True}


@app.delete("/favorites/{visitor_id}/{pet_id}", tags=["Favoritos"])
def remove_favorite(visitor_id: str, pet_id: int) -> dict:
    with connect() as db:
        db.execute(
            "DELETE FROM favorites WHERE visitor_id = ? AND pet_id = ?",
            (visitor_id, pet_id),
        )
    return {"visitor_id": visitor_id, "pet_id": pet_id, "saved": False}
