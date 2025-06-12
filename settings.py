import tkinter as tk
from tkinter import ttk, messagebox
import backend
from page import AppPage

class Settings(AppPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.current_user = backend.current_backend.get_current_user()

        settings_frame = ttk.LabelFrame(self, text="Display Settings")
        settings_frame.pack(fill="x", padx=15, pady=10)
        settings_frame.columnconfigure(1, weight=1)
        
        lang_label_frame = ttk.Frame(settings_frame)
        lang_label_frame.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(lang_label_frame, text="Language", font=backend.current_backend.get_font()).pack(side="left")
        ttk.Label(lang_label_frame, text="🌐", font=("Calibre", 16)).pack(side="left", padx=(2,0))
        self.language_var = tk.StringVar(value=backend.current_backend.get_language())
        language_combo = ttk.Combobox(settings_frame, textvariable=self.language_var, values=["English", "Afrikaans", "isiZulu"], state="readonly", font=backend.current_backend.get_font())
        language_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        language_combo.bind("<<ComboboxSelected>>", self.on_setting_change)

        ttk.Label(settings_frame, text="Units:", font=backend.current_backend.get_font()).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.units_var = tk.StringVar(value=backend.current_backend.get_measurement_unit_string())
        units_combo = ttk.Combobox(settings_frame, textvariable=self.units_var, values=["Metric (Litres)", "Imperial (Gallons)"], state="readonly", font=backend.current_backend.get_font())
        units_combo.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        units_combo.bind("<<ComboboxSelected>>", self.on_setting_change)

        ttk.Label(settings_frame, text="Font Size:", font=backend.current_backend.get_font()).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.font_var = tk.StringVar(value=backend.current_backend.get_font_size())
        font_combo = ttk.Combobox(settings_frame, textvariable=self.font_var, values=["Small", "Medium", "Large"], state="readonly", font=backend.current_backend.get_font())
        font_combo.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        font_combo.bind("<<ComboboxSelected>>", self.on_setting_change)

        if self.current_user:
            password_frame = ttk.LabelFrame(self, text="Change Password")
            password_frame.pack(fill="x", padx=15, pady=10)
            password_frame.columnconfigure(1, weight=1)

            ttk.Label(password_frame, text="Current Password:", font=backend.current_backend.get_font()).grid(row=0, column=0, sticky="w", padx=5, pady=5)
            self.current_pass_entry = ttk.Entry(password_frame, show="*", font=backend.current_backend.get_font())
            self.current_pass_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

            ttk.Label(password_frame, text="New Password:", font=backend.current_backend.get_font()).grid(row=1, column=0, sticky="w", padx=5, pady=5)
            self.new_pass_entry = ttk.Entry(password_frame, show="*", font=backend.current_backend.get_font())
            self.new_pass_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
            
            ttk.Label(password_frame, text="Confirm New Password:", font=backend.current_backend.get_font()).grid(row=2, column=0, sticky="w", padx=5, pady=5)
            self.confirm_pass_entry = ttk.Entry(password_frame, show="*", font=backend.current_backend.get_font())
            self.confirm_pass_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
            self.confirm_pass_entry.bind("<Return>", self.update_password_on_enter)

            update_btn = ttk.Button(password_frame, text="Update Password", command=self.update_password_action)
            update_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def on_setting_change(self, event=None):
        backend.current_backend.set_language(self.language_var.get())
        backend.current_backend.set_font_size(self.font_var.get())
        backend.current_backend.set_measurement_unit(self.units_var.get())
        
        self.controller.update_ttk_styles()
        self.controller.show_frame(Settings)

    def update_password_on_enter(self, event):
        self.update_password_action()

    def update_password_action(self):
        current_pass = self.current_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()

        if not all([current_pass, new_pass, confirm_pass]):
            messagebox.showerror("Error", "All password fields are required.")
            return
        
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New passwords do not match.")
            return
            
        success, message = backend.current_backend.change_password(
            self.current_user.get_id(),
            current_pass,
            new_pass
        )

        if success:
            messagebox.showinfo("Success", message)
            self.current_pass_entry.delete(0, tk.END)
            self.new_pass_entry.delete(0, tk.END)
            self.confirm_pass_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", message)