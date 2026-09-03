import tkinter as tk
from database import DatabaseManager
from gui import ChefMasterGUI


def main() -> None:
    """
    Application Entry Point.
    Orchestrates Dependency Injection between Persistence Layer and Presentation Layer.
    """
    # 1. Initialize Persistence Layer
    db = DatabaseManager("chef_master.db")

    # Seed initial demo records if database is empty for immediate portfolio demonstration
    if not db.get_all_recipes():
        db.add_recipe("Classic Carbonara", "25m")
        db.add_recipe("Greek Salad", "10m")
        db.add_recipe("Beef Bourguignon", "120m")

    # 2. Instantiate Main Window
    root = tk.Tk()

    # 3. Mount Presentation Layer Controller with Injected Database Instance
    app = ChefMasterGUI(root, db_manager=db)

    # 4. Start Event Loop
    root.mainloop()


if __name__ == "__main__":
    main()
