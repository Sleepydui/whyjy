from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import datetime
import os

app = Flask(__name__)
CORS(app)

# 获取当前脚本的绝对路径
current_script_path = os.path.dirname(os.path.abspath(__file__))
# 图片文件夹的相对路径，相对于当前脚本
image_base_path = os.path.join(current_script_path, "images") # 或者 "data/images",

@app.route('/get-image', methods=['GET'])
def get_image():
    print(request.args)
    # 获取参数date
    date = request.args.get('date')
    # 获取版面号，默认为1
    page = int(request.args.get('page', 1))
    # 转化成年月日
    date = datetime.datetime.strptime(date, r"%Y-%m-%d")
    year = date.year
    month = date.month
    day = date.day

    # 转字符串
    year = str(year)
    month = str(month) if month >= 10 else "0" + str(month)
    day = str(day) if day >= 10 else "0" + str(day)
    page = str(page) if page >= 10 else "0" + str(page)

    # 生成图片地址
    # 确保这里的路径拼接逻辑与你的图片存储结构一致
    # 比如如果图片直接在 images/20240101.jpg，则改为:
    # path = os.path.join(image_base_path, "%s%s%s%s.jpg" % (year, month, day, page))
    path = os.path.join(image_base_path, "%s"%(year), "%s%s%s.jpg"%(year, month, day))


    # 检查文件是否存在
    if not os.path.exists(path):
        # 404
        return jsonify({"error": "file not found"}), 404 
    # 以图片格式返回
    return send_file(path, mimetype='image/jpeg')
    

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=14563)