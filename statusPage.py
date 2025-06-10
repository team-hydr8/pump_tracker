import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import backend

class Map(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.current_user = backend.current_backend.get_current_user()

        if not self.current_user:
            login_prompt_label = tk.Label(self, 
                                          text="Please log in to view water infrastructure.", 
                                          font=backend.current_backend.get_font("italic"),
                                          wraplength=270,
                                          justify=tk.CENTER)
            login_prompt_label.pack(expand=True, padx=15, pady=20)
            return

        canvas = tk.Canvas(self, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky='nsew')
        
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.columnconfigure(0, weight=1) 
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=300)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.build_map_content()


    def build_map_content(self):
        parent_frame = self.scrollable_frame
        
        pump_icon = ImageTk.PhotoImage(Image.open("images/pump.png").resize((60, 60)))
        tank_icon = ImageTk.PhotoImage(Image.open("images/tank.png").resize((60, 60)))
        
        self.pump_icon_ref = pump_icon
        self.tank_icon_ref = tank_icon
            
        is_staff = isinstance(self.current_user, backend.Employee)

        if is_staff:
            title_text = "All Water Infrastructure"
            infra = backend.current_backend.get_all_infrastructure()
        else: 
            title_text = f"Infrastructure for {self.current_user.region}"
            infra = backend.current_backend.get_infrastructure_by_region(self.current_user.region)

        title_label = tk.Label(parent_frame, text=title_text, font=backend.current_backend.get_font("title"),
                               anchor="center", wraplength=270, justify=tk.CENTER)
        title_label.grid(row=0, column=0, pady=(0, 15), padx=15, sticky="ew")


        pumps = infra.get('pumps', [])
        tanks = infra.get('tanks', [])
        
        current_row = 1
        
        if not pumps and not tanks:
            ttk.Label(parent_frame, text="No active infrastructure found.", font=backend.current_backend.get_font()).grid(row=current_row, column=0, padx=15)
            current_row += 1

        def create_item_frame(parent, row, image, id_text, region_text, status_text, integrity_text, usage_level_text, status_color):
            item_frame = ttk.Frame(parent)
            item_frame.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
            item_frame.columnconfigure(1, weight=1)

            ttk.Label(item_frame, image=image).grid(row=0, column=0, sticky='w', rowspan=4)
            
            info_frame = ttk.Frame(item_frame)
            info_frame.grid(row=0, column=1, sticky="nsew", padx=10)
            
            ttk.Label(info_frame, text=id_text, font=backend.current_backend.get_font()).pack(anchor="w")
            if region_text:
                ttk.Label(info_frame, text=region_text, font=backend.current_backend.get_font()).pack(anchor="w")
            ttk.Label(info_frame, text=status_text, foreground=status_color, font=backend.current_backend.get_font("default_bold")).pack(anchor="w")
            ttk.Label(info_frame, text=integrity_text, font=backend.current_backend.get_font()).pack(anchor="w")
            ttk.Label(info_frame, text=usage_level_text, font=backend.current_backend.get_font()).pack(anchor="w")
            return item_frame

        if pumps:
            ttk.Label(parent_frame, text="Water Pumps", font=backend.current_backend.get_font("default_bold")).grid(row=current_row, column=0, pady=(10,5), sticky="w", padx=15)
            current_row += 1
            for pump in pumps:
                status_enum = pump.get_status()
                status, color = self.get_status_info(status_enum)
                region = f"Region: {pump.region}" if is_staff else None
                
                converted_usage, unit_label = backend.current_backend.convert_volume(pump.get_water_usage())
                usage_text = f"Usage: {converted_usage:,.1f} {unit_label}"
                
                create_item_frame(parent_frame, current_row, pump_icon, f"Pump ID: {pump.get_id()}", region, f"Status: {status}", f"Integrity: {pump.get_integrity()}%", usage_text, color)
                current_row += 1

        if tanks:
            ttk.Label(parent_frame, text="Water Tanks", font=backend.current_backend.get_font("default_bold")).grid(row=current_row, column=0, pady=(10,5), sticky="w", padx=15)
            current_row += 1
            for tank in tanks:
                status_enum = tank.get_status()
                status, color = self.get_status_info(status_enum)
                region = f"Region: {tank.region}" if is_staff else None

                converted_level, unit_label = backend.current_backend.convert_volume(tank.get_water_level())
                level_text = f"Level: {converted_level:,.1f} {unit_label}"
                
                create_item_frame(parent_frame, current_row, tank_icon, f"Tank ID: {tank.get_id()}", region, f"Status: {status}", f"Integrity: {tank.get_integrity()}%", level_text, color)
                current_row += 1
        
    def get_status_info(self, status_enum):
        if status_enum == backend.PumpStatus.GREEN:
            return "Good", "green"
        elif status_enum == backend.PumpStatus.YELLOW:
            return "Warning", "orange"
        else:
            return "Critical", "red"