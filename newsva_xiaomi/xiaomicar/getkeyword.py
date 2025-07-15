import json

def process_keywords_in_json(file_path):
    """
    读取JSON文件，将'keywords'字段的字符串按空格拆分成列表，
    然后将修改后的数据写回文件。

    Args:
        file_path (str): JSON文件的路径。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 未找到。")
        return
    except json.JSONDecodeError:
        print(f"错误：无法解析文件 '{file_path}'，请检查JSON格式。")
        return

    modified_count = 0
    for item in data:
        if "keywords" in item and isinstance(item["keywords"], str):
            # 将字符串按空格拆分成列表
            item["keywords"] = item["keywords"].split(' ')
            modified_count += 1
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"成功处理并更新了 {modified_count} 条数据的 'keywords' 字段。")
        print(f"文件 '{file_path}' 已成功修改。")
    except IOError as e:
        print(f"错误：写入文件 '{file_path}' 时发生问题：{e}")

# 假设你的JSON文件名为 data.json
json_file_path = 'data.json'
process_keywords_in_json(json_file_path)