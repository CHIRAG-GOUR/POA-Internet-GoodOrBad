import os, sys, json, time, urllib.request, base64

sys.stdout.reconfigure(encoding='utf-8')

# Read API Key from .env
api_key = None
with open('.env', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('ELEVENLABS_API_KEY='):
            api_key = line.split('=', 1)[1].strip()

if not api_key:
    print("Error: Could not read ELEVENLABS_API_KEY from .env")
    sys.exit(1)

# Voices
VOICE_BOY = "ErXwobaYiN019PkySvjV"   # Antoni (Natural, friendly, expressive young male / kid voice)
VOICE_GIRL = "EXAVITQu4vr4xnSDxMaL"  # Bella (Standard Premade - Meera)
MODEL = "eleven_turbo_v2_5"
FORMAT = "mp3_22050_32"

AUDIO_DIR = "audio"
PACK_FILE = "tts_audio_pack.json"
os.makedirs(AUDIO_DIR, exist_ok=True)

with open("dialogues_manifest.json", "r", encoding="utf-8") as f:
    lines = json.load(f)

total = len(lines)
print(f"============================================================")
print(f"🎙️ STARTING ELEVENLABS BATCH TTS GENERATION ({total} LINES)")
print(f"  👦 Boy (Aarav): Antoni ({VOICE_BOY})")
print(f"  👧 Girl (Meera): Bella ({VOICE_GIRL})")
print(f"  ⚡ Model: {MODEL} | Format: {FORMAT}")
print(f"============================================================\n")

results = {}
total_bytes = 0

for idx, item in enumerate(lines):
    who = item['who']
    text = item['text']
    audio_rel = item['audio']
    fname = os.path.basename(audio_rel)
    out_path = os.path.join(AUDIO_DIR, fname)
    line_id = os.path.splitext(fname)[0]

    voice_id = VOICE_BOY if who == 'boy' else VOICE_GIRL
    role_label = "👦 AARAV" if who == 'boy' else "👧 MEERA"

    print(f"[{idx+1:02d}/{total:02d}] Generating {fname} ({role_label})...")
    print(f"       Text: \"{text}\"")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format={FORMAT}"
    req = urllib.request.Request(
        url,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        },
        data=json.dumps({
            "text": text,
            "model_id": MODEL,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }).encode('utf-8')
    )

    try:
        with urllib.request.urlopen(req) as resp:
            audio_data = resp.read()
            total_bytes += len(audio_data)

            # Write individual MP3 file
            with open(out_path, "wb") as af:
                af.write(audio_data)

            # Convert to base64 for bundle
            b64 = base64.b64encode(audio_data).decode('utf-8')
            results[line_id] = {
                "who": who,
                "audio": audio_rel,
                "text": text,
                "base64": b64,
                "size": len(audio_data)
            }
            print(f"       ✅ Saved {len(audio_data)/1024:.1f} KB -> {out_path}")
            
            # Short rate limit pause
            time.sleep(0.3)
    except Exception as e:
        print(f"       ❌ FAILED generating {fname}: {e}")
        # Continue to next if possible or print details
        time.sleep(1.0)

# Save bundled json
with open(PACK_FILE, "w", encoding="utf-8") as pf:
    json.dump(results, pf, indent=2)

print(f"\n============================================================")
print(f"🎉 GENERATION COMPLETE!")
print(f"  Total files generated: {len(results)}/{total}")
print(f"  Total audio size: {total_bytes/1024:.1f} KB")
print(f"  Pack bundle updated: {PACK_FILE}")
print(f"============================================================")
