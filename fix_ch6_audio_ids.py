import os

for fname in ['index.html', 'internet-smart-adventure.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # In Chapter 6:
    # Look for boy_017 near rubEyes or screen
    target1 = "{who:'boy', expr:'worried', pose:'rubEyes', audio:'audio/boy_017.mp3', text:\"Sometimes after staring at a screen for hours, my eyes sting, get red, and I get a headache.\"}"
    replace1 = "{who:'boy', expr:'worried', pose:'rubEyes', audio:'audio/boy_022.mp3', text:\"Sometimes after staring at a screen for hours, my eyes sting, get red, and I get a headache.\"}"

    target2 = "{who:'girl', expr:'determined', pose:'point', audio:'audio/girl_018.mp3', text:\"Let us test our 3D Vision Simulator to see exactly what happens to eyes during long screen time and how to fix it!\"}"
    replace2 = "{who:'girl', expr:'determined', pose:'point', audio:'audio/girl_023.mp3', text:\"Let us test our 3D Vision Simulator to see exactly what happens to eyes during long screen time and how to fix it!\"}"

    if target1 in content:
        content = content.replace(target1, replace1)
        print(f"Replaced target1 in {fname}")
    else:
        print(f"target1 not found in {fname}, trying regex...")
        import re
        content = re.sub(
            r"audio\s*:\s*['\"]audio/boy_017\.mp3['\"](\s*,\s*text\s*:\s*[\"']Sometimes after staring)",
            r"audio:'audio/boy_022.mp3'\1",
            content
        )

    if target2 in content:
        content = content.replace(target2, replace2)
        print(f"Replaced target2 in {fname}")
    else:
        print(f"target2 not found in {fname}, trying regex...")
        import re
        content = re.sub(
            r"audio\s*:\s*['\"]audio/girl_018\.mp3['\"](\s*,\s*text\s*:\s*[\"']Let us test our 3D Vision)",
            r"audio:'audio/girl_023.mp3'\1",
            content
        )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully updated {fname} with unique audio IDs!")
