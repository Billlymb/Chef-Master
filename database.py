import sqlite3
from typing import List, Tuple


class DatabaseManager:
    """Handles persistent SQLite operations for Chef Master with strict query parameterization."""

    def __init__(self, db_path: str = "chef_master.db") -> None:
        self.db_path = db_path
        self.init_schema()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Creates and returns a connection to SQLite database.
        Row factory enables column-name access for clean data parsing.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        """Initializes database schema with constraints and primary keys."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    prep_time TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_recipe(self, name: str, prep_time: str) -> bool:
        """
        Inserts a new recipe record.
        Uses parameterized queries (? placeholders) to prevent SQL Injection vulnerabilities.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO recipes (name, prep_time)
                    VALUES (?, ?)
                """,
                    (name.strip(), prep_time.strip()),
                )
                conn.commit()
                return True
        except sqlite3.Error as err:
            print(f"[Database Error] Insertion failed: {err}")
            return False

    def get_all_recipes(self) -> List[Tuple[str, str]]:
        """
        Retrieves all stored recipes ordered by latest creation.
        Why Tuples? Returns immutable data structures to maintain state integrity in the GUI.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name, prep_time FROM recipes ORDER BY id DESC"
                )
                rows = cursor.fetchall()
                return [(row["name"], row["prep_time"]) for row in rows]
        except sqlite3.Error as err:
            print(f"[Database Error] Query failed: {err}")
            return []

    def search_recipes(self, keyword: str) -> List[Tuple[str, str]]:
        """Performs wildcard search on recipe names."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT name, prep_time 
                    FROM recipes 
                    WHERE name LIKE ? 
                    ORDER BY id DESC
                """,
                    (f"%{keyword.strip()}%",),
                )
                rows = cursor.fetchall()
                return [(row["name"], row["prep_time"]) for row in rows]
        except sqlite3.Error as err:
            print(f"[Database Error] Search query failed: {err}")
            return []

    def delete_recipe_by_name(self, name: str) -> bool:
        """Deletes recipe records matching a given name."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM recipes WHERE name = ?", (name.strip(),)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as err:
            print(f"[Database Error] Deletion failed: {err}")
            return False
