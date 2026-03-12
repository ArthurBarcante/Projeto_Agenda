#!/usr/bin/env bash
# setup.sh — cria e configura o ambiente virtual do projeto AIgenda
set -e

VENV_DIR=".venv"
PYTHON="${PYTHON:-python3}"

# ---------------------------------------------------------------------------
# 1. Cria o .venv se ainda não existir
# ---------------------------------------------------------------------------
if [ ! -d "$VENV_DIR" ]; then
  echo "[setup] Criando ambiente virtual em $VENV_DIR ..."
  "$PYTHON" -m venv "$VENV_DIR"
else
  echo "[setup] Ambiente virtual já existe em $VENV_DIR"
fi

# Ativa o ambiente virtual
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# ---------------------------------------------------------------------------
# 2. Atualiza pip e ferramentas base
# ---------------------------------------------------------------------------
echo "[setup] Atualizando pip, setuptools e wheel ..."
pip install --upgrade pip setuptools wheel --quiet

# ---------------------------------------------------------------------------
# 3. Instala dependências de produção
# ---------------------------------------------------------------------------
echo "[setup] Instalando dependências de produção ..."
pip install -r requirements.txt --quiet

# ---------------------------------------------------------------------------
# 4. Instala dependências de desenvolvimento (opcional)
# ---------------------------------------------------------------------------
if [ "${INSTALL_DEV:-true}" = "true" ]; then
  echo "[setup] Instalando dependências de desenvolvimento ..."
  pip install -e ".[dev]" --quiet
fi

# ---------------------------------------------------------------------------
# 5. Cria .venv/.env a partir de .venv/.env.example (se não existir)
# ---------------------------------------------------------------------------
ENV_FILE="$VENV_DIR/.env"
EXAMPLE_FILE="$VENV_DIR/.env.example"

if [ ! -f "$ENV_FILE" ] && [ -f "$EXAMPLE_FILE" ]; then
  echo "[setup] Criando $ENV_FILE a partir de $EXAMPLE_FILE ..."
  cp "$EXAMPLE_FILE" "$ENV_FILE"
  echo "[setup] ATENÇÃO: edite $ENV_FILE com os valores corretos antes de iniciar a aplicação."
elif [ -f "$ENV_FILE" ]; then
  echo "[setup] $ENV_FILE já existe, pulando cópia."
else
  echo "[setup] AVISO: $EXAMPLE_FILE não encontrado, crie $ENV_FILE manualmente."
fi

echo ""
echo "[setup] Pronto! Ative o ambiente com:"
echo "  source $VENV_DIR/bin/activate"
