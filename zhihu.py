
import requests
from bs4 import BeautifulSoup

url = 'http://www.zhihu.com'
login_url = 'http://www.zhihu.com/login/email'

header = {'Host': 'www.zhihu.com',
          'Connection': 'keep-alive',
          # 'Content-Length':'100', 这个不注释就会报错，还不知道原因
           'Accept':'*/*',
           'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Referer': 'https://www.zhihu.com/',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           # ' Accept':'*/*',这个不注释就会报错，还不知道原因
           'Origin':'https://www.zhihu.com',
           'X-Requested-With':'XMLHttpRequest'
          }

s = requests.session() #session 会话对象可跨请求保持某些参数，也会在同一个Session实例发出的所有请求之间保持cookies
r= s.get(url,headers = header)  #这里必须是url里的xsrf
soup = BeautifulSoup(r.text,'lxml')
body =soup.select('input[name="_xsrf"]')[0]
xsrf=body.get('value')
print(xsrf)

data={
    'email':'####',
    'password':'####',
    '_xsrf':xsrf,
    'remember_me':'true'
}

login = s.post(login_url,headers = header, data = data)  #登陆的时候用到的xsrf必须为url里的xsrf,而不是login_url里的xsrf,否则就被403
print(login)  #<Response [200]>  成功
my_cookie = login.cookies
print(my_cookie)

test = 'https://www.zhihu.com/people/qing-nan-51-71'
t = s.get(test,headers = header,cookies = my_cookie)#测试，用post登陆得到的cookies，是可以打开知乎用户的界面了
print(t.text)
