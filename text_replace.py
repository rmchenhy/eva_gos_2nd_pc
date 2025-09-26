import os
import json
import re

# 控制符识别正则（如 @c, @n, @12）
control_split = re.compile(r'(@[a-n]+)')

# 读取原始 JSON
with open("translation_map.json", "r", encoding="utf-8") as f:
    raw_entries = json.load(f)

fragment_entries = []

for entry in raw_entries:
    original = entry.get("original", "")
    translation = entry.get("translation", "")
    if not original or not translation:
        continue

    # 按控制符拆分
    original_parts = control_split.split(original)
    translation_parts = control_split.split(translation)

    # 对齐控制符与文本
    i = 0
    while i < len(original_parts):
        if original_parts[i].startswith("@"):
            control = original_parts[i]
            i += 1
            if i < len(original_parts):
                orig_text = original_parts[i]
                trans_text = translation_parts[i] if i < len(translation_parts) else orig_text
                fragment_entries.append({
                    "original": orig_text.strip(),
                    "translation": trans_text.strip()
                })
        else:
            orig_text = original_parts[i]
            trans_text = translation_parts[i] if i < len(translation_parts) else orig_text
            fragment_entries.append({
                "original": orig_text.strip(),
                "translation": trans_text.strip()
            })
        i += 1

# 保存为新的 JSON 映射
with open("fragment_translation_map.json", "w", encoding="utf-8") as f:
    json.dump(fragment_entries, f, ensure_ascii=False, indent=2)

print(f"✅ 已生成片段翻译映射，共 {len(fragment_entries)} 条")


# 加载片段翻译映射
with open("fragment_translation_map.json", "r", encoding="utf-8") as f:
    fragment_entries = json.load(f)

translation_map = {entry["original"]: entry["translation"] for entry in fragment_entries}

# 控制符拆分正则
control_split = re.compile(r'(@[a-n]+)')

# 引号识别正则
quote_pattern = re.compile(r'"(.*?)"')

# 设置目录
origin_folder = "exec_origin"
output_folder = "exec_cn"
os.makedirs(output_folder, exist_ok=True)

missing_fragments = []


def replace_fragments(text, filename, line_num):
    parts = control_split.split(text)
    rebuilt = []
    i = 0
    while i < len(parts):
        if parts[i].startswith("@"):
            control = parts[i]
            i += 1
            content = parts[i] if i < len(parts) else ""
            translated = translation_map.get(content.strip(), content)
            if content.strip() not in translation_map:
                missing_fragments.append({
                    "file": filename,
                    "line": line_num,
                    "fragment": content.strip()
                })
            rebuilt.append(f"{control}{translated}")
        else:
            content = parts[i]
            translated = translation_map.get(content.strip(), content)
            if content.strip() not in translation_map:
                missing_fragments.append({
                    "file": filename,
                    "line": line_num,
                    "fragment": content.strip()
                })
            rebuilt.append(translated)
        i += 1
    return ''.join(rebuilt)

# 遍历文件
for filename in os.listdir(origin_folder):
    if not filename.endswith(".txt"):
        continue

    origin_path = os.path.join(origin_folder, filename)
    output_path = os.path.join(output_folder, filename)

    with open(origin_path, "r", encoding="cp932") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_line = line
        if new_line.startswith(";") or new_line.startswith("	;"):
            new_lines.append(new_line)
            continue
        matches = quote_pattern.findall(line)
        for quoted in matches:
            if quoted.startswith("M"):
                continue
            replaced = replace_fragments(quoted, filename, lines.index(line) + 1)
            new_line = new_line.replace(f'"{quoted}"', f'"{replaced}"')
        new_lines.append(new_line)

    with open(output_path, "w", encoding="gbk", errors="ignore") as f:
        f.writelines(new_lines)

print(f"\n✅ 所有文本替换完成。")
if missing_fragments:
    print(f"\n📝 未匹配片段报告（共 {len(missing_fragments)} 条）：")
    for entry in missing_fragments:
        print(f"{entry['file']} (第 {entry['line']} 行): {entry['fragment']}")
else:
    print("\n🎉 所有片段均已成功匹配翻译。")