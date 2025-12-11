import tkinter as tk
from storage import StorageManager
from clipboard_monitor import ClipboardMonitor
from ui import ClipSyncApp
import sys

def main():
    # Initialize Logic
    storage = StorageManager()
    
    # TK Root
    root = tk.Tk()
    
    # Initialize UI first to get reference for callbacks
    # But UI needs monitor? Or just monitor needs callback to UI?
    # Monitor needs callback. UI needs to handle update.
    
    # Let's create UI with placeholder monitor, then start monitor with UI callback
    # Actually, we can pass monitor=None first if we want, or create Monitor first with dummy lambda then set it.
    
    # Better:
    # 1. Create Storage
    # 2. Create UI (without monitor ref, or set later)
    # 3. Create Monitor with UI.callback
    # 4. Inject monitor into UI
    
    # We need to bridge the callback.
    # UI has `on_clipboard_change`.
    
    # We need a wrapper because UI isn't created yet when we define callback?
    # No, we can create UI inside `main`, then pass its method.
    
    monitor_ref = [None] # Mutable container
    
    app = ClipSyncApp(root, storage, None) # Pass None for monitor initially
    
    def on_change(text):
        app.on_clipboard_change(text)
        
    monitor = ClipboardMonitor(on_change)
    app.monitor = monitor # Inject back if needed (maybe for pause/stop)
    
    monitor.start()
    
    try:
        root.mainloop()
    finally:
        monitor.stop()

if __name__ == "__main__":
    main()
