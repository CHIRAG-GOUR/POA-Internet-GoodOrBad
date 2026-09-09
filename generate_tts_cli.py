import sys, os, json, argparse, urllib.request, base64

sys.stdout.reconfigure(encoding='utf-8')

VOICES = {
    'boy': 'EeQEodFZVtBkjtgK3HBc',   # Kid Voice Boy (POA default)
    'girl': 'e3FEEanj39p8QCSMe8iV'   # Bella (POA default)
}

MODEL = "eleven_turbo_v2_5"
FORMAT = "mp3_22050_32"

def main():
    parser = argparse.ArgumentParser(description="ElevenLabs Voice Generator for POA Internet - Good or Bad")
    parser.add_argument("--api-key", help="ElevenLabs API Key")
    parser.add_argument("--boy-voice", default=VOICES['boy'], help="ElevenLabs Voice ID for Boy")
    parser.add_argument("--girl-voice", default=VOICES['girl'], help="ElevenLabs Voice ID for Girl (Bella)")
    parser.add_argument("--manifest", default="dialogues_manifest.json", help="Path to dialogues manifest")
    parser.add_argument("--out-dir", default="audio", help="Output audio directory")
    parser.add_argument("--pack-file", default="tts_audio_pack.json", help="Output JSON audio pack")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        api_key = input("Please enter your ElevenLabs API Key: ").strip()

    if not api_key:
        print("Error: ElevenLabs API Key is required.")
        sys.exit(1)

    os.makedirs(args.out_dir, exist_ok=True)

    with open(args.manifest, "r", encoding="utf-8") as f:
        lines = json.load(f)

    print(f"Loaded {len(lines)} dialogue lines.")
    print(f"Boy Voice ID: {args.boy_voice}")
    print(f"Girl Voice ID (Bella): {args.girl_voice}")
    print(f"Output directory: {args.out_dir}\n")

    results = {}
    total = len(lines)

    for i, item in enumerate(lines):
        who = item['who']
        text = item['text']
        audio_rel = item['audio']
        
        # Audio file path
        fname = os.path.basename(audio_rel)
        out_path = os.path.join(args.out_dir, fname)
        line_id = os.path.splitext(fname)[0]

        voice_id = args.boy_voice if who == 'boy' else args.girl_voice

        print(f"[{i+1}/{total}] Generating {fname} ({who}): \"{text[:45]}...\"")

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format={FORMAT}"
        req = urllib.request.Request(
            url,
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json"
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
                audio_bytes = resp.read()
                
                with open(out_path, "wb") as af:
                    af.write(audio_bytes)
                
                b64 = base64.b64encode(audio_bytes).decode('utf-8')
                results[line_id] = {
                    "who": who,
                    "audio": audio_rel,
                    "text": text,
                    "base64": b64,
                    "size": len(audio_bytes)
                }
                print(f"    -> Saved {len(audio_bytes)/1024:.1f} KB to {out_path}")
        except Exception as e:
            print(f"    -> ERROR generating {fname}: {e}")
            sys.exit(1)

    with open(args.pack_file, "w", encoding="utf-8") as pf:
        json.dump(results, pf, indent=2)

    print(f"\nAll {total} audio clips generated successfully!")
    print(f"Saved to {args.out_dir}/ and {args.pack_file}")

if __name__ == '__main__':
    main()
