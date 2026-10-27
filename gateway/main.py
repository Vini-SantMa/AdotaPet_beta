"""Gateway público do sistema: interface web, proxy das APIs e estado dos serviços."""

import asyncio
import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"
SERVICES = {
    "pets": os.getenv("PETS_SERVICE_URL", "http://127.0.0.1:8001"),
    "preferences": os.getenv("PREFERENCES_SERVICE_URL", "http://127.0.0.1:8002"),
    "recommendations": os.getenv("RECOMMENDATIONS_SERVICE_URL", "http://127.0.0.1:8003"),
}

app = FastAPI(
    title="Patinhas — API Gateway",
    description="Ponto de entrada da interface para os microserviços Pets, Preferências e Recomendações.",
    version="1.0.0",
)


async def forward(service: str, path: str, method: str = "GET", params=None, body=None):
    url = f"{SERVICES[service]}{path}"
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            response = await client.request(method, url, params=params, json=body)
        try:
            payload = response.json()
        except ValueError:
            payload = {"detail": "O serviço retornou uma resposta inválida."}
        return JSONResponse(status_code=response.status_code, content=payload)
    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"detail": f"O microserviço {service} está indisponível no momento."},
        )


@app.get("/api/pets", tags=["Gateway"])
async def list_pets(species: str | None = None, size: str | None = None,
                    age: str | None = None, energy: str | None = None):
    params = {key: value for key, value in {
        "species": species, "size": size, "age": age, "energy": energy
    }.items() if value}
    return await forward("pets", "/pets", params=params)


@app.get("/api/pets/{pet_id}", tags=["Gateway"])
async def get_pet(pet_id: int):
    return await forward("pets", f"/pets/{pet_id}")


@app.get("/api/preferences", tags=["Gateway"])
async def get_preferences(visitor_id: str = "demo"):
    return await forward("preferences", f"/preferences/{visitor_id}")


@app.put("/api/preferences", tags=["Gateway"])
async def save_preferences(request: Request, visitor_id: str = "demo"):
    body = await request.json()
    return await forward("preferences", f"/preferences/{visitor_id}", "PUT", body=body)


@app.get("/api/favorites", tags=["Gateway"])
async def get_favorites(visitor_id: str = "demo"):
    return await forward("preferences", f"/favorites/{visitor_id}")


@app.put("/api/favorites/{pet_id}", tags=["Gateway"])
async def add_favorite(pet_id: int, visitor_id: str = "demo"):
    return await forward("preferences", f"/favorites/{visitor_id}/{pet_id}", "PUT")


@app.delete("/api/favorites/{pet_id}", tags=["Gateway"])
async def remove_favorite(pet_id: int, visitor_id: str = "demo"):
    return await forward("preferences", f"/favorites/{visitor_id}/{pet_id}", "DELETE")


@app.get("/api/recommendations", tags=["Gateway"])
async def get_recommendations(visitor_id: str = "demo"):
    return await forward("recommendations", f"/recommendations/{visitor_id}")


@app.get("/manus-routes.json", include_in_schema=False)
def route_manifest():
    return FileResponse(ROOT / "public" / "manus-routes.json", media_type="application/json")


@app.get("/api/status", tags=["Gateway"])
async def service_status():
    async def check(name: str, url: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=1.5) as client:
                response = await client.get(f"{url}/health")
            online = response.is_success
        except httpx.RequestError:
            online = False
        return {
            "id": name,
            "name": {
                "pets": "Microserviço Pets",
                "preferences": "Microserviço Preferências/Favoritos",
                "recommendations": "Microserviço Recomendações",
            }[name],
            "status": "online" if online else "offline",
            "docs_url": f"/api/docs/{name}",
        }

    results = await asyncio.gather(*(check(name, url) for name, url in SERVICES.items()))
    return {"gateway": "online", "services": results}


@app.get("/api/openapi/{service_name}.json", include_in_schema=False)
async def service_openapi(service_name: str):
    if service_name not in SERVICES:
        return JSONResponse(status_code=404, content={"detail": "Serviço não encontrado."})
    return await forward(service_name, "/openapi.json")


@app.get("/api/docs/{service_name}", include_in_schema=False)
async def service_docs(service_name: str):
    if service_name not in SERVICES:
        return HTMLResponse("Serviço não encontrado.", status_code=404)
    return get_swagger_ui_html(
        openapi_url=f"/api/openapi/{service_name}.json",
        title=f"Patinhas — Documentação {service_name}",
    )


# APIs definidas acima têm precedência sobre esta montagem da interface estática.
app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
