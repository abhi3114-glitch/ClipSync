import unittest
import os
import json
import time
from storage import StorageManager
# We can't easily test monitor without user interaction or mocking pyperclip.
# We will test StorageManager logic.

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_history.json'
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.storage = StorageManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_item(self):
        self.storage.add_item("Hello")
        self.assertEqual(len(self.storage.get_items()), 1)
        self.assertEqual(self.storage.get_items()[0]['text'], "Hello")

    def test_deduplication(self):
        self.storage.add_item("Hello")
        time.sleep(0.1)
        self.storage.add_item("World")
        time.sleep(0.1)
        self.storage.add_item("Hello")
        
        items = self.storage.get_items()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['text'], "Hello") # "Hello" should be moved to top

    def test_limit(self):
        for i in range(25):
            self.storage.add_item(f"Item {i}")
        
        items = self.storage.get_items()
        self.assertEqual(len(items), 20)
        self.assertEqual(items[0]['text'], "Item 24")

    def test_pinning_prevents_deletion(self):
        # Add item and pin it
        self.storage.add_item("Pinned Item")
        self.storage.toggle_pin(0) # Pin top item
        
        # Add 30 more items
        for i in range(30):
            self.storage.add_item(f"New {i}")
            
        items = self.storage.get_items()
        # "Pinned Item" should still be there
        found = any(item['text'] == "Pinned Item" for item in items)
        self.assertTrue(found)
        self.assertEqual(len(items), 20)

if __name__ == '__main__':
    unittest.main()
