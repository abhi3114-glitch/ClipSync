import json
import os
import time

HISTORY_FILE = 'history.json'
MAX_ITEMS = 20

class StorageManager:
    def __init__(self, filename=HISTORY_FILE):
        self.filename = filename
        self.items = []
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.items = data if isinstance(data, list) else []
            except (json.JSONDecodeError, IOError):
                self.items = []
        else:
            self.items = []

    def save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.items, f, indent=2)
        except IOError as e:
            print(f"Error saving history: {e}")

    def add_item(self, text):
        """Adds an item to history. Deduplicates if exists. Handles pinning (todo)."""
        if not text or not text.strip():
            return

        # Check if item exists and move to top if so
        existing_index = -1
        for i, item in enumerate(self.items):
            if item['text'] == text:
                existing_index = i
                break

        if existing_index != -1:
            # Move to top (which is index 0 for display, or end of list? Let's say index 0 is newest)
            # Actually, usually appending to list means end is newest. Let's stick to: Index 0 is newest.
            item = self.items.pop(existing_index)
            item['timestamp'] = time.time()
            self.items.insert(0, item)
        else:
            new_item = {
                'text': text,
                'timestamp': time.time(),
                'pinned': False
            }
            self.items.insert(0, new_item)

        self._enforce_limit()
        self.save()

    def _enforce_limit(self):
        """Keeps list size at MAX_ITEMS, preserving pinned items if possible."""
        if len(self.items) <= MAX_ITEMS:
            return

        # Separate pinned and unpinned
        pinned = [item for item in self.items if item.get('pinned')]
        unpinned = [item for item in self.items if not item.get('pinned')]

        # If we have too many items, strictly trim unpinned first
        # Strategy: Keep all pinned. Fill rest of MAX_ITEMS with newest unpinned.
        
        needed_slots = MAX_ITEMS - len(pinned)
        if needed_slots < 0:
            # If we have more pinned items than MAX_ITEMS, we technically exceed limit.
            # Requirement says "Store last 20 items". pinned usually implies keeping.
            # We will generate a list of pinned + latest unpinned.
            # If pinned > 20, we keep them all but can't add new unpinned? 
            # Or we just keep top 20 regardless? "Star/pin important items" implies they shouldn't drop off.
            # Let's keep all pinned, and as many unpinned as fit.
            self.items = pinned # Can't fit any unpinned
        else:
            while len(self.items) > MAX_ITEMS:
                # Find oldest unpinned
                idx_to_remove = -1
                for i in range(len(self.items) - 1, -1, -1):
                    if not self.items[i].get('pinned'):
                        idx_to_remove = i
                        break
                
                if idx_to_remove != -1:
                    self.items.pop(idx_to_remove)
                else:
                    # All remaining are pinned. Stop trimming.
                    break

    def toggle_pin(self, index):
        if 0 <= index < len(self.items):
            self.items[index]['pinned'] = not self.items[index]['pinned']
            self.save()

    def clear_history(self):
        # Keep pinned items? Usually "Clear History" clears everything except pinned.
        self.items = [item for item in self.items if item.get('pinned')]
        self.save()

    def get_items(self):
        return self.items
