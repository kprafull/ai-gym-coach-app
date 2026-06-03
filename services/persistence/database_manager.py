import sqlite3
import os
from typing import Any


class DatabaseManager:
    """Utility class for database operations and queries."""
    
    DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/gym_coach.db")
    
    @staticmethod
    def execute_query(query: str, params: tuple = ()) -> Any:
        """Execute a SELECT query and return results."""
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in results]
    
    @staticmethod
    def execute_update(query: str, params: tuple = ()) -> int:
        """Execute an UPDATE/INSERT/DELETE query and return affected rows."""
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        return affected_rows
    
    @staticmethod
    def reset_database() -> None:
        """Drop all tables and reinitialize the database."""
        conn = sqlite3.connect(DatabaseManager.DB_PATH)
        cursor = conn.cursor()
        
        # Drop tables in reverse order of dependencies
        cursor.execute("DROP TABLE IF EXISTS exercise_metrics")
        cursor.execute("DROP TABLE IF EXISTS workout_sessions")
        cursor.execute("DROP TABLE IF EXISTS exercises")
        
        conn.commit()
        conn.close()
        
        # Reinitialize
        from .exercise_repository import ExerciseRepository
        ExerciseRepository()
