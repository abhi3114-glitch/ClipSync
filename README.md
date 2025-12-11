# ClipSync - Clipboard History & Quick Paste Tool

ClipSync is a desktop utility designed to enhance your clipboard workflow by storing the last 20 copied items. It features a dark-themed interface, allowing users to easily access previously copied text, pin important items, and clear their history.

## Features

- **Clipboard Monitoring**: Automatically detects and stores text copied to the clipboard in real-time.
- **History Management**: Keeps track of the last 20 items copied.
- **Persistence**: History is saved locally and restored upon application restart.
- **Pinning**: Important items can be pinned to prevent them from being removed when the history limit is reached.
- **Quick Actions**: Features one-click copy and history clearing.
- **Privacy Focused**: All data is stored locally on your machine. No internet connection is required.

## Tech Stack

- **Python 3**: Core programming language.
- **Tkinter**: Standard GUI library for Python.
- **Pyperclip**: Cross-platform clipboard module.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abhi3114-glitch/ClipSync.git
   cd ClipSync
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. The application window will open. Any text you copy from other applications will automatically appear in the list.
3. Click on the star icon to pin an item.
4. Click on the "Copy" button or the item text to copy it back to your clipboard.
5. Use the "Clear All" button to remove all unpinned items from the history.

## Project Structure

- `main.py`: Entry point of the application.
- `ui.py`: Handles the graphical user interface using Tkinter.
- `clipboard_monitor.py`: Background thread for monitoring clipboard changes.
- `storage.py`: Manages data persistence and history logic.
- `history.json`: Local storage file for clipboard history (not included in version control).

## License

This project is open source and available under the MIT License.
