import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from gateway import main as gateway
from services.pets import main as pets
from services.preferences import main as preferences


class PetServiceTests(unittest.TestCase):
    def test_filters_pets_by_species_and_energy(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "pets.sqlite3"
            with patch.object(pets, "DB_PATH", database):
                with TestClient(pets.app) as client:
                    response = client.get(
                        "/pets", params={"species": "dog", "energy": "low"}
                    )

        self.assertEqual(response.status_code, 200)
        self.assertEqual([pet["name"] for pet in response.json()], ["Mel"])

    def test_missing_pet_returns_not_found(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "pets.sqlite3"
            with patch.object(pets, "DB_PATH", database):
                with TestClient(pets.app) as client:
                    response = client.get("/pets/999")

        self.assertEqual(response.status_code, 404)
        self.assertIn("não encontrado", response.json()["detail"])


class PreferencesServiceTests(unittest.TestCase):
    def test_new_visitor_receives_safe_default_preferences(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "preferences.sqlite3"
            with patch.object(preferences, "DB_PATH", database):
                with TestClient(preferences.app) as client:
                    response = client.get("/preferences/demo")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["species"], "any")
        self.assertEqual(response.json()["activity_level"], "medium")
        self.assertFalse(response.json()["has_children"])

    def test_preferences_and_favorites_survive_service_restart(self):
        values = {
            "species": "dog",
            "size": "small",
            "activity_level": "low",
            "home_type": "apartment",
            "has_children": False,
        }
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "preferences.sqlite3"
            with patch.object(preferences, "DB_PATH", database):
                with TestClient(preferences.app) as first_run:
                    self.assertEqual(
                        first_run.put("/preferences/demo", json=values).status_code,
                        200,
                    )
                    self.assertEqual(
                        first_run.put("/favorites/demo/1").status_code, 200
                    )
                    self.assertEqual(
                        first_run.put("/favorites/demo/1").json()["saved"], True
                    )

                # A new TestClient context starts a fresh application lifespan.
                with TestClient(preferences.app) as restarted:
                    self.assertEqual(
                        restarted.get("/preferences/demo").json()["species"], "dog"
                    )
                    self.assertEqual(
                        restarted.get("/favorites/demo").json()["pet_ids"], [1]
                    )
                    self.assertEqual(
                        restarted.delete("/favorites/demo/1").json()["saved"], False
                    )
                    self.assertEqual(
                        restarted.get("/favorites/demo").json()["pet_ids"], []
                    )


class GatewayRoutingTests(unittest.TestCase):
    def test_gateway_forwards_pet_filters_to_pets_service(self):
        forwarded = {}

        async def fake_forward(service, path, method="GET", params=None, body=None):
            forwarded.update(
                {"service": service, "path": path, "method": method, "params": params}
            )
            return JSONResponse(
                status_code=200,
                content={"service": service, "filters": params or {}},
            )

        with patch.object(gateway, "forward", new=fake_forward):
            with TestClient(gateway.app) as client:
                response = client.get("/api/pets?species=dog&energy=low")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "pets")
        self.assertEqual(forwarded["path"], "/pets")
        self.assertEqual(forwarded["params"], {"species": "dog", "energy": "low"})


if __name__ == "__main__":
    unittest.main()
