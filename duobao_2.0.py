import time
import requests
import  re
#1. 粘贴产品ID
#2. 输入预期价格  时间剩余2秒时 且  低于预期价格 开始加价
#3 输入cookie
ID = '产品id'    #产品id
my_price = 40           #预期价格
y = 2                   #加价幅度
s = 2                 #等待刷新时间

c = 'Cookie 粘贴在这'
#设置上面即可


HEADERS = {
    'Referer':'https://paipai.jd.com/auction-detail/113158389',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Cookie':'coo'
}
HEADERS['Cookie'] = c
url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'


#获取当前价格&剩余时间
def get_pricetime():
    r_url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'
    r = requests.get(r_url,headers=HEADERS)
    p_url = 'https://used-api.jd.com/auctionRecord/getCurrentAndOfferNum?auctionId=' + ID +'&callback=__jp17'
    p = requests.get(p_url,headers=HEADERS)
    cur_price = re.findall(r"currentPrice\":(.+?),",p.text)
    c_time = re.findall(r"currentTime\":\"(.+?)\"",r.text)
    e_time = re.findall(r"endTime\":(.+?),",r.text)
    cur_price = ''.join(cur_price)
    c_time = ''.join(c_time)
    e_time = ''.join(e_time)
    c_time = (float(e_time) - float(c_time))/1000   #计算剩余时间并换算成秒
    name = re.findall(r"model\":\"(.+?)\",",r.text)
    coloer = re.findall(r"quality\":\"(.+?)\",",r.text)
    print(name + coloer ,end='')
    return cur_price,str(c_time)
#下单

def buy(price):
    # price = int(price)
    # buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice?auctionId='+ ID + '&price='+ str(price)  +'&callback=__jp24'
    # bib = requests.get(buy_url,headers=HEADERS)
    # print(bib.text)
    buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice'
    data = {
        'trackId': '3b154f3a78a78f8b6c2eea5a3cee5674',
        'eid': 'UTT4AVFUIZFVD6KGHHJRAGEEGFJ4MWFSOPDUEF7KBEHDA5ODK3GKDKP5PCVTWIAQ32N2ZT2AR5YBAH3T27354OAI3Q',
             
    }
    data['price'] = str(int(price))
    data['auctionId'] = str(ID)
    #print(data)
    resp = requests.post(buy_url,headers=HEADERS,data=data)
    print(resp.json())

try:
    while True:
        p = get_pricetime()
        print('编号:'+ID + ',当前的价格是:' + p[0] + '剩余时间' + p[1] + ',预期价格:' + str(my_price) )
        x = p[0]
        x = float(x)
        tt = p[1]
        tt = float(tt)
        if  x <= my_price  and tt <= 1:
            print('开始加价: 加价金额为' + str(x + y))
            buy(x + y)
        if tt < 6 and s != 0.0002:
            s = 0.0002
            print('开始加速 ' + str(s))
        time.sleep(s)    #等待刷新时间
        if tt < -1 or x > my_price :
            print('程序结束')
            break
except KeyboardInterrupt:
    print('已停止')
