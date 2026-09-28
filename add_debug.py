import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'(movie = task\["movie_name"\]\s+)(# --- AI SPELLING AUTOCORRECT ---)'
replacement = r'\1print(f"Processing movie: {movie}")\n              \2'

new_code = re.sub(pattern, replacement, code)

pattern2 = r'(corrected = await ask_gemini\(prompt\)\s+)'
replacement2 = r'print(f"Gemini spelling correction finished")\n                      \1'

new_code = re.sub(pattern2, replacement2, new_code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(new_code)