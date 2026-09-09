with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos_ch2 = text.find("CHAPTER 02")
pos_ch3 = text.find("CHAPTER 03")
ch2 = text[pos_ch2:pos_ch3]

with open("curr_ch2.js", "w", encoding="utf-8") as f:
    f.write(ch2)
print("Saved curr_ch2.js")

pos_ch13 = text.find("CHAPTER 13")
pos_ch14 = text.find("CHAPTER 14")
if pos_ch14 == -1:
    pos_ch14 = text.find("CHAPTER REGISTRATION", pos_ch13)
ch13 = text[pos_ch13:pos_ch14]

with open("curr_ch13.js", "w", encoding="utf-8") as f:
    f.write(ch13)
print("Saved curr_ch13.js")

# Check if Chapter 14 is present
if "CHAPTER 14" in text:
    print("Chapter 14 IS present in index.html - needs to be removed!")
else:
    print("Chapter 14 is NOT present in index.html")
