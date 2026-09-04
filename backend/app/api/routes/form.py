from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.api.deps import require_roles
from app.core.responses import ok
from app.db.database import form_execute, form_row, form_rows, rows
from app.schemas import FormRegistrationRequest, FormRegistrationStatusUpdate
from app.services.audit import log

# Serves the standalone form at https://form.smartsportz.in. The POST is
# public; everything else needs a management/super_admin token.
router = APIRouter(prefix="/form", tags=["form"])

# Per-IP submission ceiling, checked against the table itself so it survives a
# backend restart. The nginx limit_req in form/nginx.conf is the first gate;
# this is the one that still applies if that proxy is ever bypassed.
MAX_SUBMISSIONS_PER_IP_PER_DAY = 20


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:60]
    return (request.client.host if request.client else "")[:60]


def _is_unique_violation(exc: Exception) -> bool:
    if isinstance(exc, sqlite3.IntegrityError):
        return "UNIQUE" in str(exc).upper()
    # psycopg raises UniqueViolation; matching by name avoids importing it,
    # since psycopg is not installed in SQLite-only deployments.
    return type(exc).__name__ == "UniqueViolation"


@router.get("/options")
def form_options():
    """Sport list for the form's dropdown. Public, same source as the site."""
    sports = rows(
        "SELECT slug, name FROM sports WHERE COALESCE(published, 1) = 1 ORDER BY sort_order, name"
    )
    return ok({
        "sports": sports,
        "ageGroups": ["Under 12", "Under 14", "Under 16", "Under 19", "Open", "Veterans"],
    })


@router.post("/register")
def submit_form_registration(payload: FormRegistrationRequest, request: Request):
    if payload.website:
        # Honeypot tripped. Answer as if it worked so the bot does not retry.
        return ok({"id": None}, "Registration received")

    ip_address = _client_ip(request)
    if ip_address:
        since = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        recent = form_row(
            "SELECT COUNT(*) AS total FROM form_registrations WHERE ip_address = ? AND created_at >= ?",
            (ip_address, since),
        )
        if recent and int(recent["total"] or 0) >= MAX_SUBMISSIONS_PER_IP_PER_DAY:
            raise HTTPException(status_code=429, detail="Too many submissions from this network today.")

    registration_id = f"frm_{uuid4().hex[:12]}"
    try:
        form_execute(
            """INSERT INTO form_registrations(
                 id, full_name, email, phone, city, sport, team_name, age_group,
                 notes, status, source, ip_address, user_agent, created_at
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                registration_id,
                payload.full_name,
                str(payload.email).strip().lower(),
                payload.phone,
                payload.city,
                payload.sport,
                payload.team_name,
                payload.age_group,
                payload.notes,
                "new",
                "form_subdomain",
                ip_address,
                request.headers.get("user-agent", "")[:400],
                datetime.now(timezone.utc).isoformat(),
            ),
        )
    except Exception as exc:
        if _is_unique_violation(exc):
            raise HTTPException(
                status_code=409,
                detail="This email is already registered for that sport.",
            ) from exc
        raise

    log("public", "form_registration_created", "form_registration", registration_id, payload.email)
    return ok({"id": registration_id}, "Registration received")


@router.get("/registrations")
def list_form_registrations(
    status: str | None = Query(default=None, pattern="^(new|contacted|approved|rejected)$"),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    _: dict = Depends(require_roles("super_admin", "management")),
):
    where = "WHERE status = ?" if status else ""
    params: tuple = (status, limit, offset) if status else (limit, offset)
    records = form_rows(
        f"""SELECT id, full_name, email, phone, city, sport, team_name, age_group,
                   notes, status, source, reviewed_by, reviewed_at, created_at
            FROM form_registrations {where}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?""",
        params,
    )
    total = form_row(
        f"SELECT COUNT(*) AS total FROM form_registrations {where}",
        (status,) if status else (),
    )
    return ok({
        "registrations": records,
        "total": int((total or {}).get("total") or 0),
        "limit": limit,
        "offset": offset,
    })


@router.patch("/registrations/{registration_id}")
def update_form_registration_status(
    registration_id: str,
    payload: FormRegistrationStatusUpdate,
    user: dict = Depends(require_roles("super_admin", "management")),
):
    existing = form_row("SELECT id FROM form_registrations WHERE id = ?", (registration_id,))
    if not existing:
        raise HTTPException(status_code=404, detail="Registration not found")
    form_execute(
        "UPDATE form_registrations SET status = ?, reviewed_by = ?, reviewed_at = ? WHERE id = ?",
        (payload.status, user["email"], datetime.now(timezone.utc).isoformat(), registration_id),
    )
    log(user["email"], "form_registration_updated", "form_registration", registration_id, payload.status)
    return ok(form_row("SELECT * FROM form_registrations WHERE id = ?", (registration_id,)), "Status updated")
