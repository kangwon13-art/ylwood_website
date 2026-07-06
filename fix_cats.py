import sys

path = r"c:\Users\1\Desktop\영림\영림우드 자료\영림 사이트 폴더\index.html"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")
changed = []
for i, line in enumerate(lines):
    # Fix 1 & 2: category card names
    if "목재<br>구조재" in line:
        line = line.replace("목재<br>구조재", "목재/구조재")
        changed.append(f"Line {i+1}: 목재<br>구조재 -> 목재/구조재")
    if "방부목<br>특수목" in line:
        line = line.replace("방부목<br>특수목", "방부목/특수목/합성목")
        changed.append(f"Line {i+1}: 방부목<br>특수목 -> 방부목/특수목/합성목")
    if "철물<br>부자재" in line:
        line = line.replace("철물<br>부자재", "철물/부자재")
        changed.append(f"Line {i+1}: 철물<br>부자재 -> 철물/부자재")
    lines[i] = line

# Fix 3: Insert 루바/집성판 card after deck_timber card (after the closing </div> of deck_timber)
# Find the line index of "<!-- 9. 철물/부자재 -->"
deck_end_idx = -1
for i, line in enumerate(lines):
    if "<!-- 9. 철물" in line or ("category-card" in line and "hardware" in line):
        deck_end_idx = i
        break

# Actually find "<!-- 8. 방부목" and then find the next card's start
bang_idx = -1
for i, line in enumerate(lines):
    if "<!-- 8." in line and "방부목" in line:
        bang_idx = i
        break

# From bang_idx, find the closing </div> of the card (4 levels deep)
insert_after = -1
depth = 0
for i in range(bang_idx, len(lines)):
    if "<div" in lines[i]:
        depth += lines[i].count("<div") - lines[i].count("</div")
    elif "</div>" in lines[i]:
        depth -= lines[i].count("</div>") - lines[i].count("<div")
    if depth == 0 and i > bang_idx:
        insert_after = i
        break

print(f"Inserting after line {insert_after+1}: {lines[insert_after].strip()}")

new_card = [
    "                <!-- 8.5. 루바/집성판 -->",
    "                <div class=\"category-card\" onclick=\"selectCategoryAndScroll('louver_wood')\">",
    "                    <div class=\"category-icon-wrap\">",
    "                        <svg viewBox=\"0 0 24 24\">",
    "                            <path d=\"M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z\" />",
    "                        </svg>",
    "                    </div>",
    "                    <div class=\"category-card-body\">",
    "                        <h3 class=\"category-name\">루바/집성판</h3>",
    "                        <p class=\"category-description\">루바, 집성판, 각종 폭판 등 인테리어 마감 및 목공 전용 목재 자재 전문 공급.</p>",
    "                    </div>",
    "                    <div class=\"category-footer-link\">",
    "                        단가 확인 및 견적 산출",
    "                        <svg viewBox=\"0 0 24 24\">",
    "                            <path d=\"M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z\" />",
    "                        </svg>",
    "                    </div>",
    "                </div>",
]

lines = lines[:insert_after+1] + new_card + lines[insert_after+1:]

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(lines))

print("Changes:")
for c in changed:
    print(c)
print(f"루바/집성판 card inserted after line {insert_after+1}")
print("Done")
