import requests
import json


class Xxkol():

    def __init__(self, userCount):
        self.userCount = userCount
        self.userInfo = None
        self.loginInfo = None
        self.userData = None
        self.authorization = None
        # self.phone = ""
        # self.password = ""
        # userInfo['phone'] = self.phone
        # userInfo['password'] = self.password
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'accept': 'application/json,text/plain,*/*',
            'content-type': 'application/json',
            'origin': 'https://xxkol.cn',
            'referer': 'https://xxkol.cn/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }
        self.login()

    def login(self):
        '''
        登录操作，获取Token
        :return: 返回自身登录的用户信息dict
        '''
        url = "https://xxkol.cn/api/login"
        param = self.userCount
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'accept': 'application/json,text/plain,*/*',
            'content-type': 'application/json',
            'origin': 'https://xxkol.cn',
            'referer': 'https://xxkol.cn/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }
        res = requests.post(url=url, data=json.dumps(param), headers=headers)
        res.encoding = "utf-8"

        self.loginInfo = res.json()
        if self.loginInfo['code'] == 200:
            self.userInfo = self.loginInfo['data']['info']
            self.authorization = self.loginInfo['data']['jwt']
            headers['cookie'] = "xxToken=" + self.loginInfo['data']['jwt']
            headers['authorization'] = self.loginInfo['data']['jwt']
            self.headers['cookie'] = "xxToken=" + self.loginInfo['data']['jwt']
            self.headers['authorization'] = self.loginInfo['data']['jwt']
            print("登录成功！")
            self.__getIds()
            self.__getGroup()
        return self.userInfo

    def __getIds(self):
        '''
        模拟用户访问
        :return: True or False
        '''
        url = "https://xxkol.cn/api/ids"
        res = requests.get(url, headers=self.headers)
        res.encoding = "utf-8"
        r = res.json()
        if r['code'] == 200:
            print('访问ids成功')
        return r['code'] == 200

    def __getGroup(self):
        '''
        模拟用户访问
        :return: True or False
        '''
        url = "https://xxkol.cn/api/group"
        res = requests.get(url, headers=self.headers)
        res.encoding = "utf-8"
        r = res.json()
        if r['code'] == 200:
            print('访问group成功')
        return r['code'] == 200

    def getUserInfo(self, mid):
        '''
        爬取指定用户的信息
        :param mid: b站用户的mid(int or string)
        :return:返回用户数据的json字符串
        '''
        url = "https://xxkol.cn/api/kinfo?mid=" + str(mid)
        headers = self.headers
        headers['referer'] = 'https://xxkol.cn/kol'
        headers['sec-fetch-dest'] = 'document'
        headers['sec-fetch-mode'] = 'navigate'
        headers['sec-fetch-site'] = 'same-origin'
        headers['sec-fetch-user'] = '?1'
        headers['upgrade-insecure-requests'] = '1'
        # self.headers['referer'] = 'https://xxkol.cn/kol'
        # self.headers['sec-fetch-dest'] = 'document'
        # self.headers['sec-fetch-mode'] = 'navigate'
        # self.headers['sec-fetch-site'] = 'same-origin'
        # self.headers['sec-fetch-user'] = '?1'
        # self.headers['upgrade-insecure-requests'] = '1'
        res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"
        # print(res.text)
        r = res.json()
        if r['code'] == 200:
            self.userData = r['data']
            return json.dumps(r['data'])
        else:
            print("获取指定用户userInfo数据异常")
            return "error"

    def getNavNum(self, mid):
        url = "https://xxkol.cn/refxx/x/space/navnum?mid=" + str(mid) + "&jsonp=jsonp&callback="
        headers = self.headers
        headers['referer'] = 'https://xxkol.cn/kol/kolinfo/' + str(mid)
        headers['sec-fetch-dest'] = 'empty'
        headers['sec-fetch-mode'] = 'cors'
        headers['sec-fetch-site'] = 'same-origin'
        headers['origin'] = ""
        headers.pop('origin')
        res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"
        r = res.json()
        if r['code'] == 0:
            return json.dumps(r['data'])
        else:
            print("获取指定用户navNumInfo数据异常")
            return "error"

    def getTypeInfo(self, mid):
        url = "https://xxkol.cn/xx/x/space/arc/search?mid=" + str(mid) + "&ps=1"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66"
        }
        res = requests.get(url=url, headers=headers)
        res.encoding = "utf-8"
        print(res.text)
        r = res.json()
        if r['code'] == 0:
            self.userData = r['data']
            return json.dumps(r['data']['list'])
        else:
            print("获取指定用户typeInfo数据异常")
            return "error"


if __name__ == '__main__':
    userCount = {
        'phone': "xxx",
        'password': "xxx"
    }
    x = Xxkol(userCount)
    infoJson = x.getUserInfo(3766866)
    NavNumInfo = x.getNavNum(3766866)
    TypeInfo = x.getTypeInfo(3766866)
    print(TypeInfo)
    # if infoJson != "error":
    #     with open('userInfo.json', 'w') as file:
    #         file.write(infoJson)
    #         print("写入userInfo.json文件成功！")
    # if NavNumInfo != "error":
    #     with open('navNumInfo.json', 'w') as file:
    #         file.write(NavNumInfo)
    #         print("navNumInfo.json文件成功！")
    #
    # else:
    #     print("获取信息失败！")
