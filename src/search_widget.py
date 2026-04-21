import tkinter as tk
import webbrowser
import pystray
from PIL import Image
import threading
import os
import sys
from screeninfo import get_monitors

# --- Constants ---
ICON_PATH = r"gmap_search.ico"

# --- App window ---
def create_widget():
    root = tk.Tk()
    root.title("GMap Search Widget")
    root.resizable(False, False)

    # Entry field
    entry = tk.Entry(root, width=30)
    entry.pack(pady=10, padx=10)
    entry.bind("<Return>", lambda event: search_map())  # 🔑 Enter triggers search

    # Search function
    def search_map():
        query = entry.get().strip()
        if not query:
            return

        # Detect route input
        if ">" in query:
            # Split and clean all waypoints
            parts = [p.strip() for p in query.split(">") if p.strip()]

            if len(parts) >= 2:
                # Encode each part
                waypoints = [p.replace(" ", "+") for p in parts]
                path = "/".join(waypoints)
                url = f"https://www.google.com/maps/dir/{path}"
            else:
                # fallback if something weird like "A >"
                url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
        else:
            # Normal search
            url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

        webbrowser.open(url)
        entry.delete(0, tk.END)



    # Button
    search_btn = tk.Button(root, text="Search in Map", command=search_map)
    search_btn.pack()

    # Snap to bottom-right of primary screen
    screen = get_monitors()[0]
    x = screen.width - 300 - 10  # window width + margin
    y = screen.height - 100 - 50  # window height + taskbar height approx
    root.geometry(f"300x100+{x}+{y}")

    # Keep hidden until tray clicked
    root.withdraw()

    def show_window():
        root.deiconify()
        root.lift()
        root.attributes('-topmost', True)
        root.after(500, lambda: root.attributes('-topmost', False))

    def quit_app(icon, item):
        icon.stop()
        root.destroy()
        sys.exit()

    # Tray icon setup
    def run_tray():
        image = Image.open(ICON_PATH).resize((64, 64))
        icon = pystray.Icon("map_widget", image, menu=pystray.Menu(
            pystray.MenuItem("Search", lambda: show_window()),
            pystray.MenuItem("Quit", quit_app)
        ))
        icon.run()

    threading.Thread(target=run_tray, daemon=True).start()

    root.mainloop()

# --- Launch ---
if __name__ == "__main__":
    create_widget()
