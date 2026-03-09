import os

import psycopg2
from psycopg2.extras import RealDictCursor


class SharedStorage:
    def __init__(self, dsn: str = ""):
        self.dsn = (dsn or os.getenv("DATABASE_URL", "")).strip()
        if not self.dsn:
            raise ValueError("DATABASE_URL is empty")

    def _connect(self):
        return psycopg2.connect(
            self.dsn,
            cursor_factory=RealDictCursor,
            connect_timeout=15,
            application_name="reportbot",
        )

    def init(self):
        from services_supabase_sync_schema import init_schema
        init_schema(self.dsn)

    def _fetchone(self, sql, params=()):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchone()

    def _fetchall(self, sql, params=()):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return list(cur.fetchall())

    def get_stats_24h(self):
        opened = self._fetchone(
            "SELECT COUNT(*) AS cnt FROM shared_exchange_events WHERE event_type='opened_exchange' AND created_at >= NOW() - INTERVAL '24 hours'"
        )["cnt"]
        new_requests = self._fetchone(
            "SELECT COUNT(*) AS cnt FROM shared_exchange_requests WHERE created_at >= NOW() - INTERVAL '24 hours'"
        )["cnt"]
        paid = self._fetchone(
            "SELECT COUNT(*) AS cnt FROM shared_exchange_events WHERE event_type='paid' AND created_at >= NOW() - INTERVAL '24 hours'"
        )["cnt"]
        qr = self._fetchone(
            "SELECT COUNT(*) AS cnt FROM shared_exchange_events WHERE event_type='qr_requested' AND created_at >= NOW() - INTERVAL '24 hours'"
        )["cnt"]
        wallet = self._fetchone(
            "SELECT COUNT(*) AS cnt FROM shared_exchange_events WHERE event_type='wallet_urgent' AND created_at >= NOW() - INTERVAL '24 hours'"
        )["cnt"]
        turnover_rows = self._fetchall(
            """
            SELECT from_currency, SUM(amount_from) AS total
            FROM shared_exchange_requests
            WHERE created_at >= NOW() - INTERVAL '24 hours'
            GROUP BY from_currency
            ORDER BY from_currency
            """
        )
        totals = {r["from_currency"]: float(r["total"] or 0) for r in turnover_rows}
        return {
            "opened": int(opened or 0),
            "new_requests": int(new_requests or 0),
            "paid": int(paid or 0),
            "qr": int(qr or 0),
            "wallet": int(wallet or 0),
            "unpaid": max(int(new_requests or 0) - int(paid or 0), 0),
            "totals": totals,
        }

    def get_opened_rows_24h(self):
        return self._fetchall(
            """
            SELECT created_at, user_id, username, profile_link
            FROM shared_exchange_events
            WHERE event_type='opened_exchange' AND created_at >= NOW() - INTERVAL '24 hours'
            ORDER BY created_at ASC
            """
        )

    def get_request_rows_24h(self):
        return self._fetchall(
            """
            SELECT *
            FROM shared_exchange_requests
            WHERE created_at >= NOW() - INTERVAL '24 hours'
            ORDER BY created_at ASC
            """
        )
