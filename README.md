# PDF to Audiobook Converter

A Python script that automatically converts PDF files to audiobooks using Kokoro text-to-speech.

## Overview

This tool takes PDF files, extracts their text content, and converts them to high-quality audio files using the Kokoro text-to-speech engine. It's useful for creating audiobooks from digital documents, making content more accessible, or enabling audio consumption of written materials.

## Requirements

- Python 3.6+
- Dependencies (install via `pip install -r requirements.txt`):
  - pdfminer.six
  - kokoro
  - soundfile
  - pydub

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install spaCy English language model (automatically done on first run, but can be pre-installed):
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Create the required directories if they don't exist:
   ```
   ./input/       # Place PDF files here
   ./audiobooks/  # Output audiobooks will be saved here
   ```

2. Place PDF files in the input directory

3. Run the script:
   ```bash
   python create_audiobook.py
   ```

4. Audiobook files (WAV format) will be created in the audiobooks directory with the same name as the original PDF files.

## How It Works

1. **Text Extraction**: Uses `pdfminer.six` to extract text from PDF files
2. **Text Processing**: Splits text into manageable chunks
3. **Audio Generation**: Processes each chunk with Kokoro TTS engine
4. **Audio Combining**: Merges audio segments into a complete audiobook
5. **Cleanup**: Removes temporary files after processing is complete

## Directory Structure

```
├── create_audiobook.py  # Main script
├── input/               # Place PDF files here
├── audio_files/         # Temporary directory for audio segments (auto-cleaned)
└── audiobooks/          # Output directory for final audiobooks
```

## Notes

- The script will process all PDF files in the input directory
- Temporary audio files are automatically cleaned up after processing
- Progress is displayed in the console during processing

## Troubleshooting

If you encounter warnings about text extraction from PDFs that have extraction restrictions, these are generally safe to ignore as the script will proceed with extraction.