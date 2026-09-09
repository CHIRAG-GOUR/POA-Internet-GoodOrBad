import sys
import re

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    with open('index.html', 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Head part (Everything up to CHAPTER 01)
    props_end_idx = text.find('/* =====================================================================\n   CHAPTER 01:')
    if props_end_idx == -1:
        props_end_idx = text.find('/* =====================================================================\r\n   CHAPTER 01:')
    head_part = text[:props_end_idx]

    # Extract Chapters 1 to 6
    ch1_idx = text.find('/* =====================================================================\n   CHAPTER 01:')
    if ch1_idx == -1: ch1_idx = text.find('/* =====================================================================\r\n   CHAPTER 01:')

    ch7_idx = text.find('/* =====================================================================\n   CHAPTER 07:')
    if ch7_idx == -1: ch7_idx = text.find('/* =====================================================================\r\n   CHAPTER 07:')
    if ch7_idx == -1: ch7_idx = text.find("id:'ch7'")
    if ch7_idx == -1: ch7_idx = text.find('id:"ch7"')

    ch1_to_6 = text[ch1_idx:text.rfind('registerChapter({', 0, ch7_idx)].strip()
    if not ch1_to_6:
        ch1_to_6 = text[ch1_idx:ch7_idx].strip()

    # Helper function to extract a chapter by id
    def extract_chapter_block(ch_id):
        for needle in [f"id:'{ch_id}'", f'id:"{ch_id}"', f"id: '{ch_id}'", f'id: "{ch_id}"']:
            pos = text.find(needle)
            if pos != -1:
                start = text.rfind('registerChapter({', 0, pos)
                start_comment = text.rfind('/* =====================================================================', 0, start)
                if start_comment != -1 and start_comment > start - 200:
                    start = start_comment
                # find end
                end = text.find('\nregisterChapter({', pos)
                if end == -1:
                    end = text.find('\n/* =============== SCENE BOOT', pos)
                if end == -1:
                    end = text.find('\n/* =====================================================================\n   CELEBRATION', pos)
                return text[start:end].strip()
        return None

    ch9_code = extract_chapter_block('ch9')
    ch11_code = extract_chapter_block('ch11')
    ch12_code = extract_chapter_block('ch12')
    ch13_code = extract_chapter_block('ch13')

    # Fireworks helper
    fw_idx = text.find('/* =====================================================================\n   CELEBRATION FIREWORKS')
    if fw_idx == -1: fw_idx = text.find('/* =====================================================================\r\n   CELEBRATION FIREWORKS')
    fw_end = text.find('/* =====================================================================\n   CHAPTER 13', fw_idx)
    if fw_end == -1: fw_end = text.find('/* =====================================================================\r\n   CHAPTER 13', fw_idx)
    if fw_idx != -1 and fw_end != -1:
        fireworks_helper = text[fw_idx:fw_end].strip()
    else:
        fireworks_helper = '''/* =====================================================================
   CELEBRATION FIREWORKS ENGINE (5 CONTINUOUS ROCKETS)
   ===================================================================== */
function launchCelebrationFireworks(root, count, onComplete){
  const total = count || 5;
  let launched = 0;
  const colors = [0xff4757, 0x2ed573, 0x1e90ff, 0xffa502, 0x9b59b6];
  
  function launchNextRocket(){
    if(launched >= total){
      if(onComplete) onComplete();
      return;
    }
    const color = colors[launched % colors.length];
    const startX = -2.8 + (launched * 1.4);
    const targetY = 5.2 + Math.random() * 1.8;
    const targetZ = -2 - Math.random() * 2;
    
    const rocket = new T.Mesh(new T.CylinderGeometry(0.06, 0.08, 0.35, 8), mat(color, {emissive: color, emissiveIntensity: 1.2}));
    rocket.position.set(startX, 0.2, targetZ);
    root.add(rocket);
    
    try { if(SFX.whoosh) SFX.whoosh(); } catch(e){}
    
    let progress = 0;
    const rocketInterval = setInterval(()=>{
      progress += 0.05;
      rocket.position.y += (targetY - 0.2) * 0.05;
      rocket.rotation.z += 0.1;
      
      if(progress >= 1.0){
        clearInterval(rocketInterval);
        root.remove(rocket);
        
        try { SFX.pop(); SFX.badge(); } catch(e){}
        const sparkGroup = new T.Group();
        const sparks = [];
        for(let s = 0; s < 36; s++){
          const sm = new T.Mesh(new T.SphereGeometry(0.07, 6, 6), mat(color, {emissive: color, emissiveIntensity: 1.4}));
          sm.position.copy(rocket.position);
          const angle = Math.random() * Math.PI * 2;
          const phi = Math.random() * Math.PI;
          const speed = 0.07 + Math.random() * 0.11;
          sparks.push({
            mesh: sm,
            vx: Math.sin(phi) * Math.cos(angle) * speed,
            vy: Math.cos(phi) * speed + 0.02,
            vz: Math.sin(phi) * Math.sin(angle) * speed
          });
          sparkGroup.add(sm);
        }
        root.add(sparkGroup);
        
        let sparkLife = 1.0;
        const sparkInterval = setInterval(()=>{
          sparkLife -= 0.04;
          sparks.forEach(sp => {
            sp.mesh.position.x += sp.vx;
            sp.mesh.position.y += sp.vy;
            sp.mesh.position.z += sp.vz;
            sp.vy -= 0.003;
            sp.mesh.scale.setScalar(Math.max(0.01, sparkLife));
          });
          if(sparkLife <= 0){
            clearInterval(sparkInterval);
            root.remove(sparkGroup);
          }
        }, 30);
        
        launched++;
        setTimeout(launchNextRocket, 450);
      }
    }, 25);
  }
  
  launchNextRocket();
}'''

    # Boot part
    boot_idx = text.rfind('/* =============== SCENE BOOT & LAUNCH =============== */')
    boot_part = text[boot_idx:]

    # 2. UPGRADED Chapter 7
    ch7_code = '''/* =====================================================================
   CHAPTER 07: Privacy Locker (3D Sorting Simulation & Review Engine)
   ===================================================================== */
registerChapter({
  id: 'ch7',
  title: 'Privacy Locker',
  logtag: 'PRIVACY',
  bg1: '#1e1b4b',
  bg2: '#312e81',
  endTitle: 'Chapter 7 Complete! Master Privacy Guardian 🔒',
  learned: [
    'Private Data (Passwords, Address, Phone Number, School): Keep locked in your Cyber Vault.',
    'Safe to Share (Favorite Colors, Cartoon Avatars, Gaming Tags): Safe for public profiles.',
    'Never share passwords with anyone except parents — not even best friends!'
  ],
  build(root, api){
    addLights(root, 'warm');
    ground(root, 0x1e293b, 45);

    // 1. 3D High-Tech Privacy Vault (Left Side)
    const vaultGroup = new T.Group();
    vaultGroup.position.set(-3.4, 0, -2.2);
    
    const safeBody = box(3.0, 3.2, 2.2, 0x0f172a); safeBody.position.y = 1.6; safeBody.castShadow = true; vaultGroup.add(safeBody);
    const safeRim = box(3.1, 3.3, 0.1, 0x3b82f6); safeRim.position.set(0, 1.6, 1.1); vaultGroup.add(safeRim);
    const safeDoor = box(2.6, 2.8, 0.14, 0x1e293b); safeDoor.position.set(0, 1.6, 1.16); vaultGroup.add(safeDoor);
    
    const wheel = cyl(0.38, 0.38, 0.12, 0xf59e0b, 20); wheel.rotation.x = Math.PI/2; wheel.position.set(0, 1.6, 1.25); vaultGroup.add(wheel);
    const lockDial = cyl(0.16, 0.16, 0.16, 0xef4444, 16); lockDial.rotation.x = Math.PI/2; lockDial.position.set(0, 1.6, 1.28); vaultGroup.add(lockDial);
    
    [[-1.8, 0.2], [1.8, 0.2]].forEach(([lx, lz]) => {
      const col = cyl(0.12, 0.12, 3.6, 0x334155, 12); col.position.set(lx, 1.8, lz); vaultGroup.add(col);
      const ring = new T.Mesh(new T.TorusGeometry(0.25, 0.03, 8, 20), mat(0x06b6d4, {emissive:0x06b6d4, emissiveIntensity:0.9}));
      ring.rotation.x = Math.PI/2; ring.position.set(lx, 2.8, lz); vaultGroup.add(ring);
    });
    
    const vaultLabel = makeLabel('🔒 CYBER VAULT\\n(KEEP PRIVATE)', {scale:0.42, fs:30, bg:'#0284c7', fg:'#ffffff'});
    vaultLabel.position.set(0, 3.5, 0); vaultGroup.add(vaultLabel);
    root.add(vaultGroup);

    // 2. 3D Public Profile Showcase (Right Side)
    const publicGroup = new T.Group();
    publicGroup.position.set(3.4, 0, -2.2);
    
    const pubPed = Props.pedestal(2.8, 0.7, 2.2, 0x1e293b);
    pubPed.position.y = 0; publicGroup.add(pubPed);
    
    const holoFrame = box(2.6, 2.6, 0.1, 0x10b981); holoFrame.position.set(0, 1.8, 0); publicGroup.add(holoFrame);
    const holoGlass = new T.Mesh(new T.PlaneGeometry(2.4, 2.4), new T.MeshStandardMaterial({color:0x34d399, transparent:true, opacity:0.45, roughness:0.1}));
    holoGlass.position.set(0, 1.8, 0.06); publicGroup.add(holoGlass);
    
    const globeHolo = sph(0.35, 0x10b981, {emissive:0x10b981, emissiveIntensity:0.7});
    globeHolo.position.set(0, 1.8, 0.4); publicGroup.add(globeHolo);
    
    const pubLabel = makeLabel('🌐 PUBLIC PROFILE\\n(SAFE TO SHARE)', {scale:0.42, fs:30, bg:'#059669', fg:'#ffffff'});
    pubLabel.position.set(0, 3.5, 0); publicGroup.add(pubLabel);
    root.add(publicGroup);

    // 3. Characters & Camera
    const {b, g} = bringKids(root, -1.8, 1.4, 1.8, 1.4, 0.25);
    camera.position.set(0, 3.2, 6.2);
    Cam.look.set(0, 1.6, -1.0);

    const introDlg = [
      {who:'girl', expr:'thinking', pose:'point', audio:'audio/girl_025.mp3', text:"Welcome to the Privacy Locker! Some personal data must be locked in the Cyber Vault forever."},
      {who:'boy', expr:'happy', pose:'think', audio:'audio/boy_026.mp3', text:"While other things like hobbies and avatars are fun to share. Let us sort them and see what happens!"}
    ];

    runDialogue(introDlg, ()=>{
      const items = [
        {
          id: 1,
          name: "Home Street Address & House Number",
          icon: "🏠",
          type: "private",
          whyPrivate: "🛡️ EXCELLENT DEFENSE! Locking your home address protects your family from real-world stalking, burglary, and unknown strangers finding where you live.",
          whyPublicRisk: "🚨 CRITICAL DANGER! If you post your real street address publicly, anyone on the internet can see your physical location and put your family in danger!"
        },
        {
          id: 2,
          name: "Favorite Drawing Color & Cartoon Avatar",
          icon: "🎨",
          type: "public",
          whyPublicGood: "✅ SAFE & CREATIVE! Sharing your favorite colors or cartoon avatars expresses your personality without leaking your real identity.",
          whyLockedMiss: "💡 It's totally safe to share your favorite color! It doesn't reveal any sensitive personal data."
        },
        {
          id: 3,
          name: "Secret Account Password (Email & Games)",
          icon: "🔑",
          type: "private",
          whyPrivate: "🛡️ IMPENETRABLE LOCK! Passwords are like toothbrushes — never share them with friends, game chats, or websites (only trusted parents).",
          whyPublicRisk: "🚨 ACCOUNT HIJACKED! Sharing passwords lets bad actors log in, steal your game items, delete your progress, and lock you out forever!"
        },
        {
          id: 4,
          name: "Favorite Video Games & Hobby Tags",
          icon: "🎮",
          type: "public",
          whyPublicGood: "✅ GREAT FOR MAKING FRIENDS! Talking about Minecraft, science, or music lets you find gaming buddies without risking privacy.",
          whyLockedMiss: "💡 Game hobbies are fun and safe to share with other kids!"
        },
        {
          id: 5,
          name: "Mom / Dad's Personal Mobile Number",
          icon: "📱",
          type: "private",
          whyPrivate: "🛡️ VAULT SHIELDED! Phone numbers are personal contact keys. Locking them stops phishing SMS spam, scam calls, and fraud.",
          whyPublicRisk: "🚨 PHONE FLOODED! Scammers can bombard your parents with fake emergency calls, fraud threats, and malware links!"
        },
        {
          id: 6,
          name: 'Cool Gaming Alias: "CyberPixel_99"',
          icon: "🎭",
          type: "public",
          whyPublicGood: "✅ PERFECT DIGITAL SHIELD! Using creative nicknames keeps your real legal name completely hidden and safe from strangers.",
          whyLockedMiss: "💡 Aliases and nicknames are safe because they protect your real name!"
        },
        {
          id: 7,
          name: "Real School Name, Grade & Classroom Section",
          icon: "🏫",
          type: "private",
          whyPrivate: "🛡️ LOCATION GUARDED! Keeping your school name and schedule private prevents strangers from tracking your daily routine.",
          whyPublicRisk: "🚨 DANGEROUS! Posting your exact school and class schedule lets strangers know where you are every weekday!"
        },
        {
          id: 8,
          name: "Favorite Songs & Science Subjects",
          icon: "🎵",
          type: "public",
          whyPublicGood: "✅ WONDERFUL & SAFE! Sharing your favorite music or love for astronomy is 100% safe and inspiring.",
          whyLockedMiss: "💡 Music and science interests have zero safety risk!"
        }
      ];

      let itemIdx = 0;
      let score = 0;

      function renderSortingCard(){
        if(itemIdx >= items.length){
          clearUI();
          try { SFX.win(); SFX.badge(); } catch(e){}
          const sumCard = el('div', 'privacy-summary-card');
          sumCard.style.cssText = `
            position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #090d16 0%, #1e1b4b 100%);
            border: 3.5px solid #38bdf8; border-radius: 26px; padding: 26px 30px;
            box-shadow: 0 25px 70px rgba(56, 189, 248, 0.45); z-index: 90;
            max-width: 600px; width: 92%; color: #fff; text-align: center;
            animation: pop .3s cubic-bezier(.2,.9,.3,1.2);
          `;
          sumCard.innerHTML = `
            <div style="font-size:42px;margin-bottom:6px;">🔒✨</div>
            <div style="font-size:12px;font-weight:900;letter-spacing:2px;color:#38bdf8;text-transform:uppercase;margin-bottom:6px;">
              PRIVACY FORTRESS RATING
            </div>
            <h3 style="margin:0 0 10px;color:#f8fafc;font-size:24px;font-weight:900;">
              ${score >= 7 ? '🌟 Level 5: Master Privacy Guardian!' : '🛡️ Level 4: Certified Privacy Defender!'}
            </h3>
            <p style="margin:0 0 16px;font-size:14.5px;color:#cbd5e1;line-height:1.5;">
              You sorted all 8 items! You understand which data belongs in the unbreakable Cyber Vault and which is safe for your public profile.
            </p>
            <div style="background:rgba(56,189,248,0.15);padding:12px 18px;border-radius:14px;border:1.5px solid #38bdf8;margin-bottom:20px;font-size:16px;font-weight:800;color:#7dd3fc;">
              ⭐ Score: ${score} / 8 Correctly Categorized (+${score * 25} XP)
            </div>
            <button id="btnFinishCh7" style="width:100%;padding:14px;font-size:16px;font-weight:800;border-radius:16px;background:linear-gradient(135deg, #10b981 0%, #059669 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(16,185,129,0.4);">
              PROCEED TO CHAPTER 8 ▶
            </button>
          `;
          sumCard.querySelector('#btnFinishCh7').onclick = () => {
            clearUI();
            const postDlg = [
              {who:'boy', expr:'excited', pose:'cheer', audio:'audio/boy_027.mp3', text:"Locked and safe! My passwords and address are guarded in the Cyber Vault forever."},
              {who:'girl', expr:'happy', pose:'point', audio:'audio/girl_028.mp3', text:"And my gamer avatar is ready for the world. Let us check out Scam Alley next!"}
            ];
            runDialogue(postDlg, ()=>{
              api.done({msg:"Privacy Fortress Sealed! You mastered data classification and consequence awareness."});
            });
          };
          addUI(sumCard);
          return;
        }

        clearUI();
        const cur = items[itemIdx];
        const card = el('div', 'sorting-sim-card');
        card.style.cssText = `
          position: fixed; bottom: 35px; left: 50%; transform: translateX(-50%);
          background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
          border: 3.5px solid #38bdf8; border-radius: 24px; padding: 22px 26px;
          box-shadow: 0 20px 60px rgba(56, 189, 248, 0.4); z-index: 90;
          max-width: 660px; width: 92%; color: #fff; text-align: center;
          animation: pop .3s cubic-bezier(.2,.9,.3,1.2);
        `;

        card.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <span style="font-size:12px;font-weight:900;letter-spacing:1.5px;color:#38bdf8;text-transform:uppercase;">
              DATA SORTING SIMULATION • ITEM ${itemIdx+1} OF ${items.length}
            </span>
            <span style="font-size:12px;background:#334155;color:#f8fafc;padding:3px 10px;border-radius:8px;font-weight:800;">
              ⭐ Score: ${score}/${items.length}
            </span>
          </div>

          <div style="background:rgba(30, 41, 59, 0.85);border:2px dashed #64748b;border-radius:16px;padding:14px 18px;display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:18px;">
            <span style="font-size:32px;">${cur.icon}</span>
            <span style="font-size:18px;font-weight:800;color:#f8fafc;">${cur.name}</span>
          </div>

          <p style="margin:0 0 16px;font-size:14px;color:#cbd5e1;font-weight:600;">
            Where does this personal data belong? Drag or click a destination below:
          </p>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
            <button id="btnDropVault" style="padding:14px 12px;font-size:14.5px;font-weight:800;border-radius:14px;background:linear-gradient(135deg, #0284c7 0%, #0369a1 100%);color:#fff;border:2px solid #38bdf8;cursor:pointer;box-shadow:0 6px 18px rgba(2,132,199,0.4);transition:all .15s;display:flex;flex-direction:column;align-items:center;gap:4px;">
              <span style="font-size:22px;">🔒</span>
              <span>LOCK IN VAULT</span>
              <span style="font-size:11px;opacity:0.85;font-weight:600;">(Private & Confidential)</span>
            </button>

            <button id="btnDropPublic" style="padding:14px 12px;font-size:14.5px;font-weight:800;border-radius:14px;background:linear-gradient(135deg, #059669 0%, #047857 100%);color:#fff;border:2px solid #34d399;cursor:pointer;box-shadow:0 6px 18px rgba(5,150,105,0.4);transition:all .15s;display:flex;flex-direction:column;align-items:center;gap:4px;">
              <span style="font-size:22px;">🌐</span>
              <span>PUT ON PUBLIC PROFILE</span>
              <span style="font-size:11px;opacity:0.85;font-weight:600;">(Safe to Share with World)</span>
            </button>
          </div>
        `;

        function showReviewFeedback(userChoice){
          const isCorrect = (userChoice === cur.type);
          if(isCorrect){
            score++;
            addXP(25);
            try { SFX.correct(); } catch(e){}
          } else {
            try { SFX.buzz(); } catch(e){}
          }

          const targetX = userChoice === 'private' ? -3.4 : 3.4;
          const orbMat = mat(userChoice === 'private' ? 0x0284c7 : 0x10b981, {emissive: userChoice === 'private' ? 0x38bdf8 : 0x34d399, emissiveIntensity: 1.0});
          const orb = new T.Mesh(new T.SphereGeometry(0.24, 16, 16), orbMat);
          orb.position.set(0, 1.4, 0);
          root.add(orb);

          if(userChoice === 'private'){
            wheel.rotation.z += 1.5;
            safeDoor.position.x = -0.4;
          } else {
            globeHolo.scale.set(1.4, 1.4, 1.4);
          }

          let tProg = 0;
          const orbTimer = setInterval(()=>{
            tProg += 0.08;
            orb.position.x = targetX * tProg;
            orb.position.y = 1.4 + Math.sin(tProg * Math.PI) * 0.8;
            orb.position.z = -2.2 * tProg;
            if(tProg >= 1.0){
              clearInterval(orbTimer);
              root.remove(orb);
              safeDoor.position.x = 0;
              globeHolo.scale.set(1.0, 1.0, 1.0);
            }
          }, 30);

          clearUI();
          const revCard = el('div', 'review-modal');
          revCard.style.cssText = `
            position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            border: 3.5px solid ${isCorrect ? '#10b981' : '#ef4444'}; border-radius: 24px; padding: 22px 26px;
            box-shadow: 0 20px 60px ${isCorrect ? 'rgba(16, 185, 129, 0.45)' : 'rgba(239, 68, 68, 0.45)'};
            z-index: 95; max-width: 580px; width: 92%; color: #fff; text-align: center;
            animation: pop .25s ease-out;
          `;

          let consequenceText = "";
          if(userChoice === 'private'){
            consequenceText = isCorrect ? cur.whyPrivate : cur.whyLockedMiss;
          } else {
            consequenceText = isCorrect ? cur.whyPublicGood : cur.whyPublicRisk;
          }

          revCard.innerHTML = `
            <div style="font-size:38px;margin-bottom:6px;">${isCorrect ? '🎯' : '⚠️'}</div>
            <div style="font-size:12px;font-weight:900;letter-spacing:1.5px;color:${isCorrect ? '#4ade80' : '#f87171'};text-transform:uppercase;margin-bottom:4px;">
              ${isCorrect ? 'PERFECT DECISION (+25 XP)' : 'SAFETY WARNING'}
            </div>
            <h3 style="margin:0 0 10px;color:#f8fafc;font-size:20px;font-weight:900;">
              ${cur.icon} ${cur.name}
            </h3>
            <div style="background:rgba(15,23,42,0.7);border-radius:14px;padding:12px 16px;font-size:14.5px;line-height:1.5;color:#e2e8f0;margin-bottom:18px;text-align:left;border-left:4px solid ${isCorrect ? '#10b981' : '#ef4444'};">
              ${consequenceText}
            </div>
            <button id="btnNextItem" style="width:100%;padding:13px;font-size:15px;font-weight:800;border-radius:14px;background:linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 6px 18px rgba(37,99,235,0.4);">
              NEXT ITEM ▶
            </button>
          `;

          revCard.querySelector('#btnNextItem').onclick = () => {
            clearUI();
            itemIdx++;
            renderSortingCard();
          };

          addUI(revCard);
        }

        card.querySelector('#btnDropVault').onclick = () => showReviewFeedback('private');
        card.querySelector('#btnDropPublic').onclick = () => showReviewFeedback('public');
        addUI(card);
      }

      renderSortingCard();
    });
  }
});
'''

    # 3. UPGRADED Chapter 8
    ch8_code = '''/* =====================================================================
   CHAPTER 08: Scam Alley (Kid's Computer Room & Interactive Chat Defense)
   ===================================================================== */
registerChapter({
  id: "ch8",
  title: "Scam Alley",
  logtag: "SCAM ALLEY",
  bg1: "#0f172a",
  bg2: "#1e293b",
  endTitle: "Chapter 8 Complete! Scam Defense Master 🛡️",
  learned: [
    "Scammers use fake urgency, exciting prizes (free Robux/gift cards), or fear to trick you.",
    "Real banks and games NEVER ask for passwords, CVVs, or OTP codes over chat.",
    "Never download or run unknown .exe cheat tools — they are Trojan viruses disguised as helpers!"
  ],
  build(root, api){
    addLights(root, "warm");
    ground(root, 0x1e293b, 40);

    // 1. Kid's Computer Bedroom Environment
    const desk = box(4.4, 0.12, 2.0, 0x334155);
    desk.position.set(0, 0.9, -2.0); root.add(desk);
    
    [[-2.0, -1.2], [2.0, -1.2], [-2.0, -2.8], [2.0, -2.8]].forEach(([lx, lz]) => {
      const leg = cyl(0.06, 0.06, 0.9, 0x1e293b, 8);
      leg.position.set(lx, 0.45, lz); root.add(leg);
    });

    const laptop = Props.laptop(true);
    laptop.position.set(0, 0.96, -1.9);
    laptop.scale.set(1.4, 1.4, 1.4);
    root.add(laptop);

    const chair = Props.chair(0x3b82f6);
    chair.position.set(0, 0, -0.9);
    root.add(chair);

    const poster1 = box(1.2, 1.6, 0.02, 0xec4899); poster1.position.set(-2.8, 3.0, -3.8); root.add(poster1);
    const poster2 = box(1.4, 1.4, 0.02, 0x38bdf8); poster2.position.set(2.8, 3.0, -3.8); root.add(poster2);

    // 2. Characters & Camera
    const {b, g} = bringKids(root, -1.8, 1.2, 1.8, 1.2, 0.3);
    camera.position.set(0, 2.6, 4.4);
    Cam.look.set(0, 1.4, -1.0);

    const introDlg = [
      {who:"boy", expr:"confused", pose:"think", audio:"audio/boy_029.mp3", text:"I just opened my messaging app on my laptop, and strange chat popups are appearing!"},
      {who:"girl", expr:"thinking", pose:"point", audio:"audio/girl_030.mp3", text:"Careful Aarav! Scammers use sneaky tricks. Let us inspect each message and reply wisely!"}
    ];

    runDialogue(introDlg, ()=>{
      const chats = [
        {
          id: 1,
          senderName: "🎁 LuckyGamer_Rewards [Bot]",
          senderAvatar: "🤖",
          incomingMsg: "🎉 CONGRATULATIONS! You won 15,000 FREE ROBUX / V-BUCKS! Click this urgent link within 2 minutes to claim: http://freerobux-gift.fake-login.xyz and enter your game password!",
          options: [
            {
              text: "🤑 Awesome! Clicking the link and entering my password now!",
              isSafe: false,
              replyText: "Thanks! Entering my password right now on the link!",
              feedback: "🚨 PHISHING TRAP TRIGGERED! The link led to a fake clone website. Entering your password would allow scammers to steal your account and lock you out forever! Real games NEVER ask for passwords on external links."
            },
            {
              text: "🛡️ ❌ SCAM ALERT! Real games never ask for passwords on sketchy links. Blocked & Reported!",
              isSafe: true,
              replyText: "❌ Stop scamming! Real game companies never give currency via fake .xyz links or ask for passwords. Reported & Blocked! 🛡️",
              feedback: "🌟 BRILLIANT DEFENSE (+50 XP)! You spotted the fake prize, fake urgency ('2 minutes'), and suspicious domain (`.xyz`). Your account and coins are 100% safe!"
            }
          ]
        },
        {
          id: 2,
          senderName: "🏦 BankSecurity_Alert_URGENT",
          senderAvatar: "⚠️",
          incomingMsg: "🚨 URGENT NOTICE: Your family's bank debit card has been SUSPENDED due to unauthorized charges! Reply immediately with your mother's 16-digit card number, CVV, and SMS OTP code to unlock!",
          options: [
            {
              text: "🛑 ❌ Banks NEVER ask for OTP or card numbers in chat! I'm showing this to my parents!",
              isSafe: true,
              replyText: "❌ Official banks NEVER request OTP codes or CVVs over random chats! I am reporting this fraud and alerting my parents right now!",
              feedback: "🌟 FINANCIAL HERO (+50 XP)! You remembered the golden banking rule: Banks never ask for secret OTPs or CVVs in text or chat. You protected your family from severe financial theft!"
            },
            {
              text: "🏃 Oh no! That sounds terrible! Let me find the card and send the numbers!",
              isSafe: false,
              replyText: "Please don't lock it! Let me get mom's card number right away!",
              feedback: "🚨 FINANCIAL FRAUD! Scammers create panic and fake emergencies so victims act without thinking. Never share any banking digits or OTPs in chat — always ask a parent immediately!"
            }
          ]
        },
        {
          id: 3,
          senderName: "⚡ CheatMaster_Dave404",
          senderAvatar: "👾",
          incomingMsg: "Hey dude! Download this secret game hack installer (Fortnite_Unlimited_Speed_Hack.exe). Run it on your PC to get infinite aimbot and unlock all legendary skins for free!",
          options: [
            {
              text: "🎮 Sweet! Downloading and running the .exe file right now!",
              isSafe: false,
              replyText: "Downloading the .exe right now! Can't wait to try it!",
              feedback: "🚨 MALWARE TROJAN INFECTION! Unknown executable (`.exe`) files from strangers often contain keyloggers and spyware that infect your computer, steal saved logins, and ruin your PC!"
            },
            {
              text: "🗑️ ❌ Never download unknown .exe files! That is a Trojan virus. Deleted & Quarantined!",
              isSafe: true,
              replyText: "❌ No way! Running unknown .exe files installs malware and Trojan viruses. Deleted & Reported! 🗑️",
              feedback: "🌟 CYBER DEFENDER (+50 XP)! You knew that random `.exe` downloads are malware traps. Only download verified software from official certified app stores!"
            }
          ]
        }
      ];

      let chatIdx = 0;
      let score = 0;

      function renderChatScreen(){
        if(chatIdx >= chats.length){
          clearUI();
          try { SFX.win(); SFX.badge(); } catch(e){}
          const sum = el('div', 'scam-summary-card');
          sum.style.cssText = `
            position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #090d16 0%, #1e1b4b 100%);
            border: 3.5px solid #10b981; border-radius: 26px; padding: 26px 30px;
            box-shadow: 0 25px 70px rgba(16, 185, 129, 0.45); z-index: 90;
            max-width: 600px; width: 92%; color: #fff; text-align: center;
            animation: pop .3s cubic-bezier(.2,.9,.3,1.2);
          `;
          sum.innerHTML = `
            <div style="font-size:42px;margin-bottom:6px;">🛡️💬</div>
            <div style="font-size:12px;font-weight:900;letter-spacing:2px;color:#10b981;text-transform:uppercase;margin-bottom:6px;">
              SCAM DEFENSE COMPLETE
            </div>
            <h3 style="margin:0 0 10px;color:#f8fafc;font-size:24px;font-weight:900;">
              All Malicious Chats Defended!
            </h3>
            <p style="margin:0 0 16px;font-size:14.5px;color:#cbd5e1;line-height:1.5;">
              You successfully identified phishing links, fraudulent bank demands, and Trojan malware executables in realistic chat conversations.
            </p>
            <div style="background:rgba(16,185,129,0.15);padding:12px 18px;border-radius:14px;border:1.5px solid #10b981;margin-bottom:20px;font-size:16px;font-weight:800;color:#6ee7b7;">
              ⭐ Score: ${score} / 3 Scams Quarantined (+${score * 50} XP)
            </div>
            <button id="btnFinishCh8" style="width:100%;padding:14px;font-size:16px;font-weight:800;border-radius:16px;background:linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(37,99,235,0.4);">
              PROCEED TO CHAPTER 9 ▶
            </button>
          `;
          sum.querySelector('#btnFinishCh8').onclick = () => {
            clearUI();
            const postDlg = [
              {who:"girl", expr:"happy", pose:"cheer", audio:"audio/girl_033.mp3", text:"Outstanding work! You stopped all three scam traps before they could do any harm."},
              {who:"boy", expr:"excited", pose:"wave", audio:"audio/boy_034.mp3", text:"Now let us see what happens when strangers message us during online gaming!"}
            ];
            runDialogue(postDlg, ()=>{
              api.done({msg:"All Scams Quarantined! You defended your computer and personal accounts."});
            });
          };
          addUI(sum);
          return;
        }

        clearUI();
        const c = chats[chatIdx];
        const chatBox = el('div', 'chat-sim-window');
        chatBox.style.cssText = `
          position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
          background: #0f172a; border: 3px solid #38bdf8; border-radius: 24px;
          box-shadow: 0 25px 70px rgba(15, 23, 42, 0.7); z-index: 90;
          max-width: 680px; width: 94%; overflow: hidden; color: #fff;
          display: flex; flex-direction: column; animation: pop .3s cubic-bezier(.2,.9,.3,1.2);
        `;

        chatBox.innerHTML = `
          <div style="background:#1e293b;padding:12px 18px;border-bottom:1.5px solid #334155;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:22px;">${c.senderAvatar}</span>
              <div>
                <div style="font-size:14.5px;font-weight:800;color:#f8fafc;">${c.senderName}</div>
                <div style="font-size:11.5px;color:#94a3b8;display:flex;align-items:center;gap:4px;">
                  <span style="width:7px;height:7px;background:#ef4444;border-radius:50%;display:inline-block;"></span>
                  Unknown / Unverified Contact
                </div>
              </div>
            </div>
            <span style="font-size:12px;background:#334155;color:#38bdf8;padding:4px 10px;border-radius:8px;font-weight:800;">
              CASE ${chatIdx+1}/3
            </span>
          </div>

          <div id="chatBody" style="padding:16px 18px;max-height:260px;overflow-y:auto;display:flex;flex-direction:column;gap:12px;background:#0b0f19;">
            <div style="display:flex;gap:10px;align-items:flex-start;max-width:85%;">
              <div style="background:#334155;color:#fff;border-radius:18px 18px 18px 4px;padding:12px 16px;font-size:14px;line-height:1.45;border:1.5px solid #475569;box-shadow:0 4px 12px rgba(0,0,0,0.2);">
                ${c.incomingMsg}
              </div>
            </div>
          </div>

          <div style="background:#1e293b;padding:14px 16px;border-top:1.5px solid #334155;">
            <div style="font-size:12px;font-weight:800;letter-spacing:1px;color:#94a3b8;margin-bottom:10px;text-transform:uppercase;">
              Choose Your Chat Reply:
            </div>
            <div style="display:flex;flex-direction:column;gap:8px;">
              ${c.options.map((opt, i) => `
                <button class="chat-opt-btn" data-idx="${i}" style="text-align:left;padding:12px 14px;font-size:13.5px;font-weight:700;border-radius:12px;background:#0f172a;border:1.5px solid #475569;color:#e2e8f0;cursor:pointer;transition:all .15s;line-height:1.4;">
                  ${opt.text}
                </button>
              `).join('')}
            </div>
          </div>
        `;

        const optBtns = chatBox.querySelectorAll('.chat-opt-btn');
        optBtns.forEach(btn => {
          btn.onmouseenter = () => { btn.style.background = '#1e3a8a'; btn.style.borderColor = '#38bdf8'; };
          btn.onmouseleave = () => { btn.style.background = '#0f172a'; btn.style.borderColor = '#475569'; };
          btn.onclick = () => {
            const chosenIdx = parseInt(btn.getAttribute('data-idx'));
            const chosen = c.options[chosenIdx];
            
            if(chosen.isSafe){
              score++;
              addXP(50);
              try { SFX.correct(); } catch(e){}
            } else {
              try { SFX.buzz(); } catch(e){}
            }

            const chatBody = chatBox.querySelector('#chatBody');
            const myBubble = el('div', '', `
              <div style="display:flex;justify-content:flex-end;margin-top:8px;">
                <div style="background:linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);color:#fff;border-radius:18px 18px 4px 18px;padding:12px 16px;font-size:14px;line-height:1.45;max-width:85%;box-shadow:0 4px 12px rgba(37,99,235,0.3);">
                  ${chosen.replyText}
                </div>
              </div>
            `);
            chatBody.appendChild(myBubble);
            chatBody.scrollTop = chatBody.scrollHeight;

            setTimeout(()=>{
              clearUI();
              const fbCard = el('div', 'chat-feedback-card');
              fbCard.style.cssText = `
                position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                border: 3.5px solid ${chosen.isSafe ? '#10b981' : '#ef4444'}; border-radius: 24px; padding: 22px 26px;
                box-shadow: 0 20px 60px ${chosen.isSafe ? 'rgba(16, 185, 129, 0.45)' : 'rgba(239, 68, 68, 0.45)'};
                z-index: 95; max-width: 580px; width: 92%; color: #fff; text-align: center;
                animation: pop .25s ease-out;
              `;

              fbCard.innerHTML = `
                <div style="font-size:38px;margin-bottom:6px;">${chosen.isSafe ? '🛡️' : '🚨'}</div>
                <div style="font-size:12px;font-weight:900;letter-spacing:1.5px;color:${chosen.isSafe ? '#4ade80' : '#f87171'};text-transform:uppercase;margin-bottom:4px;">
                  ${chosen.isSafe ? 'SAFE REPLY • THREAT BLOCKED' : 'SECURITY WARNING'}
                </div>
                <h3 style="margin:0 0 10px;color:#f8fafc;font-size:20px;font-weight:900;">
                  ${chosen.isSafe ? 'Scam Defeated!' : 'Risky Action!'}
                </h3>
                <div style="background:rgba(15,23,42,0.7);border-radius:14px;padding:14px 16px;font-size:14.5px;line-height:1.5;color:#e2e8f0;margin-bottom:18px;text-align:left;border-left:4px solid ${chosen.isSafe ? '#10b981' : '#ef4444'};">
                  ${chosen.feedback}
                </div>
                <button id="btnNextChat" style="width:100%;padding:13px;font-size:15px;font-weight:800;border-radius:14px;background:linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 6px 18px rgba(37,99,235,0.4);">
                  ${chatIdx < chats.length - 1 ? 'NEXT CHAT MESSAGE ▶' : 'VIEW FINAL REVIEW ▶'}
                </button>
              `;

              fbCard.querySelector('#btnNextChat').onclick = () => {
                clearUI();
                chatIdx++;
                renderChatScreen();
              };

              addUI(fbCard);
            }, 600);
          };
        });

        addUI(chatBox);
      }

      renderChatScreen();
    });
  }
});
'''

    # 4. UPGRADED Chapter 10
    ch10_code = '''/* =====================================================================
   CHAPTER 10: Truth Lab (Dual Truth/Falsehood Meters & Forensic Level)
   ===================================================================== */
registerChapter({
  id: "ch10",
  title: "Truth Lab",
  logtag: "TRUTH LAB",
  bg1: "#1e1b4b",
  bg2: "#312e81",
  endTitle: "Chapter 10 Complete! Forensic Truth Master 🔍",
  learned: [
    "Not everything online or on social media is true — inspect before you believe.",
    "Ask: Who wrote it? Is there real scientific evidence? Does it come from official verified sources?",
    "AI voice clones and deepfakes can impersonate real people. Fact-check with peer-reviewed data!"
  ],
  build(root, api){
    Props.truthLabEnv(root);
    const {b, g} = bringKids(root, -1.8, 1.2, 1.8, 1.2, 0.3);
    camera.position.set(0, 3.2, 6.2);
    Cam.look.set(0, 1.6, -1.0);

    const introDlg = [
      {who:"boy", expr:"confused", pose:"think", audio:"audio/boy_039.mp3", text:"Welcome to the Truth Forensic Lab! Four viral news headlines need investigation."},
      {who:"girl", expr:"thinking", pose:"point", audio:"audio/girl_040.mp3", text:"Let us analyze the evidence, fill our Truth & Falsehood Meters, and determine our Forensic Level!"}
    ];

    runDialogue(introDlg, ()=>{
      const cases = [
        {
          id: 1,
          headline: "🍋 Miracle Cure Hoax: Drinking raw salt, garlic, and boiled lemon water completely cures all viral infections in 24 hours!",
          category: "Viral Social Media Health Rumor",
          evidence: "🔬 Lab Spectral Analysis: Zero clinical trials or medical peer-reviewed evidence. Health organizations (WHO / CDC) confirm this is unverified and potentially dangerous.",
          isTruth: false,
          debunkExplanation: "🛡️ HOAX DEBUNKED (+50 XP)! Fake home remedies spread rapidly through viral reposts. Believing them delays real medical treatment. Always consult qualified doctors!"
        },
        {
          id: 2,
          headline: "🌌 NASA Space Discovery: James Webb Space Telescope confirms atmospheric water vapor and carbon molecules on distant exoplanet K2-18b!",
          category: "Astrophysics & Space Science",
          evidence: "📡 Official NASA.gov & European Space Agency release: Spectrometer infrared sensor data cross-verified by hundreds of global astrophysicists.",
          isTruth: true,
          truthExplanation: "🌟 VERIFIED FACT (+50 XP)! Backed by real infrared telescope sensors, published in peer-reviewed scientific journals, and confirmed by global astronomers!"
        },
        {
          id: 3,
          headline: "🎥 Viral Video: Famous Tech CEO announces he will send $5,000 to anyone who clicks a crypto link today!",
          category: "AI Synthetic Video & Deepfake Scam",
          evidence: "🤖 AI Audio-Visual Forensic Scan: Synthetic voice frequency artifacts detected. Lip movements do not match English phoneme waveforms. Domain linked to phishing server.",
          isTruth: false,
          debunkExplanation: "🛡️ DEEPFAKE EXPOSED (+50 XP)! Scammers use AI voice and face cloning to impersonate famous celebrities. Official charity grants are never distributed via sketchy crypto links!"
        },
        {
          id: 4,
          headline: "🦋 Monarch Butterfly Migration: Monarch butterflies fly over 3,000 miles every autumn from Canada to Mexican mountain forests!",
          category: "Biology & Wildlife Conservation",
          evidence: "🌿 Wildlife Tracking Data: Thousands of tagged butterflies monitored by biologists over 50 years. Documented by National Geographic and wildlife sanctuaries.",
          isTruth: true,
          truthExplanation: "🌟 VERIFIED FACT (+50 XP)! An extraordinary natural migration documented by thousands of field biologists and tracking data across North America!"
        }
      ];

      let caseIdx = 0;
      let truthScore = 0;
      let falseScore = 0;
      let totalCorrect = 0;

      function renderLabCase(){
        if(caseIdx >= cases.length){
          clearUI();
          try { SFX.win(); SFX.badge(); } catch(e){}
          
          let levelTitle = "Master Truth Detective (Level 5)";
          let levelColor = "#10b981";
          if(totalCorrect < 3){
            levelTitle = "Junior Fact-Checker (Level 3)";
            levelColor = "#f59e0b";
          }

          const sum = el('div', 'truth-level-card');
          sum.style.cssText = `
            position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #090d16 0%, #1e1b4b 100%);
            border: 3.5px solid ${levelColor}; border-radius: 26px; padding: 26px 30px;
            box-shadow: 0 25px 70px rgba(16, 185, 129, 0.45); z-index: 90;
            max-width: 620px; width: 92%; color: #fff; text-align: center;
            animation: pop .3s cubic-bezier(.2,.9,.3,1.2);
          `;

          const truthPct = Math.min(100, Math.round((truthScore / 2) * 100));
          const falsePct = Math.min(100, Math.round((falseScore / 2) * 100));

          sum.innerHTML = `
            <div style="font-size:42px;margin-bottom:6px;">🔍🎖️</div>
            <div style="font-size:12px;font-weight:900;letter-spacing:2px;color:${levelColor};text-transform:uppercase;margin-bottom:6px;">
              FORENSIC TRUTH LAB CERTIFICATION
            </div>
            <h3 style="margin:0 0 10px;color:#f8fafc;font-size:24px;font-weight:900;">
              ${levelTitle}
            </h3>
            
            <div style="background:rgba(15,23,42,0.8);border-radius:16px;padding:16px 18px;margin-bottom:18px;display:flex;flex-direction:column;gap:12px;">
              <div>
                <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:800;color:#34d399;margin-bottom:6px;">
                  <span>🟢 TRUTH METER (Verified Facts)</span>
                  <span>${truthPct}%</span>
                </div>
                <div style="background:#334155;height:12px;border-radius:8px;overflow:hidden;">
                  <div style="background:#10b981;height:100%;width:${truthPct}%;transition:width .4s;"></div>
                </div>
              </div>

              <div>
                <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:800;color:#f87171;margin-bottom:6px;">
                  <span>🔴 FALSEHOOD METER (Hoaxes Debunked)</span>
                  <span>${falsePct}%</span>
                </div>
                <div style="background:#334155;height:12px;border-radius:8px;overflow:hidden;">
                  <div style="background:#ef4444;height:100%;width:${falsePct}%;transition:width .4s;"></div>
                </div>
              </div>
            </div>

            <p style="margin:0 0 16px;font-size:14px;color:#cbd5e1;line-height:1.5;">
              You examined all 4 forensic cases and calibrated both meters to perfection! You have the critical eye to protect the web from fake news.
            </p>

            <button id="btnFinishCh10" style="width:100%;padding:14px;font-size:16px;font-weight:800;border-radius:16px;background:linear-gradient(135deg, #10b981 0%, #059669 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(16,185,129,0.4);">
              PROCEED TO CHAPTER 11 ▶
            </button>
          `;

          sum.querySelector('#btnFinishCh10').onclick = () => {
            clearUI();
            const postDlg = [
              {who:"boy", expr:"excited", pose:"cheer", audio:"audio/boy_041.mp3", text:"Both meters are at 100%! We can spot fake viral stories and verify real science anytime."},
              {who:"girl", expr:"happy", pose:"point", audio:"audio/girl_042.mp3", text:"Now let us see the entire global journey of the internet across our panoramic city!"}
            ];
            runDialogue(postDlg, ()=>{
              api.done({msg:"Truth Lab Certified! You mastered fact-checking and debunking misinformation."});
            });
          };
          addUI(sum);
          return;
        }

        clearUI();
        const cur = cases[caseIdx];

        const truthPct = Math.min(100, Math.round((truthScore / 2) * 100));
        const falsePct = Math.min(100, Math.round((falseScore / 2) * 100));

        const card = el('div', 'truth-case-card');
        card.style.cssText = `
          position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
          background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
          border: 3.5px solid #38bdf8; border-radius: 24px; padding: 20px 24px;
          box-shadow: 0 20px 60px rgba(56, 189, 248, 0.45); z-index: 90;
          max-width: 680px; width: 92%; color: #fff; text-align: center;
          animation: pop .3s cubic-bezier(.2,.9,.3,1.2);
        `;

        card.innerHTML = `
          <div style="background:rgba(15,23,42,0.85);border-radius:14px;padding:12px 14px;margin-bottom:14px;border:1px solid #334155;display:grid;grid-template-columns:1fr 1fr;gap:14px;text-align:left;">
            <div>
              <div style="display:flex;justify-content:space-between;font-size:11.5px;font-weight:800;color:#34d399;margin-bottom:4px;">
                <span>🟢 TRUTH METER</span>
                <span>${truthPct}%</span>
              </div>
              <div style="background:#334155;height:8px;border-radius:6px;overflow:hidden;">
                <div style="background:#10b981;height:100%;width:${truthPct}%;transition:width .3s;"></div>
              </div>
            </div>

            <div>
              <div style="display:flex;justify-content:space-between;font-size:11.5px;font-weight:800;color:#f87171;margin-bottom:4px;">
                <span>🔴 FALSEHOOD METER</span>
                <span>${falsePct}%</span>
              </div>
              <div style="background:#334155;height:8px;border-radius:6px;overflow:hidden;">
                <div style="background:#ef4444;height:100%;width:${falsePct}%;transition:width .3s;"></div>
              </div>
            </div>
          </div>

          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <span style="font-size:11.5px;font-weight:900;letter-spacing:1px;color:#38bdf8;text-transform:uppercase;">
              CASE ${caseIdx+1} OF 4 • ${cur.category}
            </span>
            <span style="font-size:11.5px;background:#0284c7;color:#fff;padding:2px 8px;border-radius:6px;font-weight:800;">
              FORENSIC SCAN
            </span>
          </div>

          <h3 style="margin:0 0 10px;color:#f8fafc;font-size:17px;font-weight:900;line-height:1.4;text-align:left;">
            "${cur.headline}"
          </h3>

          <div style="background:rgba(30,41,59,0.7);border-radius:12px;padding:10px 14px;font-size:13.5px;line-height:1.45;color:#cbd5e1;text-align:left;margin-bottom:16px;border-left:3.5px solid #38bdf8;">
            ${cur.evidence}
          </div>

          <p style="margin:0 0 12px;font-size:13.5px;font-weight:700;color:#f1f5f9;">
            What is the official forensic verdict?
          </p>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
            <button id="btnVerdictTrue" style="padding:12px;font-size:14.5px;font-weight:800;border-radius:12px;background:linear-gradient(135deg, #10b981 0%, #059669 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 6px 16px rgba(16,185,129,0.35);">
              ✅ VERIFY AS TRUTH / REAL FACT
            </button>

            <button id="btnVerdictFalse" style="padding:12px;font-size:14.5px;font-weight:800;border-radius:12px;background:linear-gradient(135deg, #ef4444 0%, #dc2626 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 6px 16px rgba(239,68,68,0.35);">
              ❌ DEBUNK AS FAKE / HOAX
            </button>
          </div>
        `;

        function handleVerdict(userIsTruth){
          const isCorrect = (userIsTruth === cur.isTruth);
          if(isCorrect){
            totalCorrect++;
            if(cur.isTruth){
              truthScore++;
            } else {
              falseScore++;
            }
            addXP(50);
            try { SFX.correct(); } catch(e){}
          } else {
            try { SFX.buzz(); } catch(e){}
          }

          clearUI();
          const fbCard = el('div', 'verdict-feedback-card');
          fbCard.style.cssText = `
            position: fixed; top: 45%; left: 50%; transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            border: 3.5px solid ${isCorrect ? '#10b981' : '#ef4444'}; border-radius: 24px; padding: 22px 26px;
            box-shadow: 0 20px 60px ${isCorrect ? 'rgba(16, 185, 129, 0.45)' : 'rgba(239, 68, 68, 0.45)'};
            z-index: 95; max-width: 580px; width: 92%; color: #fff; text-align: center;
            animation: pop .25s ease-out;
          `;

          const explanation = cur.isTruth ? cur.truthExplanation : cur.debunkExplanation;

          fbCard.innerHTML = `
            <div style="font-size:38px;margin-bottom:6px;">${isCorrect ? '🔬' : '⚠️'}</div>
            <div style="font-size:12px;font-weight:900;letter-spacing:1.5px;color:${isCorrect ? '#4ade80' : '#f87171'};text-transform:uppercase;margin-bottom:4px;">
              ${isCorrect ? 'VERDICT CONFIRMED (+50 XP)' : 'INCORRECT VERDICT'}
            </div>
            <h3 style="margin:0 0 10px;color:#f8fafc;font-size:20px;font-weight:900;">
              ${cur.isTruth ? '🟢 Authentic Verified Fact' : '🔴 Debunked Hoax / Fake'}
            </h3>
            <div style="background:rgba(15,23,42,0.7);border-radius:14px;padding:14px 16px;font-size:14.5px;line-height:1.5;color:#e2e8f0;margin-bottom:18px;text-align:left;border-left:4px solid ${isCorrect ? '#10b981' : '#ef4444'};">
              ${explanation}
            </div>
            <button id="btnNextCase" style="width:100%;padding:13px;font-size:15px;font-weight:800;border-radius:14px;background:linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);color:#fff;border:none;cursor:pointer;box-shadow:0 6px 18px rgba(37,99,235,0.4);">
              ${caseIdx < cases.length - 1 ? 'INVESTIGATE NEXT CASE ▶' : 'VIEW FORENSIC LEVEL ▶'}
            </button>
          `;

          fbCard.querySelector('#btnNextCase').onclick = () => {
            clearUI();
            caseIdx++;
            renderLabCase();
          };

          addUI(fbCard);
        }

        card.querySelector('#btnVerdictTrue').onclick = () => handleVerdict(true);
        card.querySelector('#btnVerdictFalse').onclick = () => handleVerdict(false);
        addUI(card);
      }

      renderLabCase();
    });
  }
});
'''

    # Combine everything
    new_html = head_part + '\n' + ch1_to_6 + '\n\n' + ch7_code + '\n\n' + ch8_code + '\n\n' + ch9_code + '\n\n' + ch10_code + '\n\n' + ch11_code + '\n\n' + ch12_code + '\n\n' + fireworks_helper + '\n\n' + ch13_code + '\n\n' + boot_part

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    with open('internet-smart-adventure.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    registered = re.findall(r'registerChapter\(\{[\s\S]*?id:\s*[\x27\x22]([^\x27\x22]+)[\x27\x22][\s\S]*?title:\s*[\x27\x22]([^\x27\x22]+)[\x27\x22]', new_html)
    print(f'Successfully assembled EXACTLY {len(registered)} chapters into index.html and internet-smart-adventure.html!')
    for i, (cid, title) in enumerate(registered):
        print(f'  {i+1}. {cid}: {title}')

if __name__ == '__main__':
    main()
