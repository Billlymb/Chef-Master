# 🍳 Chef Master - Recipe Management System (GUI Subsystem)

## 📌 Overview
Chef Master is a desktop application built with Python and Tkinter for managing culinary recipes, simulating cooking processes, and inspecting live analytics.

This repository contains the **Front-End / Presentation Layer** of the application, engineered using a **Single Page Architecture (SPA)** and a **Centralized Router** pattern to ensure seamless single-window navigation and zero UI clutter.

---

## 🏗️ Architectural Highlights & Engineering Decisions ("The Why")

* **Single Page Architecture (SPA):** Instead of spawning multiple top-level windows (`tk.Toplevel`), all views are dynamically mounted and unmounted on a single root frame (`main_Frame`). This maintains UI stability and a consistent desktop UX.
* **Centralized Router (`open_view`):** Implements a routing map dictionary (`self.views`) that maps route keys to view-rendering methods. It decouples screen navigation logic from individual view widgets.
* **Widget Lifecycle Management (`clear_screen`):** Destroys active child widgets (`winfo_children()`) before mounting a new view to prevent memory leaks and visual widget stacking.
* **Data State & Immutability:** Recipes are stored in RAM within `self.all_recipes` using **Tuples**. Tuples were chosen over lists for individual records due to their **immutability**, guaranteeing data integrity during runtime.
* **Non-Blocking UI Async Loops (`root.after`):** The cooking progress bar simulation utilizes Tkinter's asynchronous `.after()` callback method instead of `time.sleep()`, preventing thread blockage and keeping the event loop 100% responsive.
* **Loose Coupling Design:** The `edit/delete` view serves as an architectural integration placeholder, demonstrating strict separation of concerns between the Presentation Layer and the underlying Persistence Layer (Database).

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.x
* **GUI Framework:** Tkinter & ttk (Treeview, Progressbar)
* **Design Pattern:** Object-Oriented Programming (OOP), Single Page Architecture (SPA), Centralized Routing Pattern
* **Data Structures:** Tuples (Immutable records), Lists (In-memory storage), Dictionaries (Routing Map)
