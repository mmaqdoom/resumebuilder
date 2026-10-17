import os
import unittest
from unittest.mock import patch

from config import get_database_url


class DatabaseConfigurationTests(unittest.TestCase):
    def test_neon_url_takes_precedence_and_uses_psycopg_driver(self):
        with patch.dict(
            os.environ,
            {
                "NEON_DATABASE_URL": "postgresql://neon.example/db?sslmode=require",
                "DATABASE_URL": "postgresql://render.example/db",
            },
        ):
            self.assertEqual(
                get_database_url(),
                "postgresql+psycopg://neon.example/db?sslmode=require",
            )

    def test_legacy_postgres_url_remains_supported(self):
        with patch.dict(
            os.environ,
            {"NEON_DATABASE_URL": "", "DATABASE_URL": "postgres://render.example/db"},
        ):
            self.assertEqual(
                get_database_url(),
                "postgresql+psycopg://render.example/db",
            )


if __name__ == "__main__":
    unittest.main()
