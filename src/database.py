import sqlite3
import os

# Get the project root directory (one level up from src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "dining_optimization.db")

def init_db():
    """Initializes the SQLite database with the schema defined in the Interim Report."""
    if not os.path.exists("data"):
        os.makedirs("data")
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Table: Menu [cite: 556]
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hall_name TEXT,
            date DATE,
            meal_period TEXT,
            item_name TEXT,
            category TEXT,
            tags TEXT
        )
    ''')

    # Table: Traffic [cite: 565]
    c.execute('''
        CREATE TABLE IF NOT EXISTS traffic (
            traffic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hall_name TEXT,
            date DATE,
            meal_period TEXT,
            traffic_count INTEGER
        )
    ''')

    # Table: Weather [cite: 572]
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            meal_period TEXT,
            avg_temp REAL,
            precipitation_mm REAL
        )
    ''')

    # Table: Events [cite: 579]
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            event_type TEXT,
            expected_attendance INTEGER,
            nearby_hall TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
