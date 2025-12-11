import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import threading

# Theme Colors (Dark/Premium)
BG_COLOR = "#2b2b2b"
ITEM_BG_COLOR = "#3c3f41"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#007acc"
HOVER_COLOR = "#4b4b4b"
PINNED_COLOR = "#ffd700"  # Gold
UNPINNED_COLOR = "#808080" # Grey

class ClipSyncApp:
    def __init__(self, root, storage, monitor):
        self.root = root
        self.storage = storage
        self.monitor = monitor
        
        self.root.title("ClipSync")
        self.root.geometry("400x600")
        self.root.configure(bg=BG_COLOR)
        self.root.attributes("-topmost", True) # Keep on top for utility feel

        # --- Styles ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure("TButton", background=ITEM_BG_COLOR, foreground=TEXT_COLOR, borderwidth=0)
        style.map("TButton", background=[('active', HOVER_COLOR)])

        # --- Header ---
        self.header_frame = tk.Frame(root, bg=BG_COLOR, height=50)
        self.header_frame.pack(fill="x", padx=10, pady=10)
        
        self.title_label = tk.Label(self.header_frame, text="ClipSync", font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
        self.title_label.pack(side="left")

        self.clear_btn = tk.Button(self.header_frame, text="Clear All", command=self.clear_history, bg=ITEM_BG_COLOR, fg=TEXT_COLOR, relief="flat", padx=10)
        self.clear_btn.pack(side="right")

        # --- Scrollable List Area ---
        self.canvas = tk.Canvas(root, bg=BG_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=380) # constrained width
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10)
        self.scrollbar.pack(side="right", fill="y")
        
        # --- Logic Hook ---
        # Polling for new items loop (UI update)
        self.root.after(100, self.check_clipboard)
        
        # Initial Render
        self.refresh_list()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def check_clipboard(self):
        # The monitor runs in background, but we need to refresh UI if storage changed?
        # Actually monitor calls callback. We can just set callback to trigger refresh.
        # But monitor running in thread calling TKinter updates directly is unsafe.
        # Better: Monitor updates Storage, then signals UI.
        # Or Monitor calls a method that schedules update on main thread.
        # Implemented strategy: Monitor has callback.
        # We'll pass a thread-safe callback wrapper.
        pass # Handled by callback passed to monitor in main.py

    def on_clipboard_change(self, text):
        # Called from background thread
        self.root.after(0, lambda: self._add_and_refresh(text))

    def _add_and_refresh(self, text):
        self.storage.add_item(text)
        self.refresh_list()

    def refresh_list(self):
        # Clear current widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        items = self.storage.get_items()
        
        for idx, item in enumerate(items):
            self._create_item_row(idx, item)

    def _create_item_row(self, idx, item):
        text = item['text']
        is_pinned = item.get('pinned', False)
        
        # Row Frame
        row = tk.Frame(self.scrollable_frame, bg=ITEM_BG_COLOR, pady=5, padx=5)
        row.pack(fill="x", pady=2)
        
        # Pin Button
        pin_char = "★" if is_pinned else "☆"
        pin_color = PINNED_COLOR if is_pinned else UNPINNED_COLOR
        
        pin_btn = tk.Label(row, text=pin_char, font=("Segoe UI", 14), bg=ITEM_BG_COLOR, fg=pin_color, cursor="hand2")
        pin_btn.pack(side="left", padx=5)
        pin_btn.bind("<Button-1>", lambda e, i=idx: self.toggle_pin(i))

        # Content Label (Truncated)
        display_text = (text[:40] + '...') if len(text) > 40 else text
        # Remove newlines for preview
        display_text = display_text.replace('\n', ' ')
        
        lbl = tk.Label(row, text=display_text, bg=ITEM_BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10), anchor="w", justify="left")
        lbl.pack(side="left", fill="x", expand=True, padx=5)
        
        # Click row to copy
        lbl.bind("<Button-1>", lambda e, t=text: self.copy_to_clipboard(t))
        row.bind("<Button-1>", lambda e, t=text: self.copy_to_clipboard(t))
        
        # Copy Button (explicit)
        copy_btn = tk.Button(row, text="Copy", command=lambda t=text: self.copy_to_clipboard(t), 
                             bg=ACCENT_COLOR, fg="white", relief="flat", font=("Segoe UI", 8))
        copy_btn.pack(side="right", padx=5)

    def toggle_pin(self, index):
        self.storage.toggle_pin(index)
        self.refresh_list()

    def copy_to_clipboard(self, text):
        # pause monitor briefly to avoid strictly detecting self-copy as new?
        # requirement says "Listen to clipboard changes".
        # If I copy from app, it goes to clipboard. Monitor picks it up.
        # It adds to top. That's actually expected behavior: "Only newest at top".
        # So no need to pause.
        pyperclip.copy(text)
        # Visual feedback?
        # Could show a transient message "Copied!"
        pass

    def clear_history(self):
        if messagebox.askyesno("Clear History", "Are you sure? Pinned items will remain."):
            self.storage.clear_history()
            self.refresh_list()
