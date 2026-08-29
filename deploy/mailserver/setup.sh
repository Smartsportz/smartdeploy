#!/bin/bash

set -Eeuo pipefail

# ============================================================
# SmartSportz mail server - install / bootstrap
#
#   ./setup.sh                 preflight, install, start, create mailbox
#   ./setup.sh --skip-checks   run anyway if a preflight check fails
#   ./setup.sh dns             just reprint the DNS records to add
#
# Deploys docker-mailserver at /opt/mailserver, kept entirely separate from
# the application stack so scripts/deploy.sh never touches it.
# ============================================================

DOMAIN="smartsportz.in"
MAIL_HOST="mail.$DOMAIN"
MAILBOX="info@$DOMAIN"

INSTALL_DIR="/opt/mailserver"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SKIP_CHECKS=0

if [ -t 1 ]; then
    GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
else
    GREEN=''; YELLOW=''; RED=''; BLUE=''; NC=''
fi

success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1" >&2; }

mail_compose() { docker compose -f "$INSTALL_DIR/compose.yaml" "$@"; }

# ============================================================
# DNS RECORD REPORT
# ============================================================

print_dns_records() {
    local ip dkim_file
    ip=$(curl -fsS --max-time 10 https://api.ipify.org 2>/dev/null || echo "<this server public IP>")
    dkim_file="$INSTALL_DIR/data/config/opendkim/keys/$DOMAIN/mail.txt"

    cat <<REPORT

============================================================
  DNS RECORDS TO ADD AT GODADDY
============================================================

Type   Name              Value
----   ----              -----
A      mail              $ip
MX     @                 $MAIL_HOST          (priority 10)
TXT    @                 v=spf1 mx ~all
TXT    _dmarc            v=DMARC1; p=none; rua=mailto:$MAILBOX;

REPORT

    if [ -f "$dkim_file" ]; then
        echo "TXT    mail._domainkey   (the quoted value below, joined into one line)"
        echo ""
        cat "$dkim_file"
    else
        echo "TXT    mail._domainkey   run './setup.sh' first to generate the DKIM key"
    fi

    cat <<'REPORT'

------------------------------------------------------------
NOTES

* Only ONE SPF record may exist on @. If you add another sender
  later (Brevo, Zoho), merge it into the same record - a second
  v=spf1 record is a hard failure, not a merge.

* _dmarc currently says p=reject with no SPF and no DKIM, which
  rejects all your mail. Set it to p=none as shown, confirm a test
  message passes both checks, then move it back to p=reject.

* PTR (reverse DNS) cannot be set in GoDaddy. Ask your hosting
  provider to point this server's IP at mail.smartsportz.in.
  Without it Gmail and Outlook will refuse your mail.
============================================================
REPORT
}

if [ "${1:-}" = "dns" ]; then
    print_dns_records
    exit 0
fi

[ "${1:-}" = "--skip-checks" ] && SKIP_CHECKS=1

# ============================================================
# PREFLIGHT
# ============================================================

echo ""
echo "============================================================"
echo "        SMARTSPORTZ MAIL SERVER - SETUP"
echo "============================================================"
echo ""
echo "Hostname : $MAIL_HOST"
echo "Mailbox  : $MAILBOX"
echo "Install  : $INSTALL_DIR"
echo ""

[ "$(id -u)" -eq 0 ] || { error "Run as root."; exit 1; }

for cmd in docker dig curl openssl; do
    command -v "$cmd" >/dev/null 2>&1 || { error "$cmd is not installed."; exit 1; }
done
docker info >/dev/null 2>&1 || { error "Cannot talk to the Docker daemon."; exit 1; }

FAILED=0

# ---- 1. outbound :25 ----
# The single most important check. A mail server delivers by connecting out
# on port 25 to each recipient's MX. Most hosting providers block this, and
# no amount of configuration works around it.
info "Checking outbound port 25 (required to deliver mail)..."
OUT25=0
for mx in gmail-smtp-in.l.google.com alt1.gmail-smtp-in.l.google.com; do
    if timeout 10 bash -c "cat < /dev/null > /dev/tcp/$mx/25" 2>/dev/null; then
        OUT25=1
        break
    fi
done
if [ "$OUT25" -eq 1 ]; then
    success "Outbound port 25 is open."
else
    error "Outbound port 25 is BLOCKED by your host."
    error "This server cannot deliver mail to anyone. Ask your provider to"
    error "unblock it, or send through a relay (Brevo) instead."
    FAILED=1
fi

# ---- 2. reverse DNS ----
info "Checking reverse DNS..."
PUBLIC_IP=$(curl -fsS --max-time 10 https://api.ipify.org 2>/dev/null || true)
if [ -z "$PUBLIC_IP" ]; then
    warning "Could not determine the public IP - skipping the PTR check."
else
    PTR=$(dig +short -x "$PUBLIC_IP" 2>/dev/null | sed 's/\.$//')
    if [ -z "$PTR" ]; then
        error "$PUBLIC_IP has NO PTR record."
        error "Gmail, Outlook and Yahoo reject mail from IPs without reverse DNS."
        error "Ask your provider to set: $PUBLIC_IP -> $MAIL_HOST"
        FAILED=1
    elif [ "$PTR" != "$MAIL_HOST" ]; then
        warning "PTR is '$PTR', expected '$MAIL_HOST'. Deliverability will suffer."
    else
        success "PTR matches $MAIL_HOST."
    fi
fi

# ---- 3. the A record must exist before certbot can validate ----
info "Checking DNS for $MAIL_HOST..."
MAIL_A=$(dig +short A "$MAIL_HOST" | tail -1)
if [ -z "$MAIL_A" ]; then
    error "$MAIL_HOST has no A record. Add it at GoDaddy first:"
    error "  A    mail    ${PUBLIC_IP:-<this server IP>}"
    FAILED=1
elif [ -n "$PUBLIC_IP" ] && [ "$MAIL_A" != "$PUBLIC_IP" ]; then
    warning "$MAIL_HOST resolves to $MAIL_A but this server is $PUBLIC_IP."
else
    success "$MAIL_HOST resolves here."
fi

# ---- 4. ports free ----
info "Checking that the mail ports are free..."
for p in 25 587 465 993; do
    listeners=$(ss -ltn "( sport = :$p )" 2>/dev/null | tail -n +2)
    if [ -n "$listeners" ] && ! docker ps --format '{{.Names}}' | grep -qx mailserver; then
        error "Port $p is already in use by another process."
        FAILED=1
    fi
done
[ "$FAILED" -eq 0 ] && success "Mail ports are free."

if [ "$FAILED" -ne 0 ]; then
    echo ""
    if [ "$SKIP_CHECKS" -eq 1 ]; then
        warning "Preflight failed but --skip-checks was given. Continuing."
    else
        error "Preflight failed. Fix the above, or re-run with --skip-checks."
        exit 1
    fi
fi

# ============================================================
# INSTALL
# ============================================================

info "Installing to $INSTALL_DIR ..."
mkdir -p "$INSTALL_DIR"/data/{mail-data,mail-state,mail-logs,config}
install -m 644 "$SRC_DIR/compose.yaml"    "$INSTALL_DIR/compose.yaml"
install -m 600 "$SRC_DIR/mailserver.env"  "$INSTALL_DIR/mailserver.env"
success "Files installed."

# ---- TLS certificate ----
if [ ! -d "/etc/letsencrypt/live/$MAIL_HOST" ]; then
    info "Obtaining a TLS certificate for $MAIL_HOST ..."
    if command -v certbot >/dev/null 2>&1; then
        # --nginx keeps the existing site serving while validating.
        certbot certonly --nginx -d "$MAIL_HOST" --non-interactive --agree-tos \
            --email "$MAILBOX" || {
            error "certbot failed. The A record must resolve here and :80 must be reachable."
            exit 1
        }
        success "Certificate issued."
    else
        error "certbot is not installed: apt-get install -y certbot python3-certbot-nginx"
        exit 1
    fi
else
    success "Certificate for $MAIL_HOST already present."
fi

# ---- renewal hook ----
# SSL_TYPE=letsencrypt reads the cert at container start, so a renewed cert is
# not picked up until the container restarts.
HOOK=/etc/letsencrypt/renewal-hooks/deploy/restart-mailserver.sh
mkdir -p "$(dirname "$HOOK")"
cat > "$HOOK" <<HOOKEOF
#!/bin/bash
# Installed by SmartSportz mailserver setup.sh
if [ "\$RENEWED_LINEAGE" = "/etc/letsencrypt/live/$MAIL_HOST" ]; then
    docker compose -f $INSTALL_DIR/compose.yaml restart mailserver
fi
HOOKEOF
chmod +x "$HOOK"
success "Certificate renewal hook installed."

# ---- firewall ----
if command -v ufw >/dev/null 2>&1 && ufw status 2>/dev/null | grep -q "Status: active"; then
    info "Opening mail ports in ufw..."
    for p in 25 587 465 993; do ufw allow "$p"/tcp >/dev/null; done
    success "ufw rules added."
fi

# ============================================================
# START
# ============================================================

info "Starting the mail server..."
mail_compose up -d

info "Waiting for it to become healthy (up to 3 minutes)..."
deadline=$((SECONDS + 180))
while :; do
    state=$(docker inspect --format '{{.State.Health.Status}}' mailserver 2>/dev/null || echo starting)
    [ "$state" = "healthy" ] && { success "Mail server is healthy."; break; }
    if [ "$SECONDS" -ge "$deadline" ]; then
        error "Timed out. Logs:"
        mail_compose logs --tail=50
        exit 1
    fi
    sleep 5
done

# ============================================================
# MAILBOX + DKIM
# ============================================================

if docker exec mailserver setup email list 2>/dev/null | grep -q "$MAILBOX"; then
    success "$MAILBOX already exists."
else
    echo ""
    info "Creating $MAILBOX - you will be prompted for its password."
    docker exec -ti mailserver setup email add "$MAILBOX"
    success "Mailbox created."
fi

if [ ! -f "$INSTALL_DIR/data/config/opendkim/keys/$DOMAIN/mail.txt" ]; then
    info "Generating the DKIM key..."
    # The flag form is used by docker-mailserver v13+; older tags take it
    # positionally. Try both so this works across image versions.
    docker exec mailserver setup config dkim --domain "$DOMAIN" \
        || docker exec mailserver setup config dkim domain "$DOMAIN" \
        || { error "DKIM generation failed. Run 'docker exec -ti mailserver setup config dkim help'"; exit 1; }
    mail_compose restart mailserver
    success "DKIM key generated."
else
    success "DKIM key already present."
fi

print_dns_records

echo ""
success "Setup complete."
echo ""
echo "Add the DNS records above at GoDaddy, wait for propagation, then verify:"
echo "  dig +short MX $DOMAIN"
echo "  dig +short TXT mail._domainkey.$DOMAIN"
echo ""
echo "Send a test message to a Gmail address and check its headers show"
echo "SPF=pass, DKIM=pass and DMARC=pass before switching _dmarc to p=reject."
echo ""
echo "Reprint the DNS records any time with:  $0 dns"
echo ""
