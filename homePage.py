import tkinter as tk
from tkinter import ttk, messagebox
import backend
from page import AppPage

class Home(AppPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        notification = Notification(self)
        notification.grid(row=0, column=0, sticky="nsew")

class Notification(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.current_user = backend.current_backend.get_current_user()
        
        if not self.current_user:
            login_prompt_label = tk.Label(self, 
                                          text="Please log in to view alerts in your region", 
                                          font=backend.current_backend.get_font('italic'),
                                          wraplength=270,
                                          justify=tk.CENTER)
            login_prompt_label.grid(row=0, column=0, padx=15, pady=20)

        elif isinstance(self.current_user, backend.Employee):
            pw = ttk.PanedWindow(self, orient=tk.VERTICAL)
            pw.pack(fill="both", expand=True, padx=10, pady=5)

            tasks_container = ttk.Frame(pw)
            tasks_container.pack(fill="both", expand=True)
            pw.add(tasks_container)
            ttk.Label(tasks_container, text="My Pending Tasks", font=backend.current_backend.get_font("default_bold")).pack(anchor="w", pady=(0,5))
            tasks_text = tk.Text(tasks_container, wrap='word', height=10, highlightthickness=0, borderwidth=0, font=backend.current_backend.get_font())
            tasks_text.pack(fill="both", expand=True)
            
            tasks = self.current_user.get_alerts()
            if tasks:
                for task in tasks:
                    tasks_text.insert(tk.END, f"\u2022 {task}\n\n")
            else:
                tasks_text.insert(tk.END, "No pending tasks.")
            tasks_text.config(state='disabled')
            
            reports_container = ttk.Frame(pw)
            reports_container.pack(fill="both", expand=True)
            pw.add(reports_container)
            ttk.Label(reports_container, text="Recent Customer Reports", font=backend.current_backend.get_font("default_bold")).pack(anchor="w", pady=(0,5))
            reports_text = tk.Text(reports_container, wrap='word', height=10, highlightthickness=0, borderwidth=0, font=backend.current_backend.get_font())
            reports_text.pack(fill="both", expand=True)
            
            all_reports = backend.current_backend.get_all_reports()
            if all_reports:
                for report in all_reports:
                    reports_text.insert(tk.END, f"\u2022 {report}\n\n")
            else:
                reports_text.insert(tk.END, "No customer reports found.")
            reports_text.config(state='disabled')

        else:
            alerts_frame = ttk.Frame(self)
            alerts_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
            alerts_frame.columnconfigure(0, weight=1)

            ttk.Label(alerts_frame, text="Alerts", font=backend.current_backend.get_font("default_bold")).grid(row=0, column=0, sticky="w")
            
            alerts_text = tk.Text(alerts_frame, wrap='word', height=12, highlightthickness=0, borderwidth=0, font=backend.current_backend.get_font())
            alerts_text.grid(row=1, column=0, sticky="nsew", pady=5)
            
            alerts = self.current_user.get_alerts()
            if alerts:
                for alert in alerts:
                    alerts_text.insert(tk.END, f"\u2022 {alert}\n\n")
            else:
                alerts_text.insert(tk.END, "No system alerts at this time.")
            alerts_text.config(state='disabled')

            report_frame = ttk.Frame(self)
            report_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
            report_frame.columnconfigure(0, weight=1)

            ttk.Label(report_frame, text="Report an Issue", font=backend.current_backend.get_font("default_bold")).grid(row=0, column=0, sticky="w", pady=(5,0))
            
            self.report_text = tk.Text(report_frame, height=4, font=backend.current_backend.get_font())
            self.report_text.grid(row=1, column=0, sticky="ew", pady=5)
            self.report_text.bind("<Return>", self.submit_on_enter)
            
            submit_btn = ttk.Button(report_frame, text="Submit Report", command=self.submit_customer_report)
            submit_btn.grid(row=2, column=0, pady=(0, 10))
            
    def submit_on_enter(self, event):
        self.submit_customer_report()
        return "break"

    def submit_customer_report(self):
        description = self.report_text.get("1.0", tk.END).strip()
        if not description:
            messagebox.showwarning("Empty Report", "Please enter a description before submitting.")
            return

        success = backend.current_backend.submit_report(self.current_user.get_id(), description)

        if success:
            messagebox.showinfo("Report Submitted", "Thank you! Your report has been successfully submitted.")
            self.report_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Submission Failed", "There was an error submitting your report. Please try again.")