"""Catálogo demonstrativo de animais; este serviço é dono do seu banco SQLite."""

import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.getenv("PETS_DB_PATH", ROOT / "data" / "pets.sqlite3"))

SEED_PETS = [
    {
        "id": 1,
        "name": "Mel",
        "species": "dog",
        "age_years": 2,
        "size": "small",
        "energy_level": "low",
        "temperament": "Carinhosa e tranquila",
        "story": "A Mel adora caminhadas curtas, cochilos ao sol e companhia por perto.",
        "good_with_children": True,
        "good_with_dogs": True,
        "good_with_cats": True,
        "image_url": "/manus-storage/async-images/OfSFQyI0WM9hSBA9GCwGff/image-3.webp",
    },
    {
        "id": 2,
        "name": "Toto",
        "species": "cat",
        "age_years": 1,
        "size": "small",
        "energy_level": "medium",
        "temperament": "Curioso e brincalhão",
        "story": "O Toto gosta de explorar cantinhos novos e depois descansar perto da janela.",
        "good_with_children": True,
        "good_with_dogs": True,
        "good_with_cats": True,
        "image_url": "/manus-storage/async-images/OfSFQyI0WM9hSBA9GCwGff/image-4.webp",
    },
    {
        "id": 3,
        "name": "Nina",
        "species": "cat",
        "age_years": 6,
        "size": "medium",
        "energy_level": "low",
        "temperament": "Observadora e companheira",
        "story": "A Nina prefere ambientes calmos e uma boa sessão de carinho no fim do dia.",
        "good_with_children": True,
        "good_with_dogs": False,
        "good_with_cats": False,
        "image_url": "/manus-storage/async-images/OfSFQyI0WM9hSBA9GCwGff/image-5.webp",
    },
]


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with connect() as db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                age_years REAL NOT NULL,
                size TEXT NOT NULL,
                energy_level TEXT NOT NULL,
                temperament TEXT NOT NULL,
                story TEXT NOT NULL,
                good_with_children INTEGER NOT NULL,
                good_with_dogs INTEGER NOT NULL,
                good_with_cats INTEGER NOT NULL,
                image_url TEXT NOT NULL
            )"""
        )
        count = db.execute("SELECT COUNT(*) FROM pets").fetchone()[0]
        if count == 0:
            db.executemany(
                """INSERT INTO pets
                (id, name, species, age_years, size, energy_level, temperament,
                 story, good_with_children, good_with_dogs, good_with_cats, image_url)
                VALUES (:id, :name, :species, :age_years, :size, :energy_level,
                        :temperament, :story, :good_with_children, :good_with_dogs,
                        :good_with_cats, :image_url)""",
                [
                    {
                        **pet,
                        "good_with_children": int(pet["good_with_children"]),
                        "good_with_dogs": int(pet["good_with_dogs"]),
                        "good_with_cats": int(pet["good_with_cats"]),
                    }
                    for pet in SEED_PETS
                ],
            )


def serialize(row: sqlite3.Row) -> dict:
    pet = dict(row)
    for key in ("good_with_children", "good_with_dogs", "good_with_cats"):
        pet[key] = bool(pet[key])
    return pet


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Patinhas — Microserviço de Pets",
    description="Catálogo demonstrativo de animais fictícios para adoção.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["Operação"])
def health() -> dict:
    return {"status": "ok", "service": "pets"}


@app.get("/pets", tags=["Pets"])
def list_pets(
    species: Literal["dog", "cat"] | None = None,
    size: Literal["small", "medium", "large"] | None = None,
    age: Literal["young", "adult", "senior"] | None = None,
    energy: Literal["low", "medium", "high"] | None = None,
    limit: int = Query(default=50, ge=1, le=100),
) -> list[dict]:
    clauses: list[str] = []
    values: list[object] = []
    if species:
        clauses.append("species = ?")
        values.append(species)
    if size:
        clauses.append("size = ?")
        values.append(size)
    if energy:
        clauses.append("energy_level = ?")
        values.append(energy)
    if age == "young":
        clauses.append("age_years < 3")
    elif age == "adult":
        clauses.append("age_years >= 3 AND age_years < 8")
    elif age == "senior":
        clauses.append("age_years >= 8")

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with connect() as db:
        rows = db.execute(
            f"SELECT * FROM pets {where} ORDER BY name LIMIT ?",
            [*values, limit],
        ).fetchall()
    return [serialize(row) for row in rows]


@app.get("/pets/{pet_id}", tags=["Pets"])
def get_pet(pet_id: int) -> dict:
    with connect() as db:
        row = db.execute("SELECT * FROM pets WHERE id = ?", (pet_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado no catálogo de demonstração.")
    return serialize(row)
