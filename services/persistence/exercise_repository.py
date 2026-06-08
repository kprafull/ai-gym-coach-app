import sqlite3
import os
from datetime import datetime
from turtle import st
from typing import List, Optional, Dict, Any
import streamlit as st
from streamlit import cursor


class ExerciseRepository:
    """Repository for managing exercise data persistence using SQLite."""
    
    DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/gym_coach.db")
    
    def __init__(self):
        """Initialize the repository and ensure database schema exists."""
        self._init_db()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory enabled."""
        conn = sqlite3.connect(self.DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        print("_init_db called")
        conn = self._get_connection()

        with conn:
            # Create users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create exercises table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS exercises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    exercise_name TEXT UNIQUE NOT NULL,
                    reps INTEGER NOT NULL default 0,
                    sets INTEGER NOT NULL default 0,
                    time INTEGER NOT NULL default 0, -- Time in seconds
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def add_exercise(self, user_id: str, exercise_name: str, reps: int, sets: int, time: int) -> int:
        """Add a new exercise to the database."""
        conn = self._get_connection()

        with conn:
            existing = conn.execute(
                """SELECT id FROM exercises WHERE 
                user_id = ? AND exercise_name = ? 
                AND Date(created_at) = Date('now')""",
                (user_id, exercise_name)
            ).fetchone()

            if existing:
                exercise_id = existing["id"]
                conn.execute(
                    "UPDATE exercises SET reps = reps + ?, sets = sets + ?, time = time + ? WHERE id = ?",
                    (reps, sets, time, existing["id"])
                )
                conn.commit()
            else:
                cursor = conn.execute(
                    "INSERT INTO exercises (user_id, exercise_name, reps, sets, time) VALUES (?, ?, ?, ?, ?)",
                    (user_id, exercise_name, reps, sets, time)
                )
                conn.commit()
                exercise_id = cursor.lastrowid
        return exercise_id
    
    def get_exercise_id(self, name: str) -> Optional[int]:
        """Get exercise ID by name."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM exercises WHERE name = ?", (name,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def get_user_exercises(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all exercises for a specific user."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT exercise_name, reps, sets, time, created_at FROM exercises WHERE user_id = ?", (user_id,))
        exercises = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return exercises
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        conn = self._get_connection()

        with conn:        
            res = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
            result = res.fetchone()
        return dict(result) if result else None
    
    def create_user(self, username: str, hashed_password: str) -> int:
        """Create a new user and return their ID."""
        conn = self._get_connection()
        
        try:
            with conn:
                cursor = conn.execute(
                    "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
                    (username, hashed_password)
                )
                conn.commit()
                user_id = cursor.lastrowid
                return user_id
        except sqlite3.IntegrityError:
            # Username already exists
            print(f"User '{username}' already exists.")
            return self.get_user(username)["id"]

    