import tkinter as tk
from database import DatabaseManager
from gui import MybooksGui


def main() -> None:
    """
    Application Entry Point.
    Orchestrates Dependency Injection between Persistence Layer and Presentation Layer.
    """
    # 1. Initialize Persistence Layer (Database)
    db = DatabaseManager("chef_master.db")

    # Seed initial demo records if database is empty for immediate portfolio demonstration
    if not db.get_all_recipes():
        db.add_recipe("Classic Carbonara", "25m")
        db.add_recipe("Greek Salad", "10m")
        db.add_recipe("Beef Bourguignon", "120m")

    # 2. Instantiate Tkinter Main Window
    root = tk.Tk()

    # 3. Mount Presentation Layer Controller
    app = MybooksGui(root)

    # Hydrate in-memory GUI list with persistent records from SQLite
    db_records = db.get_all_recipes()
    if db_records:
        app.all_recipes = db_records

    # 4. Start Tkinter Non-Blocking Event Loop
    root.mainloop()


if __name__ == "__main__":
    main()
