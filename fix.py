import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Fix 1: p9 syntax error and garbled text
    if "{ id: 'p9'" in line and "unit: '??" in line:
        line = "                { id: 'p9', code: '', name: '4mm 4x8 일반합판', spec: '준내수 / 4x8 (1220x2440mm)', unit: '장', price: 17500 },\n"
        
    # Fix 2: Tab buttons white-space nowrap
    if ".tab-btn {" in line:
        line = ".tab-btn {\n            white-space: nowrap;\n"
        
    # Fix 3: REFERENCES fallback (SyntaxError)
    if line.strip() == "const":
        if i + 1 < len(lines) and lines[i+1].strip() == "":
            if i + 2 < len(lines) and "refs.forEach(ref => {" in lines[i+2]:
                line = '''            let refs = [];
            const stored = localStorage.getItem("youngrim_admin_references");
            if(stored) {
                try { refs = JSON.parse(stored); } catch(e){}
            }
            if(!refs || refs.length === 0) {
                refs = [
                    { name: "KCC / 하남시 지식산업센터", spec: "KCC 석고보드 및 경량철골 자재 납품", unit: "2024.05" },
                    { name: "벽산 / 인천 검단 신도시 아파트", spec: "벽산 단열재 및 그라스울 대량 납품", unit: "2024.04" },
                    { name: "영림 / 서울 강남구 오피스 빌딩", spec: "영림 도어 및 인테리어 마감재 납품", unit: "2024.03" }
                ];
            }\n'''
                
    # Fix 4: Hero Date
    if 'window.addEventListener("DOMContentLoaded", () => {' in line:
        line += '''            const dateObj = new Date();
            const yyyy = dateObj.getFullYear();
            const mm = String(dateObj.getMonth() + 1).padStart(2, '0');
            const dd = String(dateObj.getDate()).padStart(2, '0');
            const heroDateEl = document.getElementById("heroDate");
            if(heroDateEl) heroDateEl.innerText = `${yyyy}.${mm}.${dd} 09:00 기준 완료`;\n'''

    new_lines.append(line)

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
