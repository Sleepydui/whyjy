import json
from itertools import combinations
from collections import defaultdict
from tqdm import tqdm

# 读取数据
with open('data.json', 'r', encoding='utf-8') as f:
    news_data = json.load(f)

with open('categorized_keywords.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

# Step 1: 从 categorized_keywords.json 创建节点集（去重）+ 加分类
# 这一步现在是核心，定义了所有的节点
keyword_to_category = {}
nodes = {} # 直接初始化 nodes 字典

for cat, words in categories.items():
    for word in words:
        if word not in nodes: # 确保关键词唯一
            nodes[word] = {
                'id': word,
                'category': cat # 直接使用其分类
            }
        keyword_to_category[word] = cat # 用于后续快速查找关键词的分类

# Step 2: 遍历 data.json，创建边（共现）
# 现在只计算 categorized_keywords.json 中存在的关键词之间的共现
edges = []
edge_counter = defaultdict(int)

for article in tqdm(xiaomicar, desc="Counting co-occurrences"):
    # 检查 article['keywords'] 是否存在且是字符串类型
    if 'keywords' in article and isinstance(article['keywords'], str):
        # 将关键词字符串按空格分割成列表
        article_keywords_raw = article['keywords'].split(' ')
    else:
        article_keywords_raw = []

    # 过滤文章中的关键词，只保留在 categorized_keywords.json 中存在的关键词
    # 使用 set 可以提高查找效率，并自动去重
    relevant_keywords_in_article = [
        kw for kw in article_keywords_raw if kw in keyword_to_category
    ]

    # 只有当文章中存在至少两个相关关键词时才计算组合
    if len(relevant_keywords_in_article) >= 2:
        for kw1, kw2 in combinations(set(relevant_keywords_in_article), 2):
            pair = tuple(sorted([kw1, kw2]))
            edge_counter[pair] += 1

# 生成边列表（可加权）
for (kw1, kw2), weight in edge_counter.items():
    edges.append({
        'source': kw1,
        'target': kw2,
        'weight': weight
    })

# 保存为 JSON 用于前端绘图（如用 D3.js）
with open('graph_nodes.json', 'w', encoding='utf-8') as f:
    json.dump(list(nodes.values()), f, ensure_ascii=False, indent=2)

with open('graph_edges.json', 'w', encoding='utf-8') as f:
    json.dump(edges, f, ensure_ascii=False, indent=2)