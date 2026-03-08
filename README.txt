РепортБот -> Supabase shared stats

Этот набор читает статистику, клиентов, заявки и Excel из общей Supabase/Postgres БД, в которую пишет КлиентБот.

Что добавить/заменить:
- report_bot_config.py
- report_handlers.py
- report_bot_main.py
- shared_storage.py
- services_supabase_sync_schema.py
- reportbot_shared.py

Что добавить в requirements.txt:
psycopg2-binary==2.9.9
openpyxl==3.1.5

Что должно быть в .env РепортБота:
BOT_TOKEN=...
DATABASE_URL=postgresql://...
PRIVATE_CHAT_ID=8500366305
AUTO_REPORT_HOURS=24
