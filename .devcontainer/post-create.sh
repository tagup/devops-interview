#!/bin/bash
set -euo pipefail

cat .devcontainer/.bashrc.sh >> "$HOME/.bashrc"

sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql-client curl ca-certificates

curl -LsSf https://astral.sh/uv/install.sh | sh
