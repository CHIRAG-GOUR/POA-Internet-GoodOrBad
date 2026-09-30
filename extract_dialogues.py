import sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Pattern matching dialogue objects
# e.g. {who:'boy', expr:'excited', pose:'wave', audio:'audio/boy_000.mp3', text:"..."}
pattern = re.compile(r'\{[^{}]*who\s*:\s*[\'"](\w+)[\'"][^{}]*audio\s*:\s*[\'"]([^\'"]+)[\'"][^{}]*text\s*:\s*[\'"]([^\'"]+)[\'"][^{}]*\}', re.DOTALL)

lines = []
for match in pattern.finditer(html):
    who = match.group(1)
    audio = match.group(2)
    text = match.group(3)
    lines.append({
        'who': who,
        'audio': audio,
        'text': text
    })

# Also handle cases where text is before audio
pattern2 = re.compile(r'\{[^{}]*who\s*:\s*[\'"](\w+)[\'"][^{}]*text\s*:\s*[\'"]([^\'"]+)[\'"][^{}]*audio\s*:\s*[\'"]([^\'"]+)[\'"][^{}]*\}', re.DOTALL)
for match in pattern2.finditer(html):
    who = match.group(1)
    text = match.group(2)
    audio = match.group(3)
    if not any(l['audio'] == audio for l in lines):
        lines.append({
            'who': who,
            'audio': audio,
            'text': text
        })

print(f"Total dialogue lines found in index.html: {len(lines)}")
for idx, l in enumerate(lines):
    print(f"{idx+1:02d}. [{l['audio']}] ({l['who']}): {l['text']}")

# Save extracted lines as json
with open('extracted_dialogues.json', 'w', encoding='utf-8') as out:
    json.dump(lines, out, indent=2, ensure_ascii=False)
print("Saved to extracted_dialogues.json")
