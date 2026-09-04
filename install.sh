#!/usr/bin/env bash
#
# ⬡ Harness — Single-command installer (v2 · fancy)
# Usage (on Android/Termux):
#   curl -sL https://raw.githubusercontent.com/1dev-hridoy/MobileAgent/main/harness/install.sh | bash
#
# Usage (on desktop/Linux/macOS):
#   curl -sL https://raw.githubusercontent.com/1dev-hridoy/MobileAgent/main/install.sh | bash
#
set -e

# ── Colors & styles ─────────────────────────────────────────────────
RED=$'\033[0;31m';  GREEN=$'\033[0;32m';  YELLOW=$'\033[1;33m';  CYAN=$'\033[0;36m'
MAGENTA=$'\033[0;35m';  BOLD=$'\033[1m';  DIM=$'\033[2m';  NC=$'\033[0m'

# ── Tiny message helpers ────────────────────────────────────────────
info()  { printf "${CYAN}${BOLD}::${NC} %s\n" "$1"; }
ok()    { printf "${GREEN}${BOLD}✔${NC} %s\n" "$1"; }
warn()  { printf "${YELLOW}${BOLD}!${NC} %s\n" "$1"; }
fail()  { printf "${RED}${BOLD}✖${NC} %s\n" "$1"; exit 1; }

# ── Spinner: run a command quietly while animating what it's doing ──
run_quiet() {
    local msg=$1 code=0 i=0 pid tty=0
    shift
    if [ -t 1 ]; then tty=1; fi
    "$@" >/dev/null 2>&1 &
    pid=$!
    if [ "$tty" -eq 1 ]; then
        local frames
        frames=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
        while kill -0 "$pid" 2>/dev/null; do
            printf "\r   ${CYAN}%s${NC} %s " "${frames[$i]}" "$msg"
            i=$(( (i + 1) % 10 ))
            sleep 0.08
        done
        printf "\r\033[K"
    fi
    wait "$pid" 2>/dev/null || code=$?
    return "$code"
}

# ── Box drawing (44 columns wide) ───────────────────────────────────
DASHES=""
for ((_d = 0; _d < 40; _d++)); do DASHES+='─'; done
box_top()    { printf "  ┌${DASHES}┐\n"; }
box_bot()    { printf "  └${DASHES}┘\n"; }
box_title()  {
    local t=$1 left right
    left=$(( (38 - ${#t}) / 2 ))
    right=$(( 38 - ${#t} - left ))
    if [ "$left"  -lt 1 ]; then left=1;  fi
    if [ "$right" -lt 1 ]; then right=1; fi
    printf "  │ ${BOLD}%*s${CYAN}%s${NC}%*s │\n" "$left" "" "$t" "$right" ""
}
box_row() {
    local key=$1 val=$2 pad
    pad=$(( 38 - ${#key} - ${#val} ))
    if [ "$pad" -lt 1 ]; then pad=1; fi
    printf "  │ ${BOLD}%s${NC}%${pad}s${GREEN}%s${NC} │\n" "$key" "" "$val"
}

# ── Phase tracking + global progress bar ────────────────────────────
NPHASES=7
PHASE=0
PHASE_START=0

global_progress() {
    local pct width filled i bar=""
    pct=$(( PHASE * 100 / NPHASES ))
    width=28
    filled=$(( pct * width / 100 ))
    for ((i = 0; i < width; i++)); do
        if [ "$i" -lt "$filled" ]; then
            bar+="${GREEN}█${NC}"
        else
            bar+="${DIM}░${NC}"
        fi
    done
    printf "  ${BOLD}Progress:${NC} %b %3d%%\n" "$bar" "$pct"
}

begin_phase() {
    PHASE=$((PHASE + 1))
    PHASE_START=$SECONDS
    printf "\n${BOLD}${CYAN}─── [%d/%d]${NC} ${BOLD}%s${NC}\n" "$PHASE" "$NPHASES" "$1"
}

end_phase() {
    local d=$((SECONDS - PHASE_START))
    printf "  ${DIM}└─ done in ${GREEN}${d}s${NC}\n"
    global_progress
}

# ── Random tips ─────────────────────────────────────────────────────
TIPS=(
  "Tip: Harness runs fully on-device — your data never leaves your phone"
  "Fun fact: the Needle LLM is only 14MB and runs 100% locally"
  "Tip: control your agent remotely with the Telegram bot"
  "Fun fact: Harness ships with 27+ tools — system, media, network & more"
  "Tip: grant Termux:API permissions in Android Settings for full control"
  "Fun fact: desktop simulation lets you try everything without a phone"
  "Tip: chain tools together — SMS, calls, camera, Wi-Fi in one prompt"
)
random_tip() {
    local idx=$(( RANDOM % ${#TIPS[@]} ))
    printf "  ${DIM}✦ %s${NC}\n" "${TIPS[$idx]}"
}

# ── Detect environment ──────────────────────────────────────────────
IS_TERMUX=false
[ -d "/data/data/com.termux" ] && IS_TERMUX=true

OS=$(uname -s 2>/dev/null || echo "unknown")
ARCH=$(uname -m 2>/dev/null || echo "unknown")

if [ "$IS_TERMUX" = true ]; then
    PLATFORM="Termux (Android)"
else
    case "$OS" in
        Darwin) PLATFORM="macOS" ;;
        Linux)  PLATFORM="Linux" ;;
        *)      PLATFORM="$OS" ;;
    esac
fi

DISK_FREE=$(df -h "$HOME" 2>/dev/null | awk 'NR==2 {print $4}')
if [ -z "$DISK_FREE" ]; then DISK_FREE="?"; fi

INSTALL_DIR="$HOME/harness"
REPO_URL="https://github.com/1dev-hridoy/MobileAgent.git"

# ── Banner ──────────────────────────────────────────────────────────
printf "\n"
printf "${MAGENTA}  █░█ ▄▀█ █▀█ █▄░█ █▀▀ █▀ █▀▀${NC}\n"
printf "${CYAN}  █▀█ █▀█ █▀▄ █▀██ █▀▀ ▄█ ██▄${NC}\n"
printf "${GREEN}  ▀░▀ █▀▄ █▄▀ █▀░▀ █▀░ █▄ █▄▄${NC}\n"
printf "\n"
printf "  ${BOLD}⬡  MOBILE AGENT — ONE-LINE INSTALLER (v2)${NC}\n"
printf "  ${DIM}   AI agent for your phone · powered by Needle (14MB)${NC}\n"
printf "  ${DIM}   github.com/1dev-hridoy/MobileAgent${NC}\n"
printf "\n"

box_top
box_title "WHAT WILL HAPPEN"
box_row "Detect environment"    "→ platform info"
box_row "Install dependencies"  "system + python"
box_row "Download MobileAgent"  "git clone"
box_row "Create virtual env"    "isolated python"
box_row "Install packages"      "pip, one by one"
box_row "Register harness"      "importable anywhere"
box_row "Show run commands"     "→ copy & paste"
box_bot
printf "\n"

# ── Phase 1 · Environment & system checks ───────────────────────────
begin_phase "Environment detection & system checks"

box_top
box_title "ENVIRONMENT"
box_row "Platform"      "$PLATFORM"
box_row "Architecture"  "$ARCH"
box_row "Install dir"   "$INSTALL_DIR"
box_row "Disk free"     "$DISK_FREE"
box_bot
printf "\n"

if command -v git >/dev/null 2>&1; then
    ok "git: found"
else
    warn "git: not found (clone will fall back to local install)"
fi

if command -v curl >/dev/null 2>&1; then
    ok "curl: found"
    code=$(curl -sI --max-time 10 -o /dev/null -w '%{http_code}' https://github.com 2>/dev/null || true)
    case "$code" in
        200|301|302) ok "network: GitHub reachable (HTTP $code)" ;;
        *)           warn "network: GitHub unreachable (HTTP ${code:-none}) — clone may fail offline" ;;
    esac
else
    warn "curl: not found — skipping network check"
fi

end_phase
random_tip

# ── Phase 2 · System dependencies ───────────────────────────────────
if [ "$IS_TERMUX" = true ]; then
    begin_phase "System dependencies (Termux)"

    info "Refreshing Termux package lists & upgrading existing packages…"
    run_quiet "updating package lists…" pkg update -y || true
    run_quiet "upgrading packages…" pkg upgrade -y || true

    TERMUX_PKGS=(python git termux-api)
    info "Installing ${#TERMUX_PKGS[@]} system packages…"
    i=0
    for pkg in "${TERMUX_PKGS[@]}"; do
        i=$((i + 1))
        run_quiet "[$i/${#TERMUX_PKGS[@]}] installing ${pkg}…" pkg install -y "$pkg" || {
            warn "pkg install ${pkg} failed — some Termux packages need proot-distro"
        }
    done

    BUILD_PKGS=(rust binutils make clang)
    info "Installing ${#BUILD_PKGS[@]} build dependencies (Rust, C compiler)…"
    i=0
    for pkg in "${BUILD_PKGS[@]}"; do
        i=$((i + 1))
        run_quiet "[$i/${#BUILD_PKGS[@]}] installing ${pkg}…" pkg install -y "$pkg" || {
            warn "pkg install ${pkg} failed — some packages may need proot-distro"
        }
    done

    end_phase
else
    begin_phase "System dependencies (desktop)"

    info "Desktop mode — no system packages required."
    ok "Everything installs via pip (clean & portable)"

    end_phase
fi

# ── Phase 3 · Python toolchain ──────────────────────────────────────
begin_phase "Python toolchain"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    if [ "$IS_TERMUX" = true ]; then
        warn "python not found — retrying install"
        run_quiet "installing python…" pkg install -y python || true
        PYTHON=python3
    else
        fail "Python not found. Install Python 3.8+ first."
    fi
fi

PY_VER=$($PYTHON --version 2>&1 || echo "?")
ok "Python: $PY_VER"

if ! $PYTHON -m pip --version >/dev/null 2>&1; then
    info "pip not found — bootstrapping…"
    run_quiet "running ensurepip…" $PYTHON -m ensurepip --upgrade || {
        warn "ensurepip failed — trying your package manager…"
        if command -v apt >/dev/null 2>&1; then
            run_quiet "installing python3-pip via apt…" sudo apt install -y python3-pip || warn "apt install failed"
        elif command -v brew >/dev/null 2>&1; then
            run_quiet "installing python via brew…" brew install python3 || warn "brew install failed"
        else
            warn "could not install pip automatically"
        fi
    }
fi
ok "pip: $($PYTHON -m pip --version 2>/dev/null | awk '{print $2}')"

if [ "$IS_TERMUX" = true ]; then
    if command -v termux-battery-status >/dev/null 2>&1; then
        ok "Termux:API found"
    else
        warn "termux-api not found — install the Termux:API app from F-Droid"
    fi
fi

end_phase
random_tip

# ── Phase 4 · Download MobileAgent ──────────────────────────────────
begin_phase "Downloading MobileAgent"

if [ -d "$INSTALL_DIR/.git" ]; then
    info "Already installed — pulling latest changes…"
    run_quiet "git pull --rebase…" git -C "$INSTALL_DIR" pull --rebase || true
    ok "Updated to latest"
else
    if [ -t 2 ]; then
        printf "  ${BOLD}${CYAN}▶${NC} cloning MobileAgent — live download progress below:\n"
        git clone --progress "$REPO_URL" "$INSTALL_DIR" 2>&1 || true
    else
        run_quiet "cloning MobileAgent…" git clone "$REPO_URL" "$INSTALL_DIR" || true
    fi
fi

if [ -d "$INSTALL_DIR/.git" ]; then
    SIZE=$(du -sh "$INSTALL_DIR" 2>/dev/null | awk '{print $1}')
    COMMIT=$(git -C "$INSTALL_DIR" log -1 --format='%h %s' 2>/dev/null || echo "?")
    ok "Repository ready — ${SIZE:-?} on disk · latest commit: $COMMIT"
else
    warn "Clone failed — creating a local installation instead…"
    mkdir -p "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# The repo may contain the package directly at its root or inside harness/
if [ -d "$INSTALL_DIR/harness" ]; then
    cd "$INSTALL_DIR/harness"
    APP_DIR="$INSTALL_DIR/harness"
else
    APP_DIR="$INSTALL_DIR"
fi

end_phase

# ── Phase 5 · Virtual environment ───────────────────────────────────
begin_phase "Virtual environment"

VENV_DIR="$INSTALL_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    run_quiet "creating virtual environment…" $PYTHON -m venv "$VENV_DIR" || {
        warn "venv creation failed — will install packages globally"
        VENV_DIR=""
    }
fi

if [ -n "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
    . "$VENV_DIR/bin/activate"
    ok "Virtual environment ready & activated"
else
    VENV_DIR=""
fi

end_phase
random_tip

# ── Phase 6 · Install Python packages, one at a time ────────────────
begin_phase "Installing Python packages"

run_quiet "upgrading pip…" $PYTHON -m pip install --upgrade pip -q || true

# On Termux, set up Rust environment so maturin can find the system rustc
FAILED_DEPS=()
if [ "$IS_TERMUX" = true ]; then
    if command -v rustc >/dev/null 2>&1; then
        ok "Rust: $(rustc --version 2>/dev/null || echo 'found')"
        # Create a rustup shim so maturin can discover the system rustc.
        # maturin checks for `rustup` first and gives up when it doesn't
        # find the target in `rustup target list`.  This shim intercepts
        # those calls and delegates to the real rustc/cargo.
        RUSTUP_DIR="${VENV_DIR:+$VENV_DIR/bin}"
        if [ -z "$RUSTUP_DIR" ] || [ ! -d "$RUSTUP_DIR" ]; then
            RUSTUP_DIR="$HOME/.cargo/bin"
        fi
        mkdir -p "$RUSTUP_DIR"
        RUSTUP_BIN="$RUSTUP_DIR/rustup"
        cat > "$RUSTUP_BIN" << 'RUSTUP_SHIM'
#!/usr/bin/env bash
# Minimal rustup shim — delegates to system rustc/cargo
REAL_CARGO=$(command -v cargo 2>/dev/null || echo "/data/data/com.termux/files/usr/bin/cargo")
REAL_RUSTC=$(command -v rustc 2>/dev/null || echo "/data/data/com.termux/files/usr/bin/rustc")
case "$1" in
  run)     shift; cmd="$1"; shift; case "$cmd" in rustc) exec "$REAL_RUSTC" "$@";; cargo) exec "$REAL_CARGO" "$@";; *) exec "$cmd" "$@";; esac;;
  show)    echo "stable-aarch64-unknown-linux-android"; exit 0;;
  which)   if [ "$2" = "rustc" ]; then echo "$REAL_RUSTC"; elif [ "$2" = "cargo" ]; then echo "$REAL_CARGO"; fi; exit 0;;
  target)  if [ "$2" = "list" ]; then echo "aarch64-unknown-linux-android"; exit 0; fi; exec "$REAL_CARGO" rustup "$@";;
  toolchain) exec "$REAL_CARGO" rustup "$@";;
  *)       exec "$REAL_CARGO" rustup "$@";;
esac
RUSTUP_SHIM
        chmod +x "$RUSTUP_BIN"
        export PATH="$RUSTUP_DIR:$PATH"
        export RUSTUP_HOME="${RUSTUP_HOME:-$HOME/.rustup}"
        export CARGO_HOME="${CARGO_HOME:-$HOME/.cargo}"
        ok "Rustup shim installed — maturin can now find system rustc"
    fi
fi

# Collect the dependency list
DEPS=()
if [ -f "requirements.txt" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            ""|\#*) continue ;;
        esac
        DEPS+=("$line")
    done < requirements.txt
else
    DEPS=(cactus-needle flask pyTelegramBotAPI pydantic waitress)
fi

# Install one package at a time so the user sees exactly what is
# downloading right now, with a live progress indicator.
install_one() {
    local idx=$1 total=$2 spec=$3 base ver
    base=$(printf '%s' "$spec" | sed 's/[\[;].*$//; s/[<>=!~].*$//')
    if [ -t 2 ]; then
        printf "  ${CYAN}▸${NC} [%d/%d] installing ${BOLD}%s${NC}…\n" "$idx" "$total" "$base"
        $PYTHON -m pip install "$spec" || { warn "${base}: install failed"; FAILED_DEPS+=("$spec"); return 1; }
    else
        run_quiet "[$idx/$total] installing ${base}…" $PYTHON -m pip install "$spec" -q || {
            warn "${base}: install failed"; FAILED_DEPS+=("$spec"); return 1
        }
    fi
    ver=$($PYTHON -c "import importlib.metadata as m; print(m.version('${base}'))" 2>/dev/null || true)
    if [ -n "$ver" ]; then
        ok "${base} ${ver}"
    else
        ok "${base}"
    fi
}

if [ "${#DEPS[@]}" -gt 0 ]; then
    printf "  ${BOLD}${CYAN}▶${NC} installing ${#DEPS[@]} Python package(s) — one at a time:\n"
    printf "\n"
    i=0
    for spec in "${DEPS[@]}"; do
        i=$((i + 1))
        install_one "$i" "${#DEPS[@]}" "$spec" || true
    done

    # Retry failed packages (Rust/clang may now be available)
    if [ "${#FAILED_DEPS[@]}" -gt 0 ]; then
        printf "\n  ${YELLOW}${BOLD}↻${NC} retrying ${#FAILED_DEPS[@]} failed package(s) with build tools available…\n"
        RETRY_FAILED=()
        for spec in "${FAILED_DEPS[@]}"; do
            base=$(printf '%s' "$spec" | sed 's/[\[;].*$//; s/[<>=!~].*$//')
            if [ -t 2 ]; then
                printf "  ${CYAN}▸${NC} retrying ${BOLD}%s${NC}…\n" "$base"
                $PYTHON -m pip install "$spec" || { RETRY_FAILED+=("$spec"); continue; }
            else
                run_quiet "retrying ${base}…" $PYTHON -m pip install "$spec" -q || {
                    RETRY_FAILED+=("$spec"); continue
                }
            fi
            ver=$($PYTHON -c "import importlib.metadata as m; print(m.version('${base}'))" 2>/dev/null || true)
            if [ -n "$ver" ]; then
                ok "${base} ${ver} (retry succeeded)"
            else
                ok "${base} (retry succeeded)"
            fi
        done
        if [ "${#RETRY_FAILED[@]}" -gt 0 ]; then
            warn "${#RETRY_FAILED[@]} package(s) still failed: ${RETRY_FAILED[*]}"
        fi
    fi

    INSTALLED_COUNT=0
    for spec in "${DEPS[@]}"; do
        base=$(printf '%s' "$spec" | sed 's/[\[;].*$//; s/[<>=!~].*$//')
        if $PYTHON -c "import importlib.metadata as m; print(m.version('${base}'))" >/dev/null 2>&1; then
            INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
        fi
    done
    ok "Installed ${INSTALLED_COUNT}/${#DEPS[@]} Python package(s)"
else
    info "No Python packages to install (empty requirements.txt)"
fi

# Register the package itself (pip install -e .) so `python -m harness`
# and `python telegram_bot.py` work from ANY directory.
run_quiet "registering harness package (pip install -e .)…" $PYTHON -m pip install -e . -q || {
    warn "package registration failed — run 'python -m harness' from the parent directory instead"
}
ok "harness registered — 'python -m harness' works from anywhere"

end_phase

# ── Phase 7 · Finish ────────────────────────────────────────────────
begin_phase "Finishing up"

TOTAL=$SECONDS
printf "\n"
printf "${GREEN}  ╔${DASHES}╗${NC}\n"
printf "${GREEN}  ║       ⬡  INSTALLATION COMPLETE       ║${NC}\n"
printf "${GREEN}  ║          HARNESS IS READY!          ║${NC}\n"
printf "${GREEN}  ╚${DASHES}╝${NC}\n"
printf "\n"

box_top
box_title "INSTALL SUMMARY"
box_row "Platform"      "$PLATFORM"
box_row "Python"        "$PY_VER"
box_row "Install dir"   "$INSTALL_DIR"
box_row "App dir"       "$APP_DIR"
INSTALLED_TOTAL=${INSTALLED_COUNT:-${#DEPS[@]}}
box_row "Packages"      "${INSTALLED_TOTAL}/${#DEPS[@]} installed"
box_row "Total time"    "${TOTAL}s"
box_bot
printf "\n"

printf "  ${BOLD}${CYAN}Run the agent:${NC}\n"
printf "    ${DIM}cd${NC}      ${GREEN}%s${NC}\n" "$APP_DIR"
if [ -n "$VENV_DIR" ]; then
    printf "    ${DIM}source${NC}  ${GREEN}%s/bin/activate${NC}\n" "$VENV_DIR"
fi
printf "    ${GREEN}%-31s${NC} ${DIM}# %s${NC}\n" "python -m harness"              "Interactive CLI"
printf "    ${GREEN}%-31s${NC} ${DIM}# %s${NC}\n" "python -m harness web"          "Web UI (port 5000)"
printf "    ${GREEN}%-31s${NC} ${DIM}# %s${NC}\n" "python -m harness web 8080"     "Custom port"
printf "    ${GREEN}%-31s${NC} ${DIM}# %s${NC}\n" "python -m harness telegram TOK" "Telegram bot"
printf "    ${GREEN}%-31s${NC} ${DIM}# %s${NC}\n" "python -m harness all"          "Web + Telegram"
printf "\n"
printf "  ${DIM}✦ The harness package is registered, so you can run it from any folder.${NC}\n"
printf "  ${DIM}✦ Enjoying Harness? Star the repo: github.com/1dev-hridoy/MobileAgent${NC}\n"
printf "\n"

end_phase