from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from app.core.security import hash_password
from app.db.database import audit_execute, execute, execute_many, row


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def prize_rows(tournament_slug: str, total_amount: int) -> list[tuple[str, tuple]]:
    prizes = [
        (1, "1st Prize", int(total_amount * 0.60), 1),
        (2, "2nd Prize", int(total_amount * 0.30), 2),
        (3, "3rd Prize", total_amount - int(total_amount * 0.60) - int(total_amount * 0.30), 3),
    ]
    return [
        (
            "INSERT OR IGNORE INTO tournament_prizes(id, tournament_slug, position, label, amount, sort_order) VALUES (?, ?, ?, ?, ?, ?)",
            (f"prize_{tournament_slug}_{position}", tournament_slug, position, label, amount, sort_order),
        )
        for position, label, amount, sort_order in prizes
    ]


def seed_gallery_album_metadata() -> None:
    statements = []
    execute_many(statements)


def live_detail_update_rows() -> list[tuple[str, tuple]]:
    return []


def seed_live_match_details() -> None:
    if row("SELECT id FROM live_matches LIMIT 1"):
        execute_many(live_detail_update_rows())


def seed_public_page_base_data() -> None:
    statements: list[tuple[str, tuple]] = []
    tournaments = []
    statements += [
        (
            """
            INSERT OR IGNORE INTO tournaments (
              slug, name, sport, status, location, date, registration_start, registration_end,
              teams, capacity, team_size, min_age, max_age, prize, image, poster, accent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            item,
        )
        for item in tournaments
    ]
    teams = []
    statements += [("INSERT OR IGNORE INTO teams(slug, name, rank, sport, players, wins, rating, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", item) for item in teams]
    matches = []
    statements += [
        (
            """
            INSERT OR IGNORE INTO live_matches (
              id, tournament, sport, home, away, score, away_score, stage, status, image
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            item,
        )
        for item in matches
    ]
    if statements:
        execute_many(statements)


def seed_data() -> None:
    if row("SELECT id FROM users LIMIT 1"):
        return

    users = [
        (str(uuid4()), "prathap455169111@gmail.com", "Smart Sportz Admin", "super_admin", hash_password("admin123"), "", 1, 1, now()), #mathanatmachinelearning@gmail.com
        (str(uuid4()), "manager@smartsportz.in", "Tournament Manager", "management", hash_password("manager123"), "", 1, 1, now()),
        (str(uuid4()), "user@smartsportz.in", "Aryan Player", "user", hash_password("user123"), "+916374409006", 1, 1, now()),
    ]
    sports = [
        ("cricket", "Cricket", 42, "emerald"),
        ("football", "Football", 36, "blue"),
        ("basketball", "Basketball", 18, "orange"),
        ("volleyball", "Volleyball", 16, "pink"),
        ("badminton", "Badminton", 22, "emerald"),
        ("table-tennis", "Table Tennis", 11, "blue"),
        ("e-sports", "E-Sports", 29, "orange"),
        ("athletics", "Athletics", 14, "emerald"),
    ]
    tournaments: list[tuple] = []
    teams: list[tuple] = []
    matches: list[tuple] = []
    timeline: list[tuple] = []
    cms = []

    statements: list[tuple[str, tuple]] = []
    statements += [(
        """
        INSERT INTO users (
          id, email, name, role, password_hash, phone, email_verified, phone_verified, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        item,
    ) for item in users]
    statements += [("INSERT INTO sports(slug, name, active, color) VALUES (?, ?, ?, ?)", item) for item in sports]
    statements += [(
        """
        INSERT INTO tournaments (
          slug, name, sport, status, location, date, registration_start, registration_end,
          teams, capacity, team_size, prize, image, accent
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        item,
    ) for item in tournaments]
    statements += [("INSERT INTO teams VALUES (?, ?, ?, ?, ?, ?, ?, ?)", item) for item in teams]
    statements += [(
        """
        INSERT INTO live_matches (
          id, tournament, sport, home, away, score, away_score, stage, status, image
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        item,
    ) for item in matches]
    statements += [("INSERT INTO timeline_events(match_id, time, type, text, score, created_at) VALUES (?, ?, ?, ?, ?, ?)", item) for item in timeline]
    statements += [("INSERT INTO cms_content VALUES (?, ?, ?, ?, ?, ?)", item) for item in cms]
    execute_many(statements)
    audit_execute(
        "INSERT INTO audit_logs(actor, action, entity, entity_id, message, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        ("system", "seed", "database", "local", "Initial local database seeded", now()),
    )


def seed_operational_data() -> None:
    seed_public_page_base_data()
    operational_ready = (
        row("SELECT slug FROM tournaments WHERE slug = ?", ("kerala-volleyball-classic",))
        and row("SELECT slug FROM news_posts LIMIT 1")
        and row("SELECT id FROM leaderboard_records LIMIT 1")
        and row("SELECT id FROM tournament_prizes LIMIT 1")
        and row("SELECT slug FROM home_discovery_cards LIMIT 1")
        and row("SELECT slug FROM home_discovery_cards WHERE image LIKE '/assets/generated/%' LIMIT 1")
        and row("SELECT id FROM live_highlights LIMIT 1")
        and row("SELECT slug FROM sponsor_logos WHERE slug = 'smartsportz' AND image = '/assets/logo.png'")
        and row("SELECT post_slug FROM news_blocks WHERE post_slug = 'mumbai-mavericks-lift-premier-bash' AND sort_order >= 5 LIMIT 1")
    )
    seed_live_match_details()
    seed_gallery_album_metadata()
    if operational_ready:
        return
    statements: list[tuple[str, tuple]] = []
    city_map = {}
    for tournament_slug, cities in city_map.items():
        existing = row("SELECT id FROM tournament_cities WHERE tournament_slug = ? LIMIT 1", (tournament_slug,))
        if not existing:
            for sort_order, city in enumerate(cities, start=1):
                statements.append((
                    "INSERT OR IGNORE INTO tournament_cities(id, tournament_slug, city, sort_order) VALUES (?, ?, ?, ?)",
                    (f"city_{uuid4().hex[:10]}", tournament_slug, city, sort_order),
                ))
    if not row("SELECT id FROM registrations WHERE id = ?", ("reg-101",)):
        registrations = []
        statements += [(
            """
            INSERT INTO registrations (
              id, tournament_slug, team_name, captain_name, email, phone, city,
              status, payment_status, amount, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            item,
        ) for item in registrations]
    if not row("SELECT id FROM bracket_nodes WHERE tournament_slug = ?", ("bangalore-corporate-t20",)):
        nodes = []
        connections = []
        statements += [("INSERT INTO bracket_nodes(id, tournament_slug, label, team, round, x, y, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", item) for item in nodes]
        statements += [("INSERT INTO bracket_connections VALUES (?, ?, ?, ?)", item) for item in connections]
    manager = row("SELECT id FROM users WHERE email = ?", ("manager@smartsportz.in",))
    if manager and not row("SELECT id FROM manager_city_assignments WHERE manager_user_id = ? LIMIT 1", (manager["id"],)):
        for city in ["Bengaluru", "Mysuru", "Mumbai"]:
            statements.append((
                "INSERT OR IGNORE INTO manager_city_assignments(id, manager_user_id, city) VALUES (?, ?, ?)",
                (f"mcity_{uuid4().hex[:10]}", manager["id"], city),
            ))
    if not row("SELECT sport_slug FROM sport_home_visibility LIMIT 1"):
        visibility = []
        for sport_slug, show_on_home, sort_order in visibility:
            statements.append((
                "INSERT OR IGNORE INTO sport_home_visibility(sport_slug, show_on_home, sort_order, updated_by) VALUES (?, ?, ?, ?)",
                (sport_slug, show_on_home, sort_order, manager["id"] if manager else None),
            ))
    if not row("SELECT slug FROM news_posts LIMIT 1"):
        published = now()
        news_posts = []
        statements += [(
            """
            INSERT INTO news_posts (
              slug, title, short_description, image, category, sport, tournament_slug,
              city, status, is_highlight, author_id, published_at, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            item,
        ) for item in news_posts]
        news_blocks = {}
        for post_slug, blocks in news_blocks.items():
            for sort_order, (block_type, content) in enumerate(blocks, start=1):
                statements.append((
                    "INSERT INTO news_blocks(id, post_slug, block_type, content_json, sort_order) VALUES (?, ?, ?, ?, ?)",
                    (f"nblock_{uuid4().hex[:10]}", post_slug, block_type, json.dumps({"text": content}), sort_order),
                ))
    rich_news_blocks = {}
    for post_slug, blocks in rich_news_blocks.items():
        existing_block_count = row("SELECT COUNT(*) AS count FROM news_blocks WHERE post_slug = ?", (post_slug,))
        if existing_block_count and existing_block_count["count"] < 5:
            next_order = existing_block_count["count"] + 1
            for offset, (block_type, content) in enumerate(blocks):
                statements.append((
                    "INSERT INTO news_blocks(id, post_slug, block_type, content_json, sort_order) VALUES (?, ?, ?, ?, ?)",
                    (f"nblock_{uuid4().hex[:10]}", post_slug, block_type, json.dumps({"text": content}), next_order + offset),
                ))
    if not row("SELECT id FROM leaderboard_records LIMIT 1"):
        leaderboard = []
        for sport, team_name, city, rank, tournaments_won, win_rate, points, record_label in leaderboard:
            statements.append((
                "INSERT INTO leaderboard_records(id, sport, team_name, city, rank, tournaments_won, win_rate, points, record_label) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (f"leader_{uuid4().hex[:10]}", sport, team_name, city, rank, tournaments_won, win_rate, points, record_label),
            ))
    if not row("SELECT slug FROM home_discovery_cards LIMIT 1"):
        discovery_cards = []
        statements += [(
            """
            INSERT OR IGNORE INTO home_discovery_cards (
              slug, label, title, sport, tournament_slug, sponsor_name, sponsor_image, image,
              event_date, description, sponsor_details, register_path, sort_order, published
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            item,
        ) for item in discovery_cards]
    extra_discovery_cards = []
    for item in extra_discovery_cards:
        if not row("SELECT slug FROM home_discovery_cards WHERE slug = ?", (item[0],)):
            statements.append((
                """
                INSERT OR IGNORE INTO home_discovery_cards (
                  slug, label, title, sport, tournament_slug, sponsor_name, sponsor_image, image,
                  event_date, description, sponsor_details, register_path, sort_order, published
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                item,
            ))
    if not row("SELECT id FROM live_highlights LIMIT 1"):
        statements.append((
            """
            INSERT OR IGNORE INTO live_highlights (
              id, match_id, title, stage_label, home_team, away_team, home_score, away_score,
              image, description, impact_notes, link_path, sort_order, published
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "live_highlight_primary",
                "match-48",
                "Corporate T20 Semi-Final Impact Watch",
                "Semi-Final Live",
                "India Forge",
                "England XI",
                "156/4",
                "Yet to bat",
                "/assets/cricket-stadium.png",
                "The current homepage highlight is selected from the live match feed so high-impact matches such as semi-finals, finals, and close chases can surface automatically instead of showing placeholder analytics.",
                "Live score, batting momentum, individual player scores, match clock, substitutions, highlights, and commentary are ready for the match center.",
                "/live/match-48",
                1,
                1,
            ),
        ))
    if not row("SELECT slug FROM sponsor_logos LIMIT 1"):
        sponsor_logos = []
        statements += [(
            "INSERT OR IGNORE INTO sponsor_logos(slug, name, image, link_url, sort_order, published) VALUES (?, ?, ?, ?, ?, ?)",
            item,
        ) for item in sponsor_logos]
    statements.append((
        """
        INSERT INTO sponsor_logos(slug, name, image, link_url, sort_order, published)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET image = excluded.image, link_url = excluded.link_url, published = excluded.published
        """,
        ("smartsportz", "SmartSportz", "/assets/logo.png", "https://smart-sportz-dun.vercel.app/", 1, 1),
    ))
    if statements:
        execute_many(statements)
        audit_execute(
            "INSERT INTO audit_logs(actor, action, entity, entity_id, message, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("system", "seed_upgrade", "database", "local", "Operational bracket and registration data seeded", now()),
        )
