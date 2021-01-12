from flask import Flask, request, make_response, Response, jsonify
from utils import Xxkol
import os, time
from flask_cors import CORS
import json

app = Flask(__name__)
app.config.from_object({'CORS_ORIGIN_ALLOW_ALL': True})
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
userCount = {
    'phone': "xxx",  # 用户名 需注册
    'password': "xxx"  # 密码
}
x = Xxkol(userCount)


@app.route("/query/userinfo", methods=["POST"])
def getUserInfo():
    try:
        headers = {
            'content-type': 'application/json'
        }
        mid = request.form.get("mid")
        mid = str(mid)
        isNum = mid.isnumeric()
        if (isNum == False):  # 是否为数字
            return make_response(jsonify({'status': 100, 'data': "param fail!"}), headers)
        path = 'public/' + mid + '/u.json'
        isExist = os.path.exists('public/' + mid)
        if (isExist == False):  # 是否存在文件 若不存在则创建路径
            os.mkdir('public/' + mid)
            navNum = x.getUserInfo(mid)
            print(navNum)
            with open(path, 'w') as file:
                file.write(navNum)
        # 如果存在文件，则返回文件文本
        if os.path.isfile(path):
            fileInfo = os.stat(path)  # 获取文件信息
            fileTime = fileInfo.st_mtime
            nowTime = time.time()
            if nowTime - fileTime < 86400:  # 如果小于1天 则返回现在的文件
                with open(path) as file:
                    print("获取userInfo成功")
                    return make_response(jsonify({'status': 200, 'data': json.loads(file.read())}), headers)
        navNum = x.getUserInfo(mid)
        with open(path, 'w') as file:
            file.write(navNum)
        print("获取userInfo成功")
        return make_response(jsonify({'status': 200, 'data': json.loads(navNum)}), headers)
    except:
        return make_response(jsonify({'status': 404, 'data': "搜索的人不在名单上哦，换个值搜索试试？"}), headers)


@app.route("/query/numInfo", methods=["POST"])
def getNumInfo():
    try:
        headers = {
            'content-type': 'application/json'
        }
        mid = request.form.get("mid")
        mid = str(mid)
        isNum = mid.isnumeric()
        if (isNum == False):  # 是否为数字
            return make_response(jsonify({'status': 100, 'data': "param fail!"}), headers)
        path = 'public/' + mid + '/n.json'
        isExist = os.path.exists('public/' + mid)
        if (isExist == False):  # 是否存在文件 若不存在则创建路径
            os.mkdir('public/' + mid)
            navNum = x.getNavNum(mid)
            print(navNum)
            with open(path, 'w') as file:
                file.write(navNum)
        # 如果存在文件，则返回文件文本
        if os.path.isfile(path):
            fileInfo = os.stat(path)  # 获取文件信息
            fileTime = fileInfo.st_mtime
            nowTime = time.time()
            if nowTime - fileTime < 86400:  # 如果小于1天 则返回现在的文件
                with open(path) as file:
                    print("获取numInfo成功")
                    return make_response(jsonify({'status': 200, 'data': json.loads(file.read())}), headers)
        # 若上述状况都不存在，则重新爬取
        navNum = x.getNavNum(mid)
        with open(path, 'w') as file:
            file.write(navNum)
        print("获取numInfo成功")

        return make_response(jsonify({'status': 200, 'data': json.loads(navNum)}), headers)

    except:
        return make_response(jsonify({'status': 404, 'data': "搜索的人不在名单上哦，换个值搜索试试？"}), headers)


@app.route("/query/typeInfo", methods=["POST"])
def getTypeInfo():
    try:
        headers = {
            'content-type': 'application/json'
        }
        mid = request.form.get("mid")
        mid = str(mid)
        path = 'public/' + mid + '/t.json'  # 文件路径
        isNum = mid.isnumeric()
        if (isNum == False):  # 是否为数字
            return make_response(jsonify({'status': 100, 'data': "param fail!"}), headers)

        isExist = os.path.exists('public/' + mid)
        if (isExist == False):  # 是否存在文件 若不存在则创建路径
            os.mkdir('public/' + mid)
            typeInfo = x.getTypeInfo(mid)
            print(typeInfo)
            with open(path, 'w') as file:
                file.write(typeInfo)
        # 如果存在文件，则返回文件文本
        if os.path.isfile(path):
            fileInfo = os.stat(path)  # 获取文件信息
            fileTime = fileInfo.st_mtime
            nowTime = time.time()
            if nowTime - fileTime < 86400:  # 如果小于1天 则返回现在的文件
                with open(path) as file:
                    print("获取typeInfo成功")
                    return make_response(jsonify({'status': 200, 'data': json.loads(file.read())}), headers)
        # 若上述状况都不存在，则重新爬取
        typeInfo = x.getTypeInfo(mid)
        with open(path, 'w') as file:
            file.write(typeInfo)
        print("获取typeInfo成功")

        return make_response(jsonify({'status': 200, 'data': json.loads(typeInfo)}), headers)
    except:
        return make_response(jsonify({'status': 404, 'data': "搜索的人不在名单上哦，换个值搜索试试？"}), headers)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2020)
