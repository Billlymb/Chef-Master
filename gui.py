import tkinter as tk
from tkinter import messagebox, ttk


class MybooksGui:
    """
    Front-End Subsystem Controller for Chef Master Application.
    Implements Single Page Architecture (SPA) with Centralized Routing.
    """

    def __init__(self, root):
        self.current_user = None
        self.all_recipes = []  # RAM State Storage: Keeps active recipes in memory
        self.root = root
        self.root.title("Chef Master - Recipe Management System")
        self.root.geometry("600x650")
        self.root.config(bg="green")

        # Base Container Frame: Acts as the primary canvas for all dynamic SPA views
        self.main_Frame = tk.Frame(self.root, bg="green")
        self.main_Frame.pack(fill="both", expand=True)

        # Routing Map: Maps route keys to view methods.
        # Why lambda? Defers method execution until the route is triggered.
        self.views = {
            "login": self.create_login_widget,
            "dashboard": lambda: self.show_dashboard(self.current_user),
            "create": self.screen_create,
            "search": self.screen_search,
            "results": self.screen_results,
            "edit": self.screen_edit,
            "execute": self.screen_execute,
        }

        # Mount initial view via the Central Router
        self.open_view("login")

    def open_view(self, name: str) -> None:
        """
        Central Router Method.
        Why? Enforces single-window SPA navigation and centralizes view lifecycles.
        """
        if name not in self.views:
            return
        self.clear_screen()  # Unmount active UI components
        self.views[name]()  # Dynamically execute and mount the requested view

    def clear_screen(self):
        """
        Destroys active widgets inside the container frame.
        Why? Prevents widget stacking and memory bloat during screen transitions.
        """
        for widget in self.main_Frame.winfo_children():
            widget.destroy()

    # --- VIEW: LOGIN SCREEN ---
    def create_login_widget(self):
        tk.Label(
            self.main_Frame,
            text="👨🍳 Chef Login",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="green",
        ).grid(row=0, column=0, columnspan=2, pady=40)

        tk.Label(
            self.main_Frame,
            text="Username:",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
        ).grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.ent_user = tk.Entry(self.main_Frame, font=("Arial", 12))
        self.ent_user.grid(row=1, column=1, padx=20, pady=10)

        tk.Label(
            self.main_Frame,
            text="Password:",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
        ).grid(row=2, column=0, padx=20, pady=10, sticky="e")
        # Why show="*"? Masks password input for security standards.
        self.ent_pass = tk.Entry(
            self.main_Frame, font=("Arial", 12), show="*"
        )
        self.ent_pass.grid(row=2, column=1, padx=20, pady=10)

        tk.Button(
            self.main_Frame,
            text="Login",
            bg="black",
            fg="white",
            width=20,
            command=self.handle_login,
        ).grid(row=3, column=0, columnspan=2, pady=30)

    def handle_login(self):
        # Why .strip()? Prevents accidental whitespace input validation errors.
        user = self.ent_user.get().strip()
        if user:
            self.current_user = user
            messagebox.showinfo("Success", f"Welcome Chef {user}!")
            self.open_view("dashboard")
        else:
            messagebox.showwarning(
                "Error", "Please fill in all credentials!"
            )

    # --- VIEW: MAIN DASHBOARD ---
    def show_dashboard(self, username):
        tk.Label(
            self.main_Frame,
            text=f"Control Panel: {username}",
            font=("Arial", 16, "bold"),
            bg="green",
            fg="white",
        ).grid(row=0, column=0, pady=30, padx=10)

        # Dashboard Navigation Buttons calling the SPA Router
        tk.Button(
            self.main_Frame,
            text="📝 Add New Recipe",
            width=30,
            command=lambda: self.open_view("create"),
        ).grid(row=1, column=0, pady=5, padx=130)
        tk.Button(
            self.main_Frame,
            text="🔍 Search Recipes",
            width=30,
            command=lambda: self.open_view("search"),
        ).grid(row=2, column=0, pady=5)
        tk.Button(
            self.main_Frame,
            text="📊 Statistics",
            width=30,
            command=lambda: self.open_view("results"),
        ).grid(row=3, column=0, pady=5)
        tk.Button(
            self.main_Frame,
            text="⚙ Edit / Delete (Database Hook)",
            width=30,
            command=lambda: self.open_view("edit"),
        ).grid(row=4, column=0, pady=5)
        tk.Button(
            self.main_Frame,
            text="🍳 Execute Simulation",
            width=30,
            command=lambda: self.open_view("execute"),
        ).grid(row=5, column=0, pady=5)

        tk.Button(
            self.main_Frame,
            text="Log out",
            bg="red",
            fg="white",
            width=20,
            command=lambda: self.open_view("login"),
        ).grid(row=6, column=0, pady=30)

    # --- VIEW: CREATE RECIPE ---
    def screen_create(self):
        tk.Label(
            self.main_Frame,
            text="📝 New Recipe Entry",
            font=("Arial", 18, "bold"),
            bg="green",
            fg="white",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(
            self.main_Frame, text="Recipe Name:", bg="green", fg="white"
        ).grid(row=1, column=0, pady=10)
        self.ent_name = tk.Entry(self.main_Frame)
        self.ent_name.grid(row=1, column=1)

        tk.Label(
            self.main_Frame, text="Prep Time (mins):", bg="green", fg="white"
        ).grid(row=2, column=0, pady=10)
        self.ent_time = tk.Entry(self.main_Frame)
        self.ent_time.grid(row=2, column=1)

        tk.Button(
            self.main_Frame, text="Save Recipe", command=self.action_save
        ).grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(
            self.main_Frame,
            text="Back",
            command=lambda: self.open_view("dashboard"),
        ).grid(row=4, column=0, columnspan=2)

    def action_save(self):
        n = self.ent_name.get().strip()
        t = self.ent_time.get().strip()
        if n and t:
            # Why Tuple? Guarantees record immutability once created in memory.
            self.all_recipes.append((n, t))
            messagebox.showinfo("Success", "Recipe saved successfully!")
            self.open_view("dashboard")
        else:
            messagebox.showwarning(
                "Error", "Please fill in all required fields!"
            )

    # --- VIEW: SEARCH RECIPES (TREEVIEW) ---
    def screen_search(self):
        tk.Label(
            self.main_Frame,
            text="🔍 Stored Recipes",
            font=("Arial", 18, "bold"),
            bg="green",
            fg="white",
        ).grid(row=0, column=0, pady=20)

        cols = ("Name", "Prep Time")
        self.tree = ttk.Treeview(self.main_Frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)

        # Populate Treeview dynamically from RAM state
        for r in self.all_recipes:
            self.tree.insert("", "end", values=r)

        self.tree.grid(row=1, column=0, padx=20, pady=10)
        tk.Button(
            self.main_Frame,
            text="
