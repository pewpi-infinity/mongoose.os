#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LOGDIR="infinity_storage/logs"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/push.log"

log() {
  echo "[$TS] $1" | tee -a "$LOGFILE"
}

log "∞ Infinity Git Push (Adaptive Mode)"

# -----------------------------
# Detect sparse-checkout
# -----------------------------
SPARSE=false
if git config --get core.sparseCheckout >/dev/null 2>&1; then
  if [ "$(git config --get core.sparseCheckout)" = "true" ]; then
    SPARSE=true
    log "Sparse-checkout detected"
  fi
fi

# -----------------------------
# Pre-push sanity checks
# -----------------------------
log "Running pre-push sanity checks"

# 1) Cart factory mismatch
if grep -R "cart027_robotics_factory" -n . --exclude-dir=.git >/dev/null 2>&1; then
  if [ ! -f cart027_robotics_factory.py ]; then
    log "ERROR: cart027_robotics_factory referenced but missing"
    exit 1
  fi
fi

# 2) Broken cart numbering (holes)
MISSING=$(ls cart[0-9][0-9][0-9]_*.py 2>/dev/null \
  | sed -E 's/cart([0-9]{3})_.*/\1/' \
  | sort -n \
  | awk 'NR>1 && $1!=prev+1 {print prev+1} {prev=$1}')

if [ -n "$MISSING" ]; then
  log "WARNING: Cart number gaps detected: $MISSING"
fi

# -----------------------------
# Git status
# -----------------------------
log "Git status BEFORE add:"
git status --short | tee -a "$LOGFILE"

# -----------------------------
# Stage files safely
# -----------------------------
log "Staging files"

if $SPARSE; then
  log "Using sparse-aware staging"
  git add --sparse .
else
  git add .
fi

# -----------------------------
# Abort if nothing staged
# -----------------------------
if git diff --cached --quiet; then
  log "Nothing to commit — aborting push"
  exit 0
fi

# -----------------------------
# Commit
# -----------------------------
MSG="∞ Auto-push $(date -u +'%Y-%m-%d %H:%M UTC')"
git commit -m "$MSG" | tee -a "$LOGFILE"

# -----------------------------
# Push
# -----------------------------
log "Pushing to origin"
git push | tee -a "$LOGFILE"

# -----------------------------
# Finalize
# -----------------------------
date -u > "$LOGDIR/last_push.time"
log "Push complete"

