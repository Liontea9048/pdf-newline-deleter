# Line Joiner

A simple GUI tool to automatically or manually join multiline text into a single line.  
Designed especially for cleaning up line breaks from PDFs and other text sources.

## Features

- 🔁 **Auto Mode**: Monitors clipboard and joins lines automatically
- ✍️ **Manual Mode**: Paste, preview, and copy manually with full control
- 🌙 **Dark/Light Mode** toggle
- 🔤 **Font Selector** from system fonts
- 🌀 Spinner indicator while processing in Auto Mode
- 🧼 Strips whitespace and blank lines automatically

## How to Use

### ▶ Auto Mode (default)
1. Copy any multiline text (e.g. from a PDF)
2. The app automatically cleans and replaces clipboard content
3. Paste it anywhere!

### ✍ Manual Mode
1. Click `AUTO MODE 🔄` button to switch to `Manual Mode`
2. Copy any multiline text (e.g. from a PDF)
3. Paste into the upper box (or skip this step and go to the 4 directly)
4. Press `📋 Paste & Copy` to clean it and copy to clipboard
5. Cleaned result appears in the lower box

### 🌗 Theme
- Use the "Dark Mode 🌙" or "Light Mode ☀️" button to switch themes

### 🔤 Font
- Select your preferred system-installed font via dropdown

## Installation

### 1. Requirements

- Python 3.7+
- `tkinter` (usually included)
- `pyinstaller` for packaging (optional)

### 2. Running

```bash
python line_joiner_gui.py
