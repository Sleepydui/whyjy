import json
import os

# 将name属性重命名为title
def rename_name2title(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for datum in data:
        datum["title"] = datum["name"]
        del datum["name"]
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def replace_xy_with_coordinates(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for datum in data:
        if "x_coord" in datum:
            datum["coordinates"] = {"x": datum["x_coord"], "y": datum["y_coord"]}
            del datum["x_coord"]
            del datum["y_coord"]
        if "tsne_x" in datum:
            datum["text_embedding"] = {"x": datum["tsne_x"], "y": datum["tsne_y"]}
            del datum["tsne_x"]
            del datum["tsne_y"]
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def correct_time(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for datum in data:
        if "time" in datum:
            for time in datum["time"]:
                if time["month"] == 0:
                    time["month"] = 1
                if time["day"] == 0:
                    time["day"] = 1
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def aggregate_coords(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    coords_key = ["text_embedding","time_embedding"]
    for datum in data:
        aggregated_coords = []
        for key in coords_key:
            if key in datum:
                aggregated_coords.append({
                    "name": key,
                    "coords": datum[key]
                })
                del datum[key]
        datum["embedding"] = aggregated_coords
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def extract_topics(data_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 获取数据的文件名
    data_name = os.path.basename(data_path).split(".")[0]
    dir_name = os.path.dirname(data_path)
    # 创建一个以数据文件名为名字的文件夹
    save_dir = os.path.join(dir_name, data_name)
    os.makedirs(save_dir, exist_ok=True)
    # 统计数据中的所有主题
    topics = dict()
    for datum in data:
        if "topic" in datum:
            topics[datum["topic"]] = topics.get(datum["topic"], 0) + 1
    topics = sorted(topics.keys(), key=lambda x: topics[x], reverse=True)
    topics = [str(topic) for topic in topics]
    # 将每条数据的主题转换为主题的索引
    for datum in data:
        if "topic" in datum:
            datum["topic"] = topics.index(datum["topic"])
    # 保存主题数据
    topic_path = os.path.join(save_dir, "topics.json")
    data_path = os.path.join(save_dir, "data.json")
    with open(topic_path, "w", encoding="utf-8") as f:
        json.dump([{"name":topic}for topic in topics], f, ensure_ascii=False, indent=4)
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    extract_topics(r"D:\Code\HisVA\frontend\public\data.json")
    extract_topics(r"D:\Code\HisVA\frontend\public\people_data.json")
    extract_topics(r"D:\Code\HisVA\frontend\public\wiki_data.json")
    extract_topics(r"D:\Code\HisVA\frontend\public\comments_zhuozhengyuan_data.json")
    extract_topics(r"D:\Code\HisVA\frontend\public\comments_data.json")

