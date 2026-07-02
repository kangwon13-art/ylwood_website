import re, sys

def modify_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # TASK 1: Font Sizes (Only applies to index.html CSS and template string)
    if 'index.html' in filepath:
        content = content.replace(
            '.hero-desc {\n            font-size: 18px;',
            '.hero-desc {\n            font-size: 20px;'
        )
        content = content.replace(
            '.section-desc {\n            font-size: 16px;',
            '.section-desc {\n            font-size: 18px;'
        )
        content = content.replace(
            '.category-description {\n            font-size: 14px;',
            '.category-description {\n            font-size: 16px;'
        )
        content = content.replace(
            '.faq-content {\n            padding: 0 24px 24px 44px;\n            font-size: 14px;\n            color: var(--color-text-muted);\n            line-height: 1.7;',
            '.faq-content {\n            padding: 0 24px 24px 44px;\n            font-size: 16px;\n            color: var(--color-text-muted);\n            line-height: 1.8;'
        )
        content = content.replace(
            'footer {\n            background-color: #050811;\n            padding: 60px 0 100px;\n            border-top: 1px solid var(--color-border);\n            font-size: 13px;',
            'footer {\n            background-color: #050811;\n            padding: 60px 0 100px;\n            border-top: 1px solid var(--color-border);\n            font-size: 14px;'
        )
        content = content.replace(
            '.footer-details {\n            line-height: 1.8;\n        }',
            '.footer-details {\n            font-size: 14px;\n            line-height: 1.8;\n        }'
        )
        content = content.replace(
            '.price-table td {\n            padding: 16px;\n            border-bottom: 1px solid var(--color-border);\n            font-size: 14px;',
            '.price-table td {\n            padding: 16px;\n            border-bottom: 1px solid var(--color-border);\n            font-size: 15px;'
        )
        content = content.replace(
            '.prod-spec {\n            font-size: 12px;',
            '.prod-spec {\n            font-size: 14px;'
        )
        content = content.replace(
            '<span class="prod-spec" style="font-size:13px; color: var(--color-text-muted);">${item.spec}</span>',
            '<span class="prod-spec" style="font-size:14px; color: var(--color-text-muted);">${item.spec}</span>'
        )

    # TASKS 2 & 3: Array parsing and modification
    # Parse hardware array
    hw_match = re.search(r'hardware:\s*\[([\s\S]*?)\]', content)
    if hw_match:
        hw_str = hw_match.group(1)
        # Parse items
        items = re.findall(r'(\{\s*id:\s*\'(.*?)\',\s*code:\s*\'.*?\',\s*name:\s*\'.*?\',\s*spec:\s*\'(.*?)\',\s*unit:\s*\'.*?\',\s*price:\s*\d+(?:,\s*sub:\s*\'.*?\')?\s*\})', hw_str)
        
        # 3-1: Update spec to '-' unless in exception list
        hw_dict = {}
        for item_full, item_id, item_spec in items:
            num = -1
            if item_id.startswith('h'):
                try:
                    num = int(item_id[1:])
                except:
                    pass
            keep_spec = False
            if 23 <= num <= 32: keep_spec = True
            elif 59 <= num <= 64: keep_spec = True
            elif 89 <= num <= 102: keep_spec = True
            elif num == 107: keep_spec = True
            elif 108 <= num <= 110: keep_spec = True
            
            if not keep_spec:
                item_full = item_full.replace(f"spec: '{item_spec}'", "spec: '-'")
            hw_dict[item_id] = item_full

        # 3-2 & 3-3: Reorder and remove h88
        new_hw_list = []
        for i_id in ['h4', 'h5', 'h1', 'h2', 'h3', 'h6']:
            if i_id in hw_dict:
                new_hw_list.append(hw_dict[i_id])
                del hw_dict[i_id]
        
        # Add remaining elements in original order, except h88
        for item_full, item_id, _ in items:
            if item_id in hw_dict and item_id != 'h88':
                new_hw_list.append(hw_dict[item_id])
                del hw_dict[item_id]

        new_hw_str = ",\n                    ".join(new_hw_list)
        # ensure proper indent based on file
        indent = "                    " if "index" in filepath else "                    "
        if "admin.html" in filepath: indent = "                    "
        
        content = content[:hw_match.start(1)] + "\n                    " + new_hw_str + "\n                " + content[hw_match.end(1):]

    # Parse insulation array
    ins_match = re.search(r'insulation:\s*\[([\s\S]*?)\]', content)
    if ins_match:
        ins_str = ins_match.group(1)
        items = re.findall(r'(\{\s*id:\s*\'(.*?)\',\s*code:\s*\'.*?\',\s*name:\s*\'.*?\',\s*spec:\s*\'(.*?)\',\s*unit:\s*\'.*?\',\s*price:\s*\d+(?:,\s*sub:\s*\'.*?\')?\s*\})', ins_str)
        ins_dict = {item_id: item_full for item_full, item_id, _ in items}
        
        # Note: h88 was in hardware originally. Let's create it or fetch from original
        if 'h88' not in ins_dict:
            ins_dict['h88'] = "{ id: 'h88', code: '', name: '충진재 50T', spec: '50x450x1000mm', unit: '개', price: 2000 }"

        # Order specified: i3, i4, i7, i8, i9, i15, i16, i17, i18, i11, i12, i13, i14, i1, i2, i10, h88
        ins_order = ['i3', 'i4', 'i7', 'i8', 'i9', 'i15', 'i16', 'i17', 'i18', 'i11', 'i12', 'i13', 'i14', 'i1', 'i2', 'i10', 'h88']
        
        new_ins_list = []
        for i_id in ins_order:
            if i_id in ins_dict:
                new_ins_list.append(ins_dict[i_id])
                
        new_ins_str = ",\n                    ".join(new_ins_list)
        content = content[:ins_match.start(1)] + "\n                    " + new_ins_str + "\n                " + content[ins_match.end(1):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

modify_html('C:/Users/1/Desktop/영림/영림우드 자료/영림 사이트 폴더/index.html')
modify_html('C:/Users/1/Desktop/영림/영림우드 자료/영림 사이트 폴더/admin.html')
print('Done!')
