import re, json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all JS arrays that contain dialogue objects
# Look for {who:'boy', ...} or {who:"girl", ...}
# We can find all {who:...} blocks accurately
obj_pattern = re.compile(r'\{[^{}]*?who\s*:\s*[\'"](boy|girl|narr)[\'"][^{}]*?\}', re.DOTALL)

items = []
for m in obj_pattern.finditer(html):
    raw = m.group(0)
    
    who_m = re.search(r'who\s*:\s*[\'"](\w+)[\'"]', raw)
    audio_m = re.search(r'audio\s*:\s*[\'"]([^\'"]+)[\'"]', raw)
    # text can be enclosed in double quotes, single quotes, or backticks
    text_m = re.search(r'text\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"|text\s*:\s*\'([^\'\\]*(?:\\.[^\'\\]*)*)\'|text\s*:\s*`([^`\\]*(?:\\.[^`\\]*)*)`', raw)
    
    who = who_m.group(1) if who_m else 'narr'
    audio = audio_m.group(1) if audio_m else ''
    text = ''
    if text_m:
        if text_m.group(1) is not None:
            text = text_m.group(1)
        elif text_m.group(2) is not None:
            text = text_m.group(2)
        elif text_m.group(3) is not None:
            text = text_m.group(3)
            
    # Unescape
    text = text.replace('\\"', '"').replace("\\'", "'").replace('\n', ' ').strip()
    
    if text:
        items.append({
            'who': who,
            'audio': audio,
            'text': text
        })

print(f"Total dialogue objects found: {len(items)}")
for i, it in enumerate(items):
    print(f"{i+1:02d}. [{it['audio']}] ({it['who']}): {it['text']}")

with open('dialogues_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print("Saved clean manifest to dialogues_manifest.json")
