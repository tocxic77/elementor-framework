#!/usr/bin/env python3
"""Registra el servidor MCP de Elementor Pro de pennacchiotti.cl en Claude.

Uso:
    python configurar-claude-elementor.py            # detecta e informa
    python configurar-claude-elementor.py desktop    # escribe claude_desktop_config.json
    python configurar-claude-elementor.py code       # ejecuta `claude mcp add` (Claude Code CLI)

La credencial se lee de <HERMES_HOME>/.env y nunca se imprime: viaja del archivo al cliente
sin pasar por la consola ni por el historial de la conversación.
"""
import json
import os
import shutil
import subprocess
import sys

ENV = r"C:\Users\mario\AppData\Local\hermes\.env"
KEY_NAME = "MCP_MARIO_PENNACCHIOTTI_ELEMENTOR_API_KEY"
URL = "https://pennacchiotti.cl/wp-json/elementor/mcp/"
DESKTOP_CFG = os.path.join(os.environ["APPDATA"], "Claude", "claude_desktop_config.json")
NOMBRE = "elementor-pro"


def leer_clave() -> str:
    for linea in open(ENV, encoding="utf-8", errors="ignore"):
        if linea.startswith(KEY_NAME + "="):
            return linea.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("No encontré %s en %s" % (KEY_NAME, ENV))


def detectar():
    print("Clave en .env: sí (%d caracteres, oculta)" % len(leer_clave()))
    print("Endpoint: %s" % URL)
    cli = shutil.which("claude")
    print("Claude Code CLI:", cli or "no instalado (npm i -g @anthropic-ai/claude-code)")
    print("Claude Desktop:", "instalado" if os.path.isdir(os.path.dirname(DESKTOP_CFG)) else "no instalado")
    print("Config Desktop:", DESKTOP_CFG, "→", "existe" if os.path.exists(DESKTOP_CFG) else "no existe")


def escribir_desktop():
    clave = leer_clave()
    cfg = {}
    if os.path.exists(DESKTOP_CFG):
        shutil.copy(DESKTOP_CFG, DESKTOP_CFG + ".bak")
        cfg = json.load(open(DESKTOP_CFG, encoding="utf-8"))
    cfg.setdefault("mcpServers", {})[NOMBRE] = {
        "command": "npx",
        "args": ["-y", "mcp-remote", URL, "--header", "Authorization: Basic %s" % clave],
    }
    os.makedirs(os.path.dirname(DESKTOP_CFG), exist_ok=True)
    json.dump(cfg, open(DESKTOP_CFG, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("Escrito %s · servidores: %s" % (DESKTOP_CFG, ", ".join(cfg["mcpServers"])))
    print("Cierra Claude por completo y vuelve a abrirlo.")


def registrar_code():
    clave = leer_clave()
    if not shutil.which("claude"):
        raise SystemExit("Instala primero: npm i -g @anthropic-ai/claude-code")
    cmd = ["claude", "mcp", "add", "--transport", "http", "--scope", "user", NOMBRE, URL,
           "--header", "Authorization: Basic %s" % clave]
    r = subprocess.run(cmd, capture_output=True, text=True)
    salida = (r.stdout + r.stderr).replace(clave, "<clave oculta>")
    print(salida.strip()[:600])
    if r.returncode == 0:
        print("\nVerifica con: claude mcp list")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "detectar"
    {"detectar": detectar, "desktop": escribir_desktop, "code": registrar_code}[modo]()
