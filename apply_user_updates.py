import re
import subprocess

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. REMOVE CHAPTER 14
# Find CHAPTER 14 in html
pos_ch14 = html.find("/* ================= CHAPTER 14")
if pos_ch14 == -1:
    pos_ch14 = html.find("registerChapter({\n  id:'ch14'")
    if pos_ch14 != -1:
        pos_ch14 = html.rfind("/*", 0, pos_ch14)

pos_reg = html.find("/* =============== CHAPTER REGISTRATION")
if pos_ch14 != -1 and pos_reg != -1:
    print(f"Removing Chapter 14 from char {pos_ch14} to {pos_reg}...")
    html = html[:pos_ch14] + "\n\n" + html[pos_reg:]

# Update CHAPTERS array registration to remove ch14
html = re.sub(r'const CHAPTERS=\[[^\]]*\];', """const CHAPTERS=[
  CHAPTER_DEFS['ch1'], CHAPTER_DEFS['ch2'], CHAPTER_DEFS['ch3'],
  CHAPTER_DEFS['ch4'], CHAPTER_DEFS['ch5'], CHAPTER_DEFS['ch6'],
  CHAPTER_DEFS['ch7'], CHAPTER_DEFS['ch8'], CHAPTER_DEFS['ch9'],
  CHAPTER_DEFS['ch10'], CHAPTER_DEFS['ch11'], CHAPTER_DEFS['ch12'],
  CHAPTER_DEFS['ch13']
];""", html)

# Update total count in HUD & Teacher Mode (14 -> 13)
html = html.replace("14 chapters", "13 chapters")
html = html.replace("0 / 14 chapters", "0 / 13 chapters")
html = html.replace("14 / 14", "13 / 13")

# 2. UPGRADE CHAPTER 2: ULTRA-SMOOTH BI-DIRECTIONAL PACKET ANIMATION WITH FLOATING MESSAGE LABELS & COLOR SHIFT
new_ch2_code = """/* =====================================================================
   CHAPTER 02: How Does the Internet Work? (Smooth Bi-Directional Packet Journey)
   ===================================================================== */
registerChapter({
  id:'ch2', title:'How Does the Internet Work?', logtag:'SIMULATION',
  bg1:'#cfeaff', bg2:'#eef6ff',
  endTitle:'Chapter 2 Complete!',
  learned:[
    'Your device sends a request through Wi-Fi and a router.',
    'A server stores information and sends it back.',
    'Data travels as tiny packets — incredibly fast!'
  ],
  build(root, api){
    addLights(root, 'cool'); ground(root, 0xdfeeff, 40);
    
    const nodes = [
      { name:'Laptop', icon:'💻', x:-5.5, z:0, desc:'Your device creates a request and splits it into data packets.' },
      { name:'Wi-Fi', icon:'📡', x:-1.8, z:0, desc:'Broadcasts packets through radio waves without wires.' },
      { name:'Router', icon:'🔀', x:1.8, z:0, desc:'Directs packets through the fastest internet superhighway.' },
      { name:'Server', icon:'🗄️', x:5.5, z:0, desc:'Powerful computer storing global knowledge that answers your request.' }
    ];
    
    const nodeMeshes = {};
    nodes.forEach(n=>{
      const pod = Props.pedestal(1.6, 0.8, 1.6, 0xffffff);
      pod.position.set(n.x, 0, n.z); root.add(pod);
      
      const lbl = makeLabel(n.icon + ' ' + n.name, {scale:0.42, fs:36, bg:'rgba(47,124,224,.95)', fg:'#fff', border:'#fff'});
      lbl.position.set(n.x, 2.3, n.z); root.add(lbl);
      
      if(n.name==='Laptop'){
        const lap = Props.laptop(true); lap.position.set(n.x, 0.82, n.z); root.add(lap);
        nodeMeshes['Laptop'] = lap;
      } else if(n.name==='Wi-Fi'){
        const pole = cyl(0.08,0.12,1.2,0x6db3f2,12); pole.position.set(n.x, 1.4, n.z); root.add(pole);
        const beacon = sph(0.28, 0x38bdf8, {emissive:0x38bdf8, emissiveIntensity:0.8}); beacon.position.set(n.x, 2.0, n.z); root.add(beacon);
        nodeMeshes['Wi-Fi'] = beacon;
      } else if(n.name==='Router'){
        const rbox = box(0.9,0.22,0.6,0x3a4250); rbox.position.set(n.x, 0.92, n.z); root.add(rbox);
        [-0.3, 0, 0.3].forEach(ax=>{ const ant=cyl(0.015,0.015,0.4,0x6b7280); ant.position.set(n.x+ax, 1.2, n.z-0.2); root.add(ant); });
        nodeMeshes['Router'] = rbox;
      } else {
        const srv = box(1.0,1.6,0.8,0x2c3340); srv.position.set(n.x, 1.6, n.z); root.add(srv);
        for(let u=0;u<4;u++){ const led=box(0.7,0.15,0.02,0x38bdf8); led.position.set(n.x, 1.0+u*0.35, n.z+0.41); root.add(led); }
        nodeMeshes['Server'] = srv;
      }
      
      makeClickable(pod, ()=>{ api.prompt(`💡 ${n.name}: ${n.desc}`); SFX.pop(); });
    });
    
    // Glowing Data Cables Connecting Nodes
    const cableMat = new T.MeshStandardMaterial({color:0x38bdf8, emissive:0x0284c7, emissiveIntensity:0.5, transparent:true, opacity:0.75});
    [[-5.5, -1.8], [-1.8, 1.8], [1.8, 5.5]].forEach(([x1, x2])=>{
      const curve = new T.LineCurve3(new T.Vector3(x1, 0.85, 0), new T.Vector3(x2, 0.85, 0));
      const tube = new T.Mesh(new T.TubeGeometry(curve, 24, 0.05, 12, false), cableMat);
      root.add(tube);
    });
    
    // Glowing Animated Data Packet Orb with Outer Halo Ring
    const packetGroup = new T.Group();
    packetGroup.position.set(-5.5, 0.85, 0);
    
    const packetMat = new T.MeshStandardMaterial({
      color: 0x00f0ff,
      emissive: 0x00f0ff,
      emissiveIntensity: 1.2,
      roughness: 0.1
    });
    const packetCore = new T.Mesh(new T.SphereGeometry(0.22, 24, 24), packetMat);
    packetGroup.add(packetCore);
    
    const ringMat = new T.MeshBasicMaterial({color: 0x38bdf8, transparent: true, opacity: 0.6});
    const packetRing = new T.Mesh(new T.RingGeometry(0.28, 0.36, 24), ringMat);
    packetRing.rotation.x = Math.PI / 2;
    packetGroup.add(packetRing);
    
    // Floating Speech Banner Above Packet
    let packetMsgLabel = makeLabel('📤 "Hi! Search Science Project"', {scale:0.42, fs:32, bg:'rgba(14,165,233,0.95)', fg:'#fff', border:'#fff'});
    packetMsgLabel.position.set(0, 0.65, 0);
    packetGroup.add(packetMsgLabel);
    
    // Pulse Light
    const packetLight = new T.PointLight(0x00f0ff, 1.8, 4.0);
    packetLight.position.set(0, 0, 0);
    packetGroup.add(packetLight);
    
    root.add(packetGroup);
    
    const {b, g} = bringKids(root, -3.6, 2.0, 3.6, 2.0, 0.2);
    camera.position.set(0, 4.5, 7.5); Cam.look.set(0, 1.2, 0);
    
    const dialogues = [
      {who:'boy', expr:'excited', pose:'think', audio:'audio/boy_005.mp3', text:"So when I send a message, it travels all the way to a global server and back?!"},
      {who:'girl', expr:'happy', pose:'point', audio:'audio/girl_006.mp3', text:"Exactly! Tap the glowing Data Packet to watch it travel forward and bring back the answer!"},
      {who:'boy', expr:'excited', pose:'cheer', audio:'audio/boy_007.mp3', text:"Watch how fast it zooms from my laptop to the server and returns!"}
    ];
    
    runDialogue(dialogues, ()=>{
      api.prompt("🚀 Tap the Glowing Data Packet to launch the request across the network!");
      
      let isAnimating = false;
      makeClickable(packetGroup, ()=>{
        if(isAnimating) return;
        isAnimating = true;
        SFX.whoosh();
        
        // Smooth multi-waypoint spline animation: Laptop (-5.5) -> WiFi (-1.8) -> Router (1.8) -> Server (5.5) -> and return back
        const waypointsForward = [-5.5, -1.8, 1.8, 5.5];
        const waypointsReturn = [5.5, 1.8, -1.8, -5.5];
        
        // Update label for forward trip
        packetGroup.remove(packetMsgLabel);
        packetMsgLabel = makeLabel('📤 [Message Sent: "Search Science 🌟"]', {scale:0.44, fs:32, bg:'rgba(2,132,199,0.95)', fg:'#fff', border:'#fff'});
        packetMsgLabel.position.set(0, 0.65, 0);
        packetGroup.add(packetMsgLabel);
        
        let leg = 0;
        let t = 0;
        let isReturnTrip = false;
        
        function animatePacket(){
          t += 0.035;
          const currentWaypoints = isReturnTrip ? waypointsReturn : waypointsForward;
          const startX = currentWaypoints[leg];
          const endX = currentWaypoints[leg + 1];
          
          // Smooth sinusoidal interpolation
          const easeT = (1 - Math.cos(t * Math.PI)) / 2;
          packetGroup.position.x = startX + (endX - startX) * easeT;
          packetGroup.position.y = 0.85 + Math.sin(t * Math.PI) * 0.25; // Gentle bounce
          packetRing.rotation.z += 0.08;
          
          if(t >= 1.0){
            t = 0;
            leg++;
            SFX.pop();
            
            if(!isReturnTrip && leg === waypointsForward.length - 1){
              // Reached Server! Pause briefly, pulse server green, change color, start return
              isReturnTrip = true;
              leg = 0;
              
              // Server Processing Effect
              packetMat.color.setHex(0x10b981);
              packetMat.emissive.setHex(0x10b981);
              packetLight.color.setHex(0x10b981);
              ringMat.color.setHex(0x34d399);
              
              packetGroup.remove(packetMsgLabel);
              packetMsgLabel = makeLabel('📥 [Message Received: "Science Results Ready! 🚀"]', {scale:0.44, fs:32, bg:'rgba(5,150,105,0.95)', fg:'#fff', border:'#fff'});
              packetMsgLabel.position.set(0, 0.65, 0);
              packetGroup.add(packetMsgLabel);
              
              toast("⚙️ Server Processed Request: Sending answer back to Laptop!");
              setTimeout(()=>{ requestAnimationFrame(animatePacket); }, 600);
              return;
            } else if(isReturnTrip && leg === waypointsReturn.length - 1){
              // Reached Laptop! Complete!
              packetGroup.position.set(-5.5, 0.85, 0);
              SFX.fanfare();
              addXP(75);
              toast("🎉 Message Delivered & Loaded in 0.02 seconds!");
              api.done({msg:"Data packet traveled to server and returned successfully with your answer!"});
              return;
            }
          }
          requestAnimationFrame(animatePacket);
        }
        
        requestAnimationFrame(animatePacket);
      });
    });
  }
});"""

# Replace Chapter 2 in html
pos_ch2_start = html.find("/* =====================================================================\n   CHAPTER 02")
if pos_ch2_start == -1:
    pos_ch2_start = html.find("/* ================= CHAPTER 02")
pos_ch3_start = html.find("/* =====================================================================\n   CHAPTER 03")
if pos_ch3_start == -1:
    pos_ch3_start = html.find("/* ================= CHAPTER 03")

print(f"Replacing Chapter 02 from {pos_ch2_start} to {pos_ch3_start}...")
html = html[:pos_ch2_start] + new_ch2_code + "\n\n" + html[pos_ch3_start:]

# 3. UPGRADE CHAPTER 13: 5 CONTINUOUS CELEBRATION ROCKETS & JUMPING CHARACTER CELEBRATION
pos_ch13_start = html.find("/* ================= CHAPTER 13")
if pos_ch13_start == -1:
    pos_ch13_start = html.find("CHAPTER 13")
    pos_ch13_start = html.rfind("/*", 0, pos_ch13_start)

pos_after_ch13 = html.find("/* =============== CHAPTER REGISTRATION")

new_ch13_code = """/* =====================================================================
   CHAPTER 13: Internet Smart Master (Grand Academy Graduation & 5 Fireworks Celebration)
   ===================================================================== */
registerChapter({
  id: "ch13",
  title: "Internet Smart Master",
  logtag: "SIMULATION",
  bg1: "#0b132b",
  bg2: "#1c2541",
  endTitle: "🎉 INTERNET SMART MASTER GRADUATION!",
  learned: [
    "You mastered passwords, scams, privacy, balance, and kindness.",
    "The internet is powerful when used with smart safety rules.",
    "Certified as an official Grade 6 Cyber Smart Explorer!"
  ],
  build(root, api){
    Props.digitalCityEnv(root);
    
    // Characters Aarav and Meera
    const {b, g} = bringKids(root, -1.8, 11.2, 1.8, 11.2, 0);
    camera.position.set(0, 6.2, 16.8);
    Cam.look.set(0, 4.2, 11.0);
    
    // Graduation Stage & Cyber Master Podium
    const stage = box(9.0, 0.6, 6.0, 0x1e293b);
    stage.position.set(0, 3.2, 11.0); root.add(stage);
    
    const bannerMat = new T.MeshStandardMaterial({color:0x3b82f6, roughness:0.2, metalness:0.8});
    const banner = new T.Mesh(new T.BoxGeometry(7.2, 1.2, 0.1), bannerMat);
    banner.position.set(0, 6.4, 8.5); root.add(banner);
    
    const bannerLbl = makeLabel("🏆 CYBER SECURITY GRADUATION CEREMONY 🎓", {scale:0.62, fs:38, bg:"#1d4ed8", fg:"#ffffff", border:"#93c5fd"});
    bannerLbl.position.set(0, 6.4, 8.56); root.add(bannerLbl);
    
    const introDlg = [
      {who:"boy", expr:"excited", pose:"cheer", audio:"audio/boy_043.mp3", text:"WE DID IT! We explored the entire internet, defended against scams, built strong passwords, and helped our community!"},
      {who:"girl", expr:"happy", pose:"wave", audio:"audio/girl_044.mp3", text:"We are now officially certified Internet Smart Champions! Tap the Graduation Trophy to launch the Grand 5-Rocket Celebration!"}
    ];
    
    runDialogue(introDlg, ()=>{
      const trophyGroup = new T.Group();
      trophyGroup.position.set(0, 3.8, 10.5);
      
      const trophyPed = Props.pedestal(1.4, 0.6, 1.4, 0x1e293b);
      trophyPed.position.y = 0; trophyGroup.add(trophyPed);
      
      const cupMat = new T.MeshStandardMaterial({color:0xfbbf24, metalness:0.9, roughness:0.1, emissive:0xf59e0b, emissiveIntensity:0.6});
      const cup = new T.Mesh(new T.CylinderGeometry(0.35, 0.18, 0.8, 24), cupMat);
      cup.position.y = 0.7; trophyGroup.add(cup);
      
      const star = sph(0.2, 0xffffff, {emissive:0xfef08a, emissiveIntensity:1.0});
      star.position.y = 1.3; trophyGroup.add(star);
      
      const cupLbl = makeLabel("🌟 TAP TO GRADUATE & CELEBRATE! 🚀", {scale:0.46, fs:34, bg:"#eab308", fg:"#0f172a"});
      cupLbl.position.set(0, 1.8, 0); trophyGroup.add(cupLbl);
      
      root.add(trophyGroup);
      api.prompt("🏆 Tap the Golden Graduation Trophy to ignite the Grand Celebration!");
      
      let celebrated = false;
      makeClickable(trophyGroup, ()=>{
        if(celebrated) return;
        celebrated = true;
        
        // Characters Celebrate: Continuous Jumping and Cheering
        b.pose = 'cheer';
        g.pose = 'wave';
        
        // Continuous jumping animation for characters
        let jumpTime = 0;
        const jumpAnim = setInterval(()=>{
          jumpTime += 0.15;
          if(b.group) b.group.position.y = 3.5 + Math.abs(Math.sin(jumpTime * 3)) * 0.6;
          if(g.group) g.group.position.y = 3.5 + Math.abs(Math.sin((jumpTime + 0.5) * 3)) * 0.6;
        }, 30);
        
        // Blast 5 Rockets continuously one after another into the sky
        const rocketColors = [
          { name: "Crimson Glory", col: 0xef4444, x: -3.5, z: 7.0 },
          { name: "Cyan Spark", col: 0x06b6d4, x: -1.8, z: 5.5 },
          { name: "Emerald Nova", col: 0x10b981, x: 0, z: 4.5 },
          { name: "Purple Starlight", col: 0xa855f7, x: 1.8, z: 5.5 },
          { name: "Golden Rainbow Finale", col: 0xf59e0b, x: 3.5, z: 7.0 }
        ];
        
        let rocketIdx = 0;
        const rocketInterval = setInterval(()=>{
          if(rocketIdx < rocketColors.length){
            const rc = rocketColors[rocketIdx];
            launchCelebrationRocket(root, rc.x, rc.z, rc.col, rc.name);
            rocketIdx++;
          } else {
            clearInterval(rocketInterval);
            setTimeout(()=>{
              clearInterval(jumpAnim);
              addXP(200);
              api.done({
                msg: "🎓 CONGRATULATIONS! You have officially graduated as an Internet Smart Master! 🌟"
              });
            }, 3200);
          }
        }, 700); // Launches 1 rocket every 700ms continuously for 5 rockets
      });
    });
  }
});

// 5-Rocket Celebration Particle System Helper
function launchCelebrationRocket(root, startX, startZ, colorHex, rocketName){
  try { SFX.whoosh(); } catch(e){}
  
  // Rocket Shell
  const rocket = new T.Mesh(
    new T.CylinderGeometry(0.08, 0.14, 0.6, 12),
    new T.MeshStandardMaterial({color: colorHex, emissive: colorHex, emissiveIntensity: 1.5})
  );
  rocket.position.set(startX, 3.8, startZ);
  root.add(rocket);
  
  // Rocket Trail Light
  const rLight = new T.PointLight(colorHex, 2.5, 6.0);
  rLight.position.set(0, 0, 0);
  rocket.add(rLight);
  
  // Rocket Ascend Animation
  let altitude = 3.8;
  const targetAlt = 10.5 + Math.random() * 2.5;
  const ascendTimer = setInterval(()=>{
    altitude += 0.45;
    rocket.position.y = altitude;
    rocket.rotation.y += 0.2;
    
    if(altitude >= targetAlt){
      clearInterval(ascendTimer);
      root.remove(rocket);
      
      // Explosion Burst: Create 30 glowing sparks
      try { SFX.pop(); } catch(e){}
      toast(`🎆 Rocket ${rocketName} Bursting in the Sky!`);
      
      const particleGroup = new T.Group();
      particleGroup.position.set(startX, targetAlt, startZ);
      
      const particles = [];
      const pMat = new T.MeshBasicMaterial({color: colorHex});
      for(let p = 0; p < 28; p++){
        const spark = new T.Mesh(new T.SphereGeometry(0.09, 8, 8), pMat);
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.random() * Math.PI;
        const speed = 0.08 + Math.random() * 0.12;
        spark.userData = {
          vx: Math.sin(phi) * Math.cos(theta) * speed,
          vy: Math.cos(phi) * speed + 0.03,
          vz: Math.sin(phi) * Math.sin(theta) * speed
        };
        particleGroup.add(spark);
        particles.push(spark);
      }
      
      const burstLight = new T.PointLight(colorHex, 4.0, 10.0);
      particleGroup.add(burstLight);
      root.add(particleGroup);
      
      // Spark expansion & fade
      let sparkLife = 0;
      const sparkTimer = setInterval(()=>{
        sparkLife += 0.04;
        particles.forEach(sp=>{
          sp.position.x += sp.userData.vx;
          sp.position.y += sp.userData.vy;
          sp.position.z += sp.userData.vz;
          sp.userData.vy -= 0.003; // gravity
          sp.scale.multiplyScalar(0.96);
        });
        burstLight.intensity *= 0.94;
        
        if(sparkLife >= 1.2){
          clearInterval(sparkTimer);
          root.remove(particleGroup);
        }
      }, 30);
    }
  }, 30);
}"""

print(f"Replacing Chapter 13 from {pos_ch13_start} to {pos_after_ch13}...")
html = html[:pos_ch13_start] + new_ch13_code + "\n\n" + html[pos_after_ch13:]

# Write back to index.html and internet-smart-adventure.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("internet-smart-adventure.html", "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] Updated Chapter 2, Chapter 13 with 5-Rocket Celebration, and removed Chapter 14!")

# Validate all script tags with node --check
script_tags = re.findall(r'<script>([\s\S]*?)</script>', html)
print(f"Total script tags: {len(script_tags)}")

all_passed = True
for idx, code in enumerate(script_tags):
    with open(f"temp_chk_{idx}.js", "w", encoding="utf-8") as tf:
        tf.write(code)
    res = subprocess.run(["node", "--check", f"temp_chk_{idx}.js"], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[PASSED] Script {idx} is 100% valid JS")
    else:
        all_passed = False
        print(f"[FAILED] Script {idx} syntax error:")
        print(res.stderr)

if all_passed:
    print("\n[SUCCESS] ALL JAVASCRIPT IN index.html IS 100% VALID!")
