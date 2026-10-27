"""Compatibilidade transparente: consulta APIs de Pets e Preferências via HTTP."""

import os

import httpx
from fastapi import FastAPI, HTTPException

PETS_URL = os.getenv("PETS_SERVICE_URL", "http://127.0.0.1:8001")
PREFERENCES_URL = os.getenv("PREFERENCES_SERVICE_URL", "http://127.0.0.1:8002")

app = FastAPI(
    title="Patinhas — Microserviço de Recomendações",
    description="Ordena pets por compatibilidade usando regras simples e explicáveis.",
    version="1.0.0",
)


@app.get("/health", tags=["Operação"])
def health() -> dict:
    return {"status": "ok", "service": "recommendations"}


def score_pet(pet: dict, preferences: dict) -> dict:
    score = 0
    reasons: list[str] = []

    species = preferences["species"]
    if species == "any" or species == pet["species"]:
        score += 25
        reasons.append("A espécie está de acordo com o que você procura.")
    else:
        reasons.append("A espécie não coincide com a preferência escolhida.")

    size = preferences["size"]
    if size == "any" or size == pet["size"]:
        score += 20
        reasons.append("O porte combina com sua preferência.")
    else:
        reasons.append("O porte é diferente do que você selecionou.")

    preferred_activity = preferences["activity_level"]
    energy = pet["energy_level"]
    activity_points = {
        "low": {"low": 30, "medium": 19, "high": 8},
        "medium": {"low": 19, "medium": 30, "high": 19},
        "high": {"low": 8, "medium": 19, "high": 30},
    }
    score += activity_points[preferred_activity][energy]
    if preferred_activity == energy:
        reasons.append("O nível de energia combina com a sua rotina.")
    else:
        reasons.append("Considere se o nível de energia combina com a sua rotina.")

    home_type = preferences["home_type"]
    if home_type == "house" or pet["size"] in ("small", "medium"):
        score += 15
        reasons.append("As características do pet podem se adaptar ao tipo de moradia informado.")
    else:
        reasons.append("O porte pode exigir mais espaço do que um apartamento costuma oferecer.")

    if not preferences["has_children"] or pet["good_with_children"]:
        score += 10
        reasons.append("O perfil informado é compatível com a convivência com crianças.")
    else:
        reasons.append("O perfil do pet indica cautela na convivência com crianças.")

    label = "Ótima combinação" if score >= 80 else "Pode combinar" if score >= 60 else "Vale conhecer melhor"
    return {"pet": pet, "score": score, "label": label, "reasons": reasons}


@app.get("/recommendations/{visitor_id}", tags=["Recomendações"])
async def get_recommendations(visitor_id: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            pets_response = await client.get(f"{PETS_URL}/pets")
            preferences_response = await client.get(
                f"{PREFERENCES_URL}/preferences/{visitor_id}"
            )
            pets_response.raise_for_status()
            preferences_response.raise_for_status()
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail="Não foi possível consultar os serviços de Pets e Preferências.",
        ) from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail="Um serviço interno respondeu com erro ao calcular recomendações.",
        ) from exc

    pets = pets_response.json()
    preferences = preferences_response.json()
    recommendations = [score_pet(pet, preferences) for pet in pets]
    recommendations.sort(key=lambda item: item["score"], reverse=True)
    return {
        "visitor_id": visitor_id,
        "preferences": preferences,
        "recommendations": recommendations,
    }
