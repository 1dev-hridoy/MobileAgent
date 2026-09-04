#!/usr/bin/env bash
#
# Harness — Single-command installer
# Usage (on Android/Termux):
#   curl -sL https://raw.githubusercontent.com/1dev-hridoy/MobileAgent/main/harness/install.sh | bash
#
# Usage (on desktop/Linux/macOS):
#   curl -sL https://raw.githubusercontent.com/1dev-hridoy/MobileAgent/main/install.sh | bash
#
set -e

# ── Colors ────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

info()  { echo -e "${CYAN}[*]${NC} $1"; }
ok()    { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
fail()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ── Detect environment ────────────────────────────────────────────────
IS_TERMUX=false
[ -d "/data/data/com.termux" ] && IS_TERMUX=true

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     ⬡ Harness — Mobile Agent Installer   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════╝${NC}"
echo ""

INSTALL_DIR="$HOME/harness"

# ── Termux setup ──────────────────────────────────────────────────────
if [ "$IS_TERMUX" = true ]; then
    info "Detected Termux environment"

    info "Updating packages..."
    pkg update -y && pkg upgrade -y 2>/dev/null || true

    info "Installing dependencies..."
    pkg install -y python git termux-api 2>/dev/null || {
        warn "Some Termux packages may need proot-distro. Continuing..."
    }

    # Check for Termux:API
    if command -v termux-battery-status &>/dev/null; then
        ok "Termux:API found"
    else
        warn "termux-api command not found. Install the Termux:API app from F-Droid."
    fi
else
    info "Detected desktop environment"

    # Check Python
    if command -v python3 &>/dev/null; then
        PYTHON=python3
    elif command -v python &>/dev/null; then
        PYTHON=python
    else
        fail "Python not found. Install Python 3.8+ first."
    fi
    ok "Python found: $($PYTHON --version 2>&1)"

    # Check pip
    if ! $PYTHON -m pip --version &>/dev/null; then
        info "Installing pip..."
        $PYTHON -m ensurepip --upgrade 2>/dev/null || {
            warn "pip not found. Trying to install via package manager..."
            if command -v apt &>/dev/null; then
                sudo apt install -y python3-pip
            elif command -v brew &>/dev/null; then
                brew install python3
            fi
        }
    fi
fi

# ── Clone or update repo ──────────────────────────────────────────────
if [ -d "$INSTALL_DIR/.git" ]; then
    info "Harness already installed. Updating..."
    cd "$INSTALL_DIR" && git pull --rebase || true
else
    info "Cloning MobileAgent to $INSTALL_DIR..."
    git clone https://github.com/1dev-hridoy/MobileAgent.git "$INSTALL_DIR" 2>/dev/null || {
        warn "Clone failed. Creating local installation..."
        mkdir -p "$INSTALL_DIR"
    }
fi

cd "$INSTALL_DIR"

# ── Locate the harness package ────────────────────────────────────────
# Repo may contain the package directly at its root or inside harness/
if [ -d "$INSTALL_DIR/harness" ]; then
    cd "$INSTALL_DIR/harness"
    APP_DIR="$INSTALL_DIR/harness"
else
    APP_DIR="$INSTALL_DIR"
fi

# ── Setup virtual environment ─────────────────────────────────────────
VENV_DIR="$INSTALL_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment..."
    $PYTHON -m venv "$VENV_DIR" 2>/dev/null || python3 -m venv "$VENV_DIR" 2>/dev/null || {
        warn "venv creation failed. Installing globally..."
        VENV_DIR=""
    }
fi

# Activate venv if it exists
if [ -n "$VENV_DIR" ] && [ -d "$VENV_DIR" ]; then
    . "$VENV_DIR/bin/activate"
    ok "Virtual environment activated"
fi

# ── Install Python dependencies ───────────────────────────────────────
info "Installing Python packages..."
pip install --upgrade pip -q 2>/dev/null || true

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    ok "Dependencies installed"
else
    # Install individually if no requirements.txt
    pip install cactus-needle flask pyTelegramBotAPI pydantic waitress -q
    ok "Dependencies installed (manual)"
fi

# ── Done ──────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        ✓ Installation Complete!           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  Run the agent:"
echo -e "    ${CYAN}cd $APP_DIR${NC}"
if [ -n "$VENV_DIR" ]; then
    echo -e "    ${CYAN}source $VENV_DIR/bin/activate${NC}"
fi
echo -e "    ${CYAN}python -m harness              ${NC}  # Interactive CLI"
echo -e "    ${CYAN}python -m harness web          ${NC}  # Web UI"
echo -e "    ${CYAN}python -m harness web 8080     ${NC}  # Custom port"
echo -e "    ${CYAN}python -m harness telegram TOK ${NC}  # Telegram bot"
echo -e "    ${CYAN}python -m harness all          ${NC}  # Web + Telegram"
echo ""
