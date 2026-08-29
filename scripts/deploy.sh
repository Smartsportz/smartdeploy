#!/bin/bash

set -Eeuo pipefail

# ============================================================
# SmartSportz - Docker Compose Deployment Script
#
#   ./deploy.sh              deploy the current origin/main
#   ./deploy.sh rollback     restore the most recent image backup
#   ./deploy.sh status       show container status
#   ./deploy.sh logs [svc]   tail logs
#
# Layout on the server:
#   /opt/smartdeploy/.env       secrets  (outside the clone on purpose)
#   /opt/smartdeploy/app/       git clone
#   /opt/smartdeploy/images/    image backups, newest 5 kept
#   /opt/smartdeploy/logs/      one log per run
# ============================================================

# -----------------------------
# CONFIGURATION
# -----------------------------

APP_NAME="smartdeploy"

REPO_URL="https://github.com/Smartsportz/smartdeploy.git"
BRANCH="main"

BASE_DIR="/opt/smartdeploy"
APP_DIR="$BASE_DIR/app"
IMAGE_DIR="$BASE_DIR/images"
LOG_DIR="$BASE_DIR/logs"

ENV_FILE="$BASE_DIR/.env"
COMPOSE_FILE="$APP_DIR/docker-compose.yml"

# Fixed project name. Without -p, compose derives the project from the
# directory name ("app"), which would change every built image tag and make
# the backups from a differently-named checkout unrestorable.
PROJECT="smartsportz"

# Keep latest 5 deployment image backups
KEEP_IMAGES=5

# Free space required in $IMAGE_DIR before an image backup is attempted.
MIN_FREE_MB=8192

# How long to wait for every container to become healthy.
HEALTH_TIMEOUT=240

# Roll back automatically when the health gate fails.
ROLLBACK_ON_FAILURE="${ROLLBACK_ON_FAILURE:-true}"

# -----------------------------
# COLORS
# -----------------------------

if [ -t 1 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    GREEN='' ; YELLOW='' ; RED='' ; BLUE='' ; NC=''
fi

# -----------------------------
# LOGGING
# -----------------------------

success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1" >&2; }

TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Create the log directory BEFORE redirecting output, and report the failure
# on the real stderr - a permissions problem here is exactly the case you
# most want to see, and it cannot be written to a log that cannot be created.
if ! mkdir -p "$BASE_DIR" "$IMAGE_DIR" "$LOG_DIR" 2>/dev/null; then
    error "Cannot create $BASE_DIR. Run as root, or chown it to $(id -un)."
    exit 1
fi

LOG_FILE="$LOG_DIR/deploy-$TIMESTAMP.log"
exec > >(tee -a "$LOG_FILE") 2>&1

# ============================================================
# COMPOSE WRAPPER
# ============================================================

# --env-file feeds ${VAR} interpolation in docker-compose.yml (the published
# ports); the env_file: key inside the compose file is what puts the secrets
# into the containers. Both point at the same file.
compose() {
    docker compose \
        -p "$PROJECT" \
        -f "$COMPOSE_FILE" \
        --env-file "$ENV_FILE" \
        "$@"
}

# ============================================================
# ERROR HANDLER
# ============================================================

deployment_failed() {
    local exit_code=$?

    # Stop the trap from re-entering while we gather diagnostics.
    trap - ERR

    error "Deployment failed (exit $exit_code)."

    if [ -f "$COMPOSE_FILE" ] && [ -f "$ENV_FILE" ]; then
        echo ""
        echo "Container status:"
        compose ps -a || true

        echo ""
        echo "Recent logs:"
        compose logs --tail=100 || true
    fi

    echo ""
    error "Full log: $LOG_FILE"
    exit 1
}

trap deployment_failed ERR

# ============================================================
# HELPERS
# ============================================================

# `docker compose ps --format json` emits NDJSON on some versions and a single
# JSON array on others. Normalise to one object per line either way.
compose_ps_json() {
    compose ps -a --format json 2>/dev/null \
        | jq -c 'if type == "array" then .[] else . end'
}

port_owner() {
    # Prints something if the TCP port is already bound on the host.
    ss -ltn "( sport = :$1 )" 2>/dev/null | tail -n +2 | grep -q . && echo busy || true
}

free_mb() {
    df -Pm "$1" | awk 'NR==2 {print $4}'
}

# ============================================================
# ROLLBACK
# ============================================================

latest_backup() {
    find "$IMAGE_DIR" -maxdepth 1 -type f -name "${APP_NAME}-*.tar.gz" \
        -printf '%T@ %p\n' 2>/dev/null \
        | sort -nr | head -1 | cut -d' ' -f2-
}

do_rollback() {
    local archive
    archive=$(latest_backup)

    if [ -z "$archive" ]; then
        error "No image backup found in $IMAGE_DIR - cannot roll back."
        return 1
    fi

    warning "Rolling back to $archive"

    # The archive holds the images under the same tags the build overwrites
    # (smartsportz-backend, smartsportz-frontend, ...), so loading it puts the
    # previous build back behind those tags.
    gunzip -c "$archive" | docker load

    # --no-build is essential: rebuilding would immediately undo the load.
    compose up -d --no-build --remove-orphans

    if [ -f "${archive%.tar.gz}.meta" ]; then
        echo ""
        info "Rolled back to:"
        cat "${archive%.tar.gz}.meta"
    fi

    success "Rollback complete."
}

# ============================================================
# HEALTH GATE
# ============================================================

wait_for_healthy() {
    local deadline=$(( SECONDS + HEALTH_TIMEOUT ))
    local pending failed report

    info "Waiting up to ${HEALTH_TIMEOUT}s for containers to become healthy..."

    while :; do
        report=$(compose_ps_json)

        # No containers at all means `up` produced nothing - never report that
        # as success just because there is nothing in the failed list.
        if [ -z "$report" ]; then
            if [ "$SECONDS" -ge "$deadline" ]; then
                error "No containers are running for project $PROJECT."
                return 1
            fi
            sleep 5
            continue
        fi

        # A container that exited non-zero is a hard failure - no point waiting.
        # backend-init is a one-shot that always exits 0, so the exit CODE is
        # what matters here, not the "exited" state. Checking State alone would
        # flag every successful deploy as broken.
        failed=$(echo "$report" | jq -r '
            select((.State == "exited"  and (.ExitCode // 0) != 0)
                or (.State == "dead")
                or (.Health == "unhealthy"))
            | "\(.Service) (state=\(.State) exit=\(.ExitCode // 0) health=\(.Health // "none"))"')

        if [ -n "$failed" ]; then
            error "Containers failed:"
            echo "$failed" | sed 's/^/  - /'
            return 1
        fi

        # Still settling: starting healthchecks, restarting, or not up yet.
        pending=$(echo "$report" | jq -r '
            select(.Health == "starting"
                or .State == "restarting"
                or .State == "created"
                or (.State == "running" and .Health == "unhealthy"))
            | .Service')

        if [ -z "$pending" ]; then
            success "All containers are healthy."
            return 0
        fi

        if [ "$SECONDS" -ge "$deadline" ]; then
            error "Timed out waiting for: $(echo "$pending" | paste -sd', ')"
            return 1
        fi

        sleep 5
    done
}

# ============================================================
# SUBCOMMANDS
# ============================================================

case "${1:-deploy}" in
    rollback)
        do_rollback
        exit 0
        ;;
    status)
        compose ps -a
        exit 0
        ;;
    logs)
        shift || true
        compose logs --tail=200 -f "$@"
        exit 0
        ;;
    deploy)
        ;;
    *)
        error "Unknown command: $1 (expected: deploy | rollback | status | logs)"
        exit 1
        ;;
esac

# ============================================================
# START
# ============================================================

echo ""
echo "============================================================"
echo "              SMARTSPORTZ DEPLOYMENT"
echo "============================================================"
echo ""
echo "Application : $APP_NAME"
echo "Project     : $PROJECT"
echo "Repository  : $REPO_URL"
echo "Branch      : $BRANCH"
echo "Time        : $TIMESTAMP"
echo "Log         : $LOG_FILE"
echo ""

# ============================================================
# 1. PREFLIGHT
# ============================================================

info "Checking required commands..."

for cmd in git docker jq ss; do
    command -v "$cmd" >/dev/null 2>&1 || {
        error "$cmd is not installed."
        exit 1
    }
done

docker compose version >/dev/null 2>&1 || {
    error "The docker compose plugin is not installed."
    exit 1
}

# `docker --version` works without the daemon; this actually talks to it and
# so also catches "user is not in the docker group".
docker info >/dev/null 2>&1 || {
    error "Cannot talk to the Docker daemon."
    error "Start it, or add $(id -un) to the docker group (note: that is"
    error "equivalent to granting root on this host)."
    exit 1
}

success "git, docker, docker compose, jq and ss are available."

# ---- secrets file ----

info "Checking secrets file..."

if [ ! -f "$ENV_FILE" ]; then
    error "Missing $ENV_FILE"
    error "Copy .env.example there and fill it in:"
    error "  sudo install -m 600 /dev/null $ENV_FILE"
    error "  sudo nano $ENV_FILE"
    exit 1
fi

perms=$(stat -c '%a' "$ENV_FILE")
if [ "$perms" != "600" ] && [ "$perms" != "400" ]; then
    warning "$ENV_FILE is mode $perms - tightening to 600."
    chmod 600 "$ENV_FILE"
fi

success "Secrets file present."

# ============================================================
# 2. CLONE / UPDATE REPOSITORY
# ============================================================

info "Checking Git repository..."

if [ ! -d "$APP_DIR/.git" ]; then

    if [ -d "$APP_DIR" ] && [ -n "$(ls -A "$APP_DIR" 2>/dev/null)" ]; then
        error "$APP_DIR exists, is not empty, and is not a git clone."
        error "Move it aside before deploying."
        exit 1
    fi

    rm -rf "$APP_DIR"

    info "Cloning repository..."
    git clone --branch "$BRANCH" --single-branch "$REPO_URL" "$APP_DIR"
    success "Repository cloned."

else

    info "Fetching latest code..."
    cd "$APP_DIR"

    git fetch origin "$BRANCH"
    git checkout "$BRANCH"
    git reset --hard "origin/$BRANCH"

    # Removes untracked build leftovers. The secrets file is safe because it
    # lives in $BASE_DIR, not in the clone - keep it that way.
    git clean -fd

    success "Repository updated."
fi

cd "$APP_DIR"

COMMIT_ID=$(git rev-parse --short HEAD)
COMMIT_MESSAGE=$(git log -1 --pretty=format:"%s")

echo ""
echo "------------------------------------------------------------"
echo "Commit  : $COMMIT_ID"
echo "Message : $COMMIT_MESSAGE"
echo "------------------------------------------------------------"
echo ""

# ============================================================
# 3. VALIDATE COMPOSE CONFIGURATION
# ============================================================

info "Validating Docker Compose configuration..."

[ -f "$COMPOSE_FILE" ] || {
    error "docker-compose.yml not found at $COMPOSE_FILE"
    exit 1
}

# Also proves every required variable in $ENV_FILE is set - the ${VAR:?...}
# guards in the compose file fail here rather than halfway through a deploy.
compose config >/dev/null

success "Compose configuration is valid."

# ---- host port availability ----

info "Checking host ports..."

conflict=0
while read -r host_port; do
    [ -n "$host_port" ] || continue
    if [ -n "$(port_owner "$host_port")" ]; then
        # Already bound by our own project? Then it is just the running
        # version of this stack and `up` will hand the port over.
        if compose ps -q 2>/dev/null | grep -q .; then
            info "Port $host_port is held by the current deployment."
        else
            error "Port $host_port is already in use by another process."
            conflict=1
        fi
    fi
done < <(compose config --format json | jq -r '.services[].ports[]?.published // empty' | sort -u)

if [ "$conflict" -ne 0 ]; then
    error "Free the ports above, or change them in $ENV_FILE."
    exit 1
fi

success "Host ports are available."

# ============================================================
# 4. PULL BASE IMAGES
# ============================================================

# `build` only touches services that have a build: section. redis, prometheus
# and grafana are pull-only, so without this they may not exist locally and
# the docker save in the next step fails with "No such image".
info "Pulling pull-only base images..."

compose pull --ignore-buildable

success "Base images present."

# ============================================================
# 5. BACK UP THE CURRENTLY DEPLOYED IMAGES
# ============================================================

# This runs BEFORE the build, on purpose. Saving after the build would archive
# the new images - if the new build is broken, the archive is broken too and
# there is nothing to roll back to.

info "Backing up the currently deployed images..."

mapfile -t ALL_IMAGES < <(compose config --images)

if [ "${#ALL_IMAGES[@]}" -eq 0 ]; then
    error "Compose reported no images."
    exit 1
fi

# Only images that actually exist right now - on a first deploy the built
# tags do not exist yet, and that is not an error.
PRESENT_IMAGES=()
for image in "${ALL_IMAGES[@]}"; do
    if docker image inspect "$image" >/dev/null 2>&1; then
        PRESENT_IMAGES+=("$image")
    fi
done

BACKUP_FILE=""
BACKUP_SIZE="n/a"

if [ "${#PRESENT_IMAGES[@]}" -eq 0 ]; then
    warning "No existing images found - first deploy, nothing to back up."
else
    available=$(free_mb "$IMAGE_DIR")
    if [ "$available" -lt "$MIN_FREE_MB" ]; then
        error "Only ${available}MB free in $IMAGE_DIR, need ${MIN_FREE_MB}MB."
        error "Delete old backups or lower KEEP_IMAGES."
        exit 1
    fi

    BACKUP_FILE="$IMAGE_DIR/${APP_NAME}-${TIMESTAMP}-${COMMIT_ID}.tar.gz"

    echo ""
    echo "Images being archived:"
    printf '  %s\n' "${PRESENT_IMAGES[@]}"
    echo ""

    docker save "${PRESENT_IMAGES[@]}" | gzip > "$BACKUP_FILE"

    if [ ! -s "$BACKUP_FILE" ]; then
        error "Image backup is empty."
        rm -f "$BACKUP_FILE"
        exit 1
    fi

    # Record what this archive restores you TO, so a rollback is not a guess.
    {
        echo "archived_at : $TIMESTAMP"
        echo "rolls_back_to_commit: $(git rev-parse --short HEAD@{1} 2>/dev/null || echo "$COMMIT_ID")"
        echo "deploying_commit: $COMMIT_ID"
        echo "images:"
        printf '  %s\n' "${PRESENT_IMAGES[@]}"
    } > "${BACKUP_FILE%.tar.gz}.meta"

    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | awk '{print $1}')
    success "Backup created: $BACKUP_FILE ($BACKUP_SIZE)"
fi

# ---- keep only the newest $KEEP_IMAGES ----

info "Pruning old image backups (keeping $KEEP_IMAGES)..."

find "$IMAGE_DIR" -maxdepth 1 -type f -name "${APP_NAME}-*.tar.gz" \
    -printf '%T@ %p\n' \
    | sort -nr \
    | tail -n +"$((KEEP_IMAGES + 1))" \
    | cut -d' ' -f2- \
    | while read -r old; do
        rm -f "$old" "${old%.tar.gz}.meta"
        info "Removed $(basename "$old")"
    done

echo ""
echo "Current backups in $IMAGE_DIR:"
ls -lh "$IMAGE_DIR"/*.tar.gz 2>/dev/null || echo "  (none)"
echo ""

# ============================================================
# 6. BUILD
# ============================================================

info "Building application images..."

compose build --pull

success "Images built."

# ============================================================
# 7. DEPLOY
# ============================================================

info "Starting containers..."

compose up -d --remove-orphans

success "Containers started."

# ============================================================
# 8. HEALTH GATE
# ============================================================

if ! wait_for_healthy; then
    echo ""
    echo "Container status:"
    compose ps -a || true
    echo ""
    echo "Recent logs:"
    compose logs --tail=100 || true

    if [ "$ROLLBACK_ON_FAILURE" = "true" ] && [ -n "$(latest_backup)" ]; then
        echo ""
        warning "Health gate failed - rolling back."
        trap - ERR
        do_rollback || error "Rollback also failed. Manual intervention needed."
        error "Deployment rolled back. Log: $LOG_FILE"
        exit 1
    fi

    exit 1
fi

# ---- end-to-end check through the published port ----

FRONTEND_PORT_ACTUAL=$(compose config --format json \
    | jq -r '.services.frontend.ports[0].published // "8081"')

info "Probing the frontend on 127.0.0.1:$FRONTEND_PORT_ACTUAL ..."

if curl -fsS -o /dev/null --max-time 10 "http://127.0.0.1:${FRONTEND_PORT_ACTUAL}/"; then
    success "Frontend responded."
else
    warning "Frontend did not respond on the published port."
    warning "Containers are healthy, so check the port binding and host nginx."
fi

# ============================================================
# 9. CLEAN UP
# ============================================================

# Scoped to this project's dangling images. A bare `docker image prune -f`
# would also delete unrelated dangling images belonging to other stacks (and,
# on this host, anything Jenkins has built).
info "Removing dangling images from this project..."

docker image prune -f --filter "label=com.docker.compose.project=$PROJECT" || true

success "Cleanup done."

# ============================================================
# 10. RESULT
# ============================================================

echo ""
echo "============================================================"
echo -e "${GREEN}           DEPLOYMENT SUCCESSFUL${NC}"
echo "============================================================"
echo ""
echo "Application : $APP_NAME"
echo "Commit      : $COMMIT_ID"
echo "Backup      : ${BACKUP_FILE:-none (first deploy)}"
echo "Backup Size : $BACKUP_SIZE"
echo "Log         : $LOG_FILE"
echo ""
echo "Roll back with: $0 rollback"
echo ""

compose ps

echo ""
