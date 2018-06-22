import urllib.request
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud
import jieba, codecs
from collections import Counter

import numpy as np
from snownlp import SnowNLP
import matplotlib.pyplot as plt
 
 
if __name__=='__main__':
    
    #极简模式
    import urllib.request
    response = urllib.request.urlopen('http://finance.sina.com.cn/blog/7.html')
    buff = response.read()
    html = buff.decode("gbk")
        
    #增加参数， 模拟浏览器行为
    '''        
    url = 'http://finance.sina.com.cn/blog/7.html'
    values = {'name': 'voidking','language': 'Python'}
    data = urllib.parse.urlencode(values).encode(encoding='gb2312',errors='ignore')
    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0' }
    request = urllib.request.Request(url=url, data=data,headers=headers,method='GET')
    response = urllib.request.urlopen(request)
    buff = response.read()
    html = buff.decode("gbk")
    '''
    
    soup = BeautifulSoup(html, "lxml")
    #print(soup.prettify())
    
    links = soup.find_all('a', href=re.compile(r'/blog.sina.com.cn/s/blog'))
    comment_file = open("comment.txt",'w+', encoding = 'utf-8')
    for link in links:
        new_url = link['href']
        
        #new_full_url = urljoin(page_url, new_url)
        #print(new_url)
        print(link.get_text())
        comment_file.write(link.get_text() + "\n")  
    
    print(soup.find('a'))
    comment_file.close()
    
    text = codecs.open('comment.txt', 'r', encoding = 'utf-8').read()
    text_jieba = list(jieba.cut(text))
    c = Counter(text_jieba)  # 计数
    word = c.most_common(100)  # 取前100
	
    bg_pic = imread('heart.jpg')
    wc = WordCloud(
			font_path = 'C:\Windows\Fonts\simfang.ttf',  # 指定中文字体
			background_color = 'white',  # 设置背景颜色
			max_words = 200,  # 设置最大显示的字数
			mask = bg_pic,  # 设置背景图片
			max_font_size = 150,  # 设置字体最大值
			random_state = 20  # 设置多少种随机状态，即多少种配色
		)
    wc.generate_from_frequencies(dict(word))  # 生成词云
	 
    ''' 
    plt.figure()
    plt.imshow(wc)
    plt.axis('off')
    plt.show
    '''
    wc.to_file('heart.png')  
 
    f = open('comment.txt', 'r', encoding = 'utf-8')
    list = f.readlines()
    sentimentslist = []
    
    for i in list:
        s = SnowNLP(i)
        # print s.sentiments
        sentimentslist.append(s.sentiments)
    plt.hist(sentimentslist, bins = np.arange(0, 1, 0.01), facecolor = 'g')
    plt.xlabel('Sentiments Probability')
    plt.ylabel('Quantity')
    plt.title('Analysis of Sentiments')
    #plt.show()
    plt.savefig("sentiments.png")    