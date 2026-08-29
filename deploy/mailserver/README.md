# SmartSportz mail server

Self-hosted `docker-mailserver` providing `info@smartsportz.in`, with
`mail.smartsportz.in` as the mail host.

Deployed to `/opt/mailserver`, deliberately **separate** from the application
stack. `scripts/deploy.sh` only manages the root `docker-compose.yml`, so it
will never restart, recreate, or prune anything here.

## Status of the prerequisites

| Requirement | State |
|---|---|
| Outbound port 25 | **OPEN** — verified against Gmail's MX |
| IP on a blocklist | Clean — not listed on Spamhaus ZEN or Barracuda |
| Reverse DNS (PTR) | **MISSING** — must be set by the hosting provider |
| `mail.smartsportz.in` A record | Not yet created |
| SPF / DKIM | Not yet published |
| DMARC | `p=reject` with nothing to pass it — rejects all your mail today |

## Order of operations

1. **Ask your host to set the PTR record** for this server's IP to
   `mail.smartsportz.in`. Gmail and Outlook reject mail from IPs without
   reverse DNS, and this is the one item you cannot do yourself.

2. **Add the A record at GoDaddy** — `A  mail  <server IP>`. Needed before
   certbot can issue a certificate for the mail hostname.

3. **Run the setup:**
   ```bash
   cd /opt/smartdeploy/app/deploy/mailserver
   ./setup.sh
   ```
   It runs preflight checks, installs to `/opt/mailserver`, obtains the TLS
   certificate, installs a renewal hook, starts the container, creates the
   mailbox (prompting for a password), generates the DKIM key, and prints the
   DNS records you still need.

4. **Add the remaining DNS records** it prints — MX, SPF, DKIM, and the DMARC
   change. Reprint them any time with `./setup.sh dns`.

5. **Verify before trusting it.** Send to a Gmail address and check
   *Show original*: SPF, DKIM and DMARC must all say `PASS`. Only then set
   `_dmarc` back to `p=reject`.

## Pointing the app at it

In `/opt/smartdeploy/.env`:

```
EMAIL_PROVIDER=smtp
SMTP_HOST=mail.smartsportz.in
SMTP_PORT=587
SMTP_USERNAME=info@smartsportz.in
SMTP_PASSWORD=<the mailbox password from step 3>
SMTP_USE_SSL=false
SMTP_USE_TLS=true
SMTP_SENDER_EMAIL=info@smartsportz.in
SMTP_SENDER_NAME=Smart Sportz
```

Port 587 with `USE_SSL=false` / `USE_TLS=true` selects the STARTTLS path in
`backend/app/services/notifications.py`. Then recreate the backend:

```bash
cd /opt/smartdeploy/app
docker compose -p smartsportz -f docker-compose.yml \
  --env-file /opt/smartdeploy/.env up -d --no-build
```

## Operating it

```bash
cd /opt/mailserver
docker compose logs -f mailserver          # tail logs
docker compose ps                          # status
docker exec -ti mailserver setup email list
docker exec -ti mailserver setup email add someone@smartsportz.in
docker exec -ti mailserver setup email update info@smartsportz.in   # change password
```

Mail data lives in `/opt/mailserver/data/`. **Back it up** — it is not in git
and not covered by the application's image backups.

## Ongoing responsibilities

Running your own mail server is not fire-and-forget:

- Watch for blocklist listings (mxtoolbox.com/blacklists) — one compromised
  account or a misconfiguration can get the IP listed, and delisting is slow.
- Keep the image updated; it is an internet-exposed SMTP/IMAP service.
- Monitor `/opt/mailserver/data/mail-logs/` for auth-failure floods. fail2ban
  is enabled, but check it is actually banning.
- The TLS certificate auto-renews via certbot; the deploy hook restarts the
  container so it picks up the new cert. Verify this works at the first
  renewal, roughly 60 days in.
- Reputation on a fresh IP starts neutral. Volume ramps matter — a sudden
  burst of mail from a new IP looks exactly like spam.
