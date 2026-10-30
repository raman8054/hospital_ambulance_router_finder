"""CustomTkinter desktop dashboard for the ambulance route mini project."""

import tkinter as tk
import customtkinter as ctk

from dijkstra import dijkstra
from route_data import PLACES, ROADS

BG = "#07111F"
PANEL = "#0D1B2B"
PANEL_LIGHT = "#11243A"
TEXT = "#E7F6FF"
MUTED = "#91ABC4"
CYAN = "#00F0FF"
BLUE = "#168BFF"
GREEN = "#25E0AD"
RED = "#FF5C83"
FASTEST_PATH = "#FF007F"


class AmbulanceRouteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Ambulance Route Finder")
        self.root.geometry("1440x900")
        self.root.minsize(1180, 760)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color=BG)
        self.font_family = "Segoe UI"
        self.path = []
        self.build_ui()
        self.find_route()

    def font(self, size, weight="normal"):
        return ctk.CTkFont(family=self.font_family, size=size, weight=weight)

    def panel(self, parent, **kwargs):
        kwargs.setdefault("fg_color", PANEL)
        kwargs.setdefault("corner_radius", 12)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", "#263B51")
        return ctk.CTkFrame(parent, **kwargs)

    def build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        header = self.panel(self.root)
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 8))
        header.grid_columnconfigure(0, weight=1)
        title_area = ctk.CTkFrame(header, fg_color="transparent")
        title_area.grid(row=0, column=0, sticky="w", padx=20, pady=14)
        ctk.CTkLabel(title_area, text="HOSPITAL AMBULANCE ROUTE FINDER",
                     text_color=TEXT, font=self.font(23, "bold")).pack(anchor="w")
        ctk.CTkLabel(title_area, text="CITY RESPONSE NETWORK  /  DIJKSTRA ROUTE ENGINE",
                     text_color=CYAN, font=self.font(11, "bold")).pack(anchor="w", pady=(3, 0))
        ctk.CTkLabel(header, text="SYSTEM ONLINE", text_color=GREEN,
                     fg_color="#102B2C", corner_radius=8,
                     font=self.font(11, "bold")).grid(
                         row=0, column=1, sticky="e", padx=20, pady=15)

        dashboard = ctk.CTkFrame(self.root, fg_color="transparent")
        dashboard.grid(row=1, column=0, sticky="nsew", padx=18, pady=8)
        dashboard.grid_columnconfigure(0, weight=0, minsize=270)
        dashboard.grid_columnconfigure(1, weight=1, minsize=520)
        dashboard.grid_columnconfigure(2, weight=0, minsize=300)
        dashboard.grid_rowconfigure(0, weight=1)

        controls = self.panel(dashboard)
        controls.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        controls.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(controls, text="Route planner", text_color=TEXT,
                     font=self.font(18, "bold")).grid(row=0, column=0, sticky="w", padx=18, pady=(20, 3))
        ctk.CTkLabel(controls, text="Choose a unit and receiving hospital.",
                     text_color=MUTED, font=self.font(12), wraplength=225,
                     justify="left").grid(row=1, column=0, sticky="w", padx=18, pady=(0, 18))

        stations = [name for name, place in PLACES.items() if place[2] == "ambulance"]
        hospitals = [name for name, place in PLACES.items() if place[2] == "hospital"]
        self.start_var = ctk.StringVar(value=stations[0])
        self.end_var = ctk.StringVar(value=hospitals[0])
        ctk.CTkLabel(controls, text="AMBULANCE STARTING POINT", text_color=MUTED,
                     font=self.font(10, "bold")).grid(row=2, column=0, sticky="w", padx=18, pady=(4, 6))
        self.start = ctk.CTkComboBox(
            controls, values=stations, variable=self.start_var, state="readonly",
            font=self.font(12), dropdown_font=self.font(12), height=42, corner_radius=8,
            border_color="#31506C", button_color="#164A70", button_hover_color="#087EAE",
            fg_color=PANEL_LIGHT, text_color=TEXT, command=self._selection_changed)
        self.start.grid(row=3, column=0, sticky="ew", padx=18)
        ctk.CTkLabel(controls, text="DESTINATION HOSPITAL", text_color=MUTED,
                     font=self.font(10, "bold")).grid(row=4, column=0, sticky="w", padx=18, pady=(17, 6))
        self.end = ctk.CTkComboBox(
            controls, values=hospitals, variable=self.end_var, state="readonly",
            font=self.font(12), dropdown_font=self.font(12), height=42, corner_radius=8,
            border_color="#31506C", button_color="#164A70", button_hover_color="#087EAE",
            fg_color=PANEL_LIGHT, text_color=TEXT, command=self._selection_changed)
        self.end.grid(row=5, column=0, sticky="ew", padx=18)
        ctk.CTkButton(
            controls, text="Find fastest route", command=self.find_route,
            height=48, corner_radius=8, fg_color="#087EAE", hover_color="#006B9E",
            text_color="#FFFFFF", border_width=1, border_color=CYAN,
            font=self.font(13, "bold")).grid(
                row=6, column=0, sticky="ew", padx=18, pady=(20, 22))

        ctk.CTkLabel(controls, text="QUICK GUIDE", text_color=CYAN,
                     font=self.font(10, "bold")).grid(row=7, column=0, sticky="w", padx=18, pady=(2, 7))
        guide = self.panel(controls, fg_color=PANEL_LIGHT, corner_radius=10, border_color="#203B55")
        guide.grid(row=8, column=0, sticky="ew", padx=14)
        ctk.CTkLabel(guide, text="01  Select an ambulance\n\n02  Select a hospital\n\n03  Calculate the route",
                     text_color=TEXT, font=self.font(12), justify="left",
                     anchor="w").pack(fill="x", padx=13, pady=13)
        ctk.CTkLabel(controls, text="MAP KEY", text_color=CYAN,
                     font=self.font(10, "bold")).grid(row=9, column=0, sticky="w", padx=18, pady=(17, 7))
        ctk.CTkLabel(controls, text="Road labels show estimated travel time.\n\nCyan  ·  selected route\nPink  ·  fastest path",
                     text_color=MUTED, font=self.font(11), justify="left",
                     anchor="w").grid(row=10, column=0, sticky="ew", padx=18)

        map_panel = self.panel(dashboard)
        map_panel.grid(row=0, column=1, sticky="nsew", padx=5)
        map_panel.grid_rowconfigure(2, weight=1)
        map_panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(map_panel, text="LIVE CITY GRID", text_color=TEXT,
                     font=self.font(17, "bold")).grid(row=0, column=0, sticky="w", padx=17, pady=(16, 2))
        ctk.CTkLabel(map_panel, text=f"{len(PLACES)} locations   /   {len(ROADS)} roads   /   estimated minutes",
                     text_color=MUTED, font=self.font(11)).grid(row=1, column=0, sticky="w", padx=17, pady=(0, 10))
        self.canvas = tk.Canvas(map_panel, bg="#071522", highlightthickness=1,
                                highlightbackground="#263B51", relief="flat")
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=12, pady=8)
        self.canvas.bind("<Configure>", lambda _event: self.draw_map())
        ctk.CTkLabel(map_panel, text="Ambulance     Hospital     Junction     Fastest route",
                     text_color=CYAN, font=self.font(10, "bold")).grid(
                         row=3, column=0, sticky="w", padx=17, pady=(4, 13))

        details = self.panel(dashboard)
        details.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        details.grid_columnconfigure(0, weight=1)
        details.grid_rowconfigure(6, weight=1)
        ctk.CTkLabel(details, text="ROUTE SUMMARY", text_color=CYAN,
                     font=self.font(10, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=(18, 8))
        self.result = ctk.CTkLabel(details, text="Choose locations to start.", text_color=TEXT,
                                   fg_color="#102C43", corner_radius=10, justify="left",
                                   anchor="w", wraplength=250, font=self.font(13, "bold"))
        self.result.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        ctk.CTkLabel(details, text="ROAD-BY-ROAD DETAILS", text_color=CYAN,
                     font=self.font(10, "bold")).grid(row=2, column=0, sticky="w", padx=15, pady=(8, 6))
        self.route_details = ctk.CTkTextbox(details, height=155, corner_radius=8,
                                            border_width=1, border_color="#203B55",
                                            fg_color=PANEL_LIGHT, text_color=TEXT,
                                            font=self.font(11), wrap="word")
        self.route_details.grid(row=3, column=0, sticky="ew", padx=12)
        ctk.CTkLabel(details, text="DIJKSTRA'S STEPS", text_color=CYAN,
                     font=self.font(10, "bold")).grid(row=4, column=0, sticky="w", padx=15, pady=(17, 6))
        self.steps = ctk.CTkTextbox(details, corner_radius=8, border_width=1,
                                    border_color="#203B55", fg_color=PANEL_LIGHT,
                                    text_color="#C7DEF5", font=self.font(11), wrap="word")
        self.steps.grid(row=6, column=0, sticky="nsew", padx=12, pady=(0, 12))

    def _selection_changed(self, _value=None):
        self.find_route()

    def find_route(self):
        start, goal = self.start_var.get(), self.end_var.get()
        total, self.path, steps = dijkstra(start, goal, PLACES, ROADS)
        self.steps.configure(state="normal")
        self.steps.delete("1.0", "end")
        self.steps.insert("end", "\n\n".join(f"•  {step}" for step in steps))
        self.steps.configure(state="disabled")

        if total is None:
            self.result.configure(text="No road route connects these locations.", text_color=RED)
            detail_lines = ["No connected road route was found."]
        else:
            self.result.configure(
                text=f"FASTEST ESTIMATED TIME\n{total} minutes  /  {len(self.path) - 1} road segments",
                text_color=GREEN)
            road_times = {(first, second): minutes for first, second, minutes in ROADS}
            road_times.update({(second, first): minutes for first, second, minutes in ROADS})
            detail_lines = [f"{i + 1}. {first}\n   -> {second}  ·  {road_times[(first, second)]} min"
                            for i, (first, second) in enumerate(zip(self.path, self.path[1:]))]
            detail_lines.append(f"\nTOTAL  ·  {total} min")
        self.route_details.configure(state="normal")
        self.route_details.delete("1.0", "end")
        self.route_details.insert("end", "\n\n".join(detail_lines))
        self.route_details.configure(state="disabled")
        self.draw_map()

    def draw_map(self):
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 600)
        height = max(self.canvas.winfo_height(), 480)
        sx, sy = (width - 80) / 800, (height - 75) / 550

        def xy(x, y):
            return 40 + x * sx, 30 + y * sy

        def point(name):
            x, y, _kind = PLACES[name]
            return xy(x, y)

        for gx in range(20, width, 36):
            self.canvas.create_line(gx, 0, gx, height, fill="#0B2032", width=1)
        for gy in range(20, height, 36):
            self.canvas.create_line(0, gy, width, gy, fill="#0B2032", width=1)

        districts = [
            ("OLD TOWN", 12, 18, 260, 190, "#0D1930"),
            ("MARKET DISTRICT", 255, 18, 580, 210, "#0D2529"),
            ("RIVERFRONT", 255, 210, 590, 390, "#0C2030"),
            ("MEDICAL QUARTER", 585, 18, 800, 300, "#171432"),
            ("UNIVERSITY QUARTER", 255, 390, 800, 550, "#201A16"),
            ("SOUTH GATE", 12, 190, 255, 550, "#132219"),
        ]
        for label, left, top, right, bottom, fill in districts:
            x1, y1 = xy(left, top)
            x2, y2 = xy(right, bottom)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill,
                                         outline="#173049", width=2)

        river_points = [xy(x, y) for x, y in
                        ((390, 0), (430, 80), (390, 155), (435, 235),
                         (405, 315), (455, 405), (430, 550))]
        river_coords = [coord for pair in river_points for coord in pair]
        self.canvas.create_line(*river_coords, smooth=True, splinesteps=32,
                                fill="#07344A", width=26, capstyle="round")
        self.canvas.create_line(*river_coords, smooth=True, splinesteps=32,
                                fill="#0B5265", width=13, capstyle="round")
        for label, left, top, _right, _bottom, _fill in districts:
            x, y = xy(left + 12, top + 14)
            self.canvas.create_text(x, y, text=label, anchor="nw",
                                    fill="#51738D", font=self.font(8, "bold"))

        selected = {frozenset((self.path[i], self.path[i + 1]))
                    for i in range(len(self.path) - 1)}
        for first, second, minutes in ROADS:
            x1, y1 = point(first)
            x2, y2 = point(second)
            dx, dy = x2 - x1, y2 - y1
            length = max((dx * dx + dy * dy) ** 0.5, 1)
            control_x = (x1 + x2) / 2 - dy / length * 9
            control_y = (y1 + y2) / 2 + dx / length * 9
            path_coords = (x1, y1, control_x, control_y, x2, y2)
            is_fastest = frozenset((first, second)) in selected
            if is_fastest:
                self.canvas.create_line(*path_coords, smooth=True, splinesteps=24,
                                        fill="#063D55", width=14, capstyle="round", joinstyle="round")
                self.canvas.create_line(*path_coords, smooth=True, splinesteps=24,
                                        fill="#00F0FF", width=8, capstyle="round", joinstyle="round")
                self.canvas.create_line(*path_coords, smooth=True, splinesteps=24,
                                        fill="#FF007F", width=4, capstyle="round", joinstyle="round")
            else:
                self.canvas.create_line(*path_coords, smooth=True, splinesteps=20,
                                        fill="#24435C", width=5, capstyle="round", joinstyle="round")
                self.canvas.create_line(*path_coords, smooth=True, splinesteps=20,
                                        fill="#4B6C86", width=2, capstyle="round", joinstyle="round")
            mx = (x1 + control_x * 2 + x2) / 4
            my = (y1 + control_y * 2 + y2) / 4
            self.canvas.create_rectangle(mx - 22, my - 9, mx + 22, my + 9,
                                         fill="#0A1927", outline="#1B3B53", width=1)
            self.canvas.create_text(mx, my, text=f"{minutes}m", fill="#C4E8F5",
                                    font=self.font(8, "bold"))

        for index, (name, (_raw_x, _raw_y, kind)) in enumerate(PLACES.items()):
            x, y = point(name)
            color = {"ambulance": RED, "hospital": GREEN, "road": BLUE}[kind]
            radius = 13 if kind != "road" else 10
            if name in (self.start_var.get(), self.end_var.get()):
                halo = CYAN if name == self.start_var.get() else FASTEST_PATH
                self.canvas.create_oval(x - 22, y - 22, x + 22, y + 22,
                                        outline=halo, width=2)
            self.canvas.create_oval(x-radius-3, y-radius-3, x+radius+3, y+radius+3,
                                    fill="#142C41", outline="")
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius,
                                    fill=color, outline="#D9F8FF", width=2)
            marker = "A" if kind == "ambulance" else "H" if kind == "hospital" else str(index)
            self.canvas.create_text(x, y, text=marker, fill="#FFFFFF",
                                    font=self.font(8, "bold"))
            label_y = y + radius + 13
            label_width = min(max(52, len(name) * 4.8 + 12), 145)
            self.canvas.create_rectangle(x-label_width/2, label_y-9,
                                         x+label_width/2, label_y+10,
                                         fill="#091725", outline="#1B3B53", width=1)
            self.canvas.create_text(x, label_y, text=name, fill="#D9ECFF",
                                    font=self.font(8, "bold"))


if __name__ == "__main__":
    app = ctk.CTk()
    AmbulanceRouteApp(app)
    app.mainloop()
