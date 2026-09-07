"""
TTS Generator for Internet Smart Adventure
Calls ElevenLabs API to generate voice audio for all 61 dialogue lines.
Saves result as tts_audio_pack.json — attach that file back in the Claude chat.
"""
import json, base64, time, sys, os

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

API_KEY = "sk_0f9980ca55e4e016e665c493eee7941a58f01de4e7a920ef"
VOICES = {"boy": "EeQEodFZVtBkjtgK3HBc", "girl": "e3FEEanj39p8QCSMe8iV"}
MODEL = "eleven_turbo_v2_5"
URL_TEMPLATE = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

LINES = [
    {"id":"boy_000","who":"boy","text":"I use the internet almost every day — look, my laptop!"},
    {"id":"boy_001","who":"boy","text":"Good question! And is everything we do online always safe?"},
    {"id":"girl_002","who":"girl","text":"Let’s find out — together. Come on, explorer!"},
    {"id":"boy_003","who":"boy","text":"Whoa — the whole internet is waiting for us!"},
    {"id":"girl_004","who":"girl","text":"Yes! But remember our question — is it ALWAYS good? Let’s keep our eyes open."},
    {"id":"boy_005","who":"boy","text":"So my question actually zoomed all the way to a server and back?!"},
    {"id":"girl_006","who":"girl","text":"Exactly. Little packets of data carried it — faster than you can blink."},
    {"id":"boy_007","who":"boy","text":"The internet is basically a super-fast messenger. Cool!"},
    {"id":"boy_008","who":"boy","text":"Whoa! Look at all the things we can do on the internet!"},
    {"id":"girl_009","who":"girl","text":"And we can CREATE and play too — not just watch. Tap every building and try it!"},
    {"id":"boy_010","who":"boy","text":"We can learn and CREATE almost anything here. This is amazing!"},
    {"id":"girl_011","who":"girl","text":"It really is. But… if the internet is this powerful, could some parts be risky too?"},
    {"id":"boy_012","who":"boy","text":"Hmm. Let’s keep exploring and find out."},
    {"id":"girl_013","who":"girl","text":"Here come different internet habits. Some are great… some, not so good."},
    {"id":"boy_014","who":"boy","text":"Easy! Drag each one into GOOD CHOICE or NOT SO GOOD. Let’s sort them!"},
    {"id":"boy_015","who":"boy","text":"That was easier than I thought! Good and not-so-good aren’t so hard to tell apart."},
    {"id":"girl_016","who":"girl","text":"Sometimes though… the SAME thing can be good OR bad. Like gaming — a little is fun, too much isn’t."},
    {"id":"boy_017","who":"boy","text":"Ohh. So it’s about balance. Let’s test that next!"},
    {"id":"girl_018","who":"girl","text":"This is the Internet Balance Scale. Benefits on the left, risks on the right."},
    {"id":"boy_019","who":"boy","text":"So if I add too many risky habits… the scale tips! Let’s try each one."},
    {"id":"boy_020","who":"boy","text":"So the same activity can be good OR bad — it depends how much!"},
    {"id":"girl_021","who":"girl","text":"Exactly. Too much of anything tips the balance. The trick is moderation."},
    {"id":"girl_022","who":"girl","text":"Let’s plan a Grade 6 student’s day. Fill each time slot with an activity."},
    {"id":"boy_023","who":"boy","text":"Too much screen time and our student gets tired. Let’s find a healthy mix!"},
    {"id":"girl_024","who":"girl","text":"Screens are wonderful — with breaks for sleep, play and the people we love."},
    {"id":"girl_025","who":"girl","text":"Some information is personal. If a stranger gets it, it could be used to hurt us."},
    {"id":"boy_026","who":"boy","text":"So we lock the private stuff away, and only share what’s safe. Let’s sort them!"},
    {"id":"boy_027","who":"boy","text":"Locked and safe! I’ll never post my address or password online."},
    {"id":"girl_028","who":"girl","text":"Perfect. Private info is like a house key — keep it to yourself."},
    {"id":"boy_029","who":"boy","text":"WHOA! A message says I won a FREE PHONE! Let me click it!"},
    {"id":"girl_030","who":"girl","text":"Wait! Did you enter any contest?"},
    {"id":"boy_031","who":"boy","text":"No… I didn’t."},
    {"id":"girl_032","who":"girl","text":"Then why would they send YOU a prize? That’s a classic scam. Let’s learn to spot them."},
    {"id":"boy_033","who":"boy","text":"Phew! Just because something appears online doesn’t mean I should click it."},
    {"id":"girl_034","who":"girl","text":"Exactly. Stop, think and check first. Scammers try to make you excited or scared — so slow down."},
    {"id":"girl_035","who":"girl","text":"Someone you don’t know just started chatting with you online. Let’s see what they want."},
    {"id":"boy_036","who":"boy","text":"I’ll choose what to do at each step. Help me pick safely!"},
    {"id":"boy_037","who":"boy","text":"That felt uncomfortable — so I ignored, blocked, and would tell my parents."},
    {"id":"girl_038","who":"girl","text":"That uncomfortable feeling IS the warning. Never share private info, and always tell a trusted adult."},
    {"id":"boy_039","who":"boy","text":"A website says ‘drinking water after fruit is dangerous.’ Is that… true?"},
    {"id":"girl_040","who":"girl","text":"Let’s not just believe it. In the Truth Lab we CHECK. Who said it? Where’s the evidence?"},
    {"id":"boy_041","who":"boy","text":"So I shouldn’t believe something just because it’s online or looks official."},
    {"id":"girl_042","who":"girl","text":"Right! Who said it? Is there evidence? Can I check a trusted source? Think before you believe."},
    {"id":"boy_043","who":"boy","text":"We’ve come so far! Let’s take one big journey through the whole internet world."},
    {"id":"girl_044","who":"girl","text":"From home, to school, to the world — and into the internet itself. Come on!"},
    {"id":"girl_045","who":"girl","text":"The internet gives us SO many possibilities."},
    {"id":"boy_046","who":"boy","text":"But we have to decide how we use them — the good stuff, safely."},
    {"id":"girl_047","who":"girl","text":"Exactly. Now let’s write down OUR rules to remember it all."},
    {"id":"girl_048","who":"girl","text":"Time to build our rulebook! For each rule, choose the wise ending."},
    {"id":"boy_049","who":"boy","text":"And every rule we finish becomes a card on the board. Let’s go!"},
    {"id":"boy_050","who":"boy","text":"Our very own rulebook! Seven rules to use the internet smartly."},
    {"id":"girl_051","who":"girl","text":"And because we built it ourselves, we’ll actually remember it. Ready for the final challenge?"},
    {"id":"boy_052","who":"boy","text":"An arcade! But these games teach real internet skills. First up — building a strong password!"},
    {"id":"girl_053","who":"girl","text":"Let’s forge one so strong no one can guess it. Then we’ll practise being kind online."},
    {"id":"boy_054","who":"boy","text":"Strong password AND kind words. I feel like a real internet pro now!"},
    {"id":"girl_055","who":"girl","text":"That’s what being Internet Smart means — safe, thoughtful and kind. One challenge left!"},
    {"id":"girl_056","who":"girl","text":"This is it — the Final Challenge! Ten real internet moments, back to back."},
    {"id":"boy_057","who":"boy","text":"React quickly and wisely. Let’s show what we learned!"},
    {"id":"girl_058","who":"girl","text":"Let’s see your Internet Smart Explorer result and your very own rules!"},
    {"id":"boy_059","who":"boy","text":"A balanced day feels great — energy for everything!"},
    {"id":"boy_060","who":"boy","text":"Too much screen time really does drain your energy. Lesson learned!"},
]

def main():
    print("=" * 60)
    print("  TTS Audio Generator — Internet Smart Adventure")
    print("  ElevenLabs Turbo v2.5 · 61 lines · ~4,200 chars")
    print("=" * 60)
    print()

    results = {}
    total_bytes = 0
    errors = 0

    for i, ln in enumerate(LINES):
        voice_id = VOICES[ln["who"]]
        label = f"[{i+1}/{len(LINES)}] {ln['who'].upper()}: {ln['text'][:50]}..."
        print(f"  {label}", end=" ", flush=True)

        try:
            resp = requests.post(
                URL_TEMPLATE.format(voice_id=voice_id),
                headers={
                    "xi-api-key": API_KEY,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                },
                json={
                    "text": ln["text"],
                    "model_id": MODEL,
                    "output_format": "mp3_22050_32",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75,
                        "style": 0.0,
                        "use_speaker_boost": False,
                    },
                },
                timeout=30,
            )

            if resp.status_code == 200:
                audio_b64 = base64.b64encode(resp.content).decode("ascii")
                results[ln["id"]] = {
                    "who": ln["who"],
                    "text": ln["text"],
                    "audio": audio_b64,
                    "size": len(resp.content),
                }
                total_bytes += len(resp.content)
                print(f"OK ({len(resp.content)/1024:.1f} KB)")
            else:
                errors += 1
                print(f"FAILED (HTTP {resp.status_code}: {resp.text[:100]})")

        except Exception as e:
            errors += 1
            print(f"ERROR: {e}")

        # Small delay between requests
        if i < len(LINES) - 1:
            time.sleep(0.3)

    print()
    print("=" * 60)
    print(f"  Done! {len(results)}/{len(LINES)} generated ({total_bytes/1024:.0f} KB)")
    if errors:
        print(f"  {errors} errors occurred.")
    print("=" * 60)

    # Save the result
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tts_audio_pack.json")
    with open(out_path, "w") as f:
        json.dump(results, f)
    print(f"\n  Saved to: {out_path}")
    print(f"  File size: {os.path.getsize(out_path)/1024:.0f} KB")
    print(f"\n  >>> Now attach tts_audio_pack.json in the Claude chat <<<")
    print()
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
