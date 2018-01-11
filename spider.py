import requests
from requests import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def pares_one_page(html):
    news=re.compile('<dd>.*?board-index.*?>(\d+)</i>'+
                    '.*?data-src=(.*?)alt'+
                    '.*?movie-item-info.*?title=(.*?)data-act'+
                    '.*?star.*?>(.*?)</p>'+
                    '.*?releasetime.*?>(.*?)</p>'+
                    '.*?integer.*?>(.*?)</i>.*?>(\d+)</i>.*?</dd>',re.S)
    results=re.findall(news,html)
    for result in results:
        print(type(result))  #元组
        yield {
            'sort':result[0],
            'img':result[1],
            'title':result[2],
            'actor':result[3].strip()[3:],#去掉前后换行符，从第三个元素开始截取
            'time':result[4].strip()[5:],
            'score':result[5]+result[6]
        }

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        #将字典转换为字符串，ensure-ascii=False让其以utf-8输出
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()



def main(offset):
    url='http://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    for item in pares_one_page(html):  #用for方法调用那个生成器
        print(item)
        write_to_file(item)



if __name__=='__main__':
    #构建进程池
    pool=Pool()
    pool.map(main,[i*10 for i in range(10)]) #后面是构造一个数组

