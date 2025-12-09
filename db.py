# services/database.py
import os
import logging
from contextlib import contextmanager
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import pg8000

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Simple wrapper around pg8000 so local tooling can talk to Cloud SQL through
    the Cloud SQL Auth Proxy (running on localhost).
    """

    def __init__(self):
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST", "127.0.0.1")
        self.db_port = int(os.getenv("DB_PORT", "5432"))

    def _get_connection(self, retries=3, delay=0.5):
        last_err = None
        for attempt in range(retries):
            try:
                return pg8000.connect(
                    host=self.db_host,
                    port=self.db_port,
                    user=self.db_user,
                    password=self.db_password,
                    database=self.db_name,
                )
            except Exception as e:
                last_err = e
                logger.warning(
                    f"Postgres connection attempt {attempt+1}/{retries} failed: {e}"
                )
                time.sleep(delay)
        logger.error(
            f"Error creating Postgres connection after {retries} attempts: {last_err}"
        )
        raise last_err

    @contextmanager
    def get_connection(self):
        """Get database connection"""
        conn = None
        try:
            conn = self._get_connection()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass


# Global database manager instance
db_manager = DatabaseManager()