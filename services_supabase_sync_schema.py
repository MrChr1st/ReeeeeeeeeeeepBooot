import psycopg2
from psycopg2.extras import RealDictCursor


def init_schema(dsn: str):
    with psycopg2.connect(dsn, cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS shared_exchange_requests (
                    request_id BIGINT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    username TEXT DEFAULT '',
                    profile_link TEXT DEFAULT '',
                    from_currency TEXT NOT NULL,
                    to_currency TEXT NOT NULL,
                    amount_from DOUBLE PRECISION NOT NULL,
                    amount_to DOUBLE PRECISION NOT NULL,
                    receive_details TEXT NOT NULL DEFAULT '',
                    payment_method TEXT NOT NULL DEFAULT '',
                    payment_submethod TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'waiting_payment',
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    paid_at TIMESTAMP NULL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS shared_exchange_events (
                    id BIGSERIAL PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    request_id BIGINT NULL,
                    user_id BIGINT NULL,
                    username TEXT DEFAULT '',
                    profile_link TEXT DEFAULT '',
                    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS shared_users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT DEFAULT '',
                    language TEXT DEFAULT 'ru',
                    ref_code TEXT DEFAULT '',
                    referred_by BIGINT NULL,
                    is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )
            cur.execute("CREATE INDEX IF NOT EXISTS idx_shared_events_created ON shared_exchange_events(created_at DESC)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_shared_events_type_created ON shared_exchange_events(event_type, created_at DESC)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_shared_requests_created ON shared_exchange_requests(created_at DESC)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_shared_users_created ON shared_users(created_at DESC)")
            conn.commit()
