import sys
with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

md = f'''# Updated CineScraper Script (With Year Detection)

Here is your updated script! I added the logic to automatically extract the release year (e.g., 2023) from the file name and include it cleanly in your #New_File_Added captions.

`python
{content}
`
'''

with open(r'C:\Users\dhara\.gemini\antigravity\brain\0b0a9d08-bf87-48ca-b672-a1ed73f413e6\updated_script.md', 'w', encoding='utf-8') as f:
    f.write(md)