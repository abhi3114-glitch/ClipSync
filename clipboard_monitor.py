import pyperclip
import time
import threading

class ClipboardMonitor:
    def __init__(self, callback, interval=0.1):
        self.callback = callback
        self.interval = interval
        self.running = False
        self.last_text = ""
        self.thread = None

    def start(self):
        if self.running:
            return
        
        # Initialize last_text with current clipboard content to avoid immediate duplicate trigger
        try:
            self.last_text = pyperclip.paste()
        except Exception:
            self.last_text = ""

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _monitor_loop(self):
        while self.running:
            try:
                current_text = pyperclip.paste()
                if current_text != self.last_text:
                    self.last_text = current_text
                    if current_text.strip(): # Ignore empty or whitespace only? Maybe user wants whitespace.
                        # Let's keep whitespace if it's what they copied.
                        # But empty string usually means nothing.
                        if current_text:
                            self.callback(current_text)
            except Exception as e:
                print(f"Clipboard Error: {e}")
            
            time.sleep(self.interval)
