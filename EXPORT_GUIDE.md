# How to Use Your Pitch Deck

## Files Included

- **pitch-deck.md** - Source markdown file (editable)
- **pitch-deck.html** - HTML presentation (ready to present)

## Option 1: Convert HTML to PDF (Recommended)

### Method A: Using Your Browser (Easiest)
1. Open `pitch-deck.html` in any web browser (Chrome, Firefox, Edge, Safari)
2. Press **Ctrl+P** (Windows/Linux) or **Cmd+P** (Mac)
3. Select "Save as PDF" as the destination
4. Choose these settings:
   - Layout: **Landscape**
   - Paper size: **Letter** or **A4**
   - Margins: **None** or **Minimum**
   - Background graphics: **Enabled**
5. Click "Save"

### Method B: Using Chrome Headless (Command Line)
```bash
google-chrome --headless --disable-gpu --print-to-pdf=pitch-deck.pdf pitch-deck.html
```

## Option 2: Import to Google Slides

### From PDF:
1. Convert HTML to PDF (see Option 1 above)
2. Go to [Google Slides](https://slides.google.com)
3. Click **File → Open**
4. Click **Upload** tab
5. Upload your PDF file
6. Google Slides will import each page as a slide

### From PowerPoint (Alternative):
You can also use online converters:
1. Use [CloudConvert](https://cloudconvert.com/html-to-pptx) to convert HTML to PPTX
2. Upload the PPTX to Google Drive
3. Open with Google Slides

## Option 3: Present Directly from HTML

The HTML file is a fully functional presentation:

1. Open `pitch-deck.html` in your browser
2. Press **F11** for fullscreen mode
3. Use arrow keys to navigate:
   - **→** or **Space**: Next slide
   - **←** or **Backspace**: Previous slide
   - **Esc**: Exit fullscreen

## Editing the Deck

1. Edit `pitch-deck.md` with any text editor
2. Regenerate HTML:
   ```bash
   marp pitch-deck.md --html -o pitch-deck.html
   ```

## Need a Different Format?

- **PowerPoint (.pptx)**: Use [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) export feature
- **Images (PNG/JPG)**: Use Marp CLI: `marp pitch-deck.md --images png`
- **Keynote**: Export to PDF first, then import to Keynote

## Troubleshooting

**Colors look wrong in PDF?**
- Make sure "Background graphics" is enabled in print settings

**Slides are cut off?**
- Use "None" margins and "Landscape" orientation

**Text is too small?**
- The deck is optimized for 1920x1080 resolution
- When printing, use "Fit to page" option
