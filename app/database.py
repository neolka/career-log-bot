import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path="data/career_log.db"):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        # Встановлюємо з'єднання з файлом бази даних
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        """Створює таблицю, якщо її ще немає."""
        query = """
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            context TEXT,
            action TEXT,
            result TEXT
        );
        """
        try:
            with self._get_connection() as conn:
                conn.execute(query)
                conn.commit()
        except Exception as e:
            logger.error(f"Error creating table: {e}")

    def add_achievement(self, user_id: int, answers: list):
        """Додає новий запис у базу."""
        query = """
        INSERT INTO achievements (user_id, date, context, action, result)
        VALUES (?, ?, ?, ?, ?)
        """
        # Готуємо дані (дата + ID + 3 відповіді)
        data = (
            user_id, 
            datetime.now().strftime("%Y-%m-%d"), 
            answers[0], 
            answers[1], 
            answers[2]
        )
        
        try:
            with self._get_connection() as conn:
                conn.execute(query, data)
                conn.commit()
            logger.info(f"Achievement saved to DB for user {user_id}")
        except Exception as e:
            logger.error(f"Error saving to DB: {e}")

    def get_achievements(self, user_id: int, limit: int = 5):
        """Отримує останні записи конкретного користувача."""
        query = """
        SELECT date, context, action, result 
        FROM achievements 
        WHERE user_id = ? 
        ORDER BY id DESC 
        LIMIT ?
        """
        try:
            with self._get_connection() as conn:
                # Це дозволяє звертатися до колонок за назвами, як у словнику
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(query, (user_id, limit))
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching from DB: {e}")
            return []