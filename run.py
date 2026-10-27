"""Inicializa os serviços independentes do Patinhas para a demonstração local."""

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INTERNAL_SERVICES = [
    ("services.pets.main:app", 8001),
    ("services.preferences.main:app", 8002),
    ("services.recommendations.main:app", 8003),
]


def wait_until_ready() -> None:
    deadline = time.monotonic() + 18
    pending = {port for _, port in INTERNAL_SERVICES}
    while pending and time.monotonic() < deadline:
        for port in list(pending):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=0.5) as response:
                    if response.status == 200:
                        pending.discard(port)
            except (urllib.error.URLError, TimeoutError):
                pass
        if pending:
            time.sleep(0.25)
    if pending:
        print(f"Aviso: alguns serviços ainda não responderam: {sorted(pending)}", flush=True)


def main() -> None:
    os.chdir(ROOT)
    children: list[subprocess.Popen] = []
    try:
        for module, port in INTERNAL_SERVICES:
            command = [
                sys.executable, "-m", "uvicorn", module,
                "--host", "127.0.0.1", "--port", str(port), "--log-level", "warning",
            ]
            children.append(subprocess.Popen(command, cwd=ROOT))
        wait_until_ready()
        gateway_port = int(os.getenv("PORT", "3000"))
        print(f"Patinhas: API Gateway ouvindo na porta {gateway_port}.", flush=True)
        import uvicorn
        uvicorn.run("gateway.main:app", host="0.0.0.0", port=gateway_port, log_level="info")
    except KeyboardInterrupt:
        print("Encerrando Patinhas...", flush=True)
    finally:
        for process in children:
            if process.poll() is None:
                process.terminate()
        for process in children:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    main()
