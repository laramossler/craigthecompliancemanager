# Pitch Deck Viewing Guide

## How to View the Pitch Deck

The pitch deck is created using **Marp** (Markdown Presentation Ecosystem), which converts markdown to beautiful slides.

### Option 1: Using Marp CLI (Recommended)

1. Install Marp CLI:
   ```bash
   npm install -g @marp-team/marp-cli
   ```

2. View as HTML:
   ```bash
   marp pitch-deck.md -o pitch-deck.html
   ```

3. View as PDF:
   ```bash
   marp pitch-deck.md -o pitch-deck.pdf
   ```

4. View as PowerPoint:
   ```bash
   marp pitch-deck.md -o pitch-deck.pptx
   ```

5. Present directly with live server:
   ```bash
   marp -s pitch-deck.md
   ```

### Option 2: Using Marp for VS Code

1. Install the [Marp for VS Code extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
2. Open `pitch-deck.md` in VS Code
3. Click the preview button or press `Ctrl+K V` (Windows/Linux) or `Cmd+K V` (Mac)
4. Use the built-in presentation mode

### Option 3: Online Editors

- Upload to [Marp Web](https://web.marp.app/) for instant preview
- Use [GitPitch](https://gitpitch.com/) with your repository

## Deck Structure

The pitch deck includes:

1. **Cover Slide** - Title and tagline
2. **The Problem** - Pain points in compliance
3. **Meet Craig** - Solution overview
4. **How It Works** - Process flow
5. **Key Features** (2 slides) - Product capabilities
6. **Market Opportunity** - TAM/SAM/SOM analysis
7. **Competitive Advantage** - Comparison table
8. **Business Model** - Pricing tiers
9. **Traction & Roadmap** - Milestones and goals
10. **The Team** - Founders and advisors
11. **The Ask** - Fundraising details
12. **Closing** - Contact information

## Customization Tips

- Update team details in slide 10
- Adjust pricing based on market research
- Add real traction numbers when available
- Include customer logos when you have them
- Update contact information in the final slide

## Presentation Mode

- Use arrow keys to navigate
- Press `F` for fullscreen
- Press `P` for presenter notes (if added)
- Press `Esc` to exit fullscreen
