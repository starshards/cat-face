import urllib
import time
import os

img_src = 'http://cdn.file.yirimao.com/cat-daily-sign/%E4%B8%AD%E5%8D%8E%E6%B0%94%E6%AD%BB%E7%8C%AB.png'

t = str(int(time.time()))
filename = t+'.jpg'
basepath = os.path.dirname(__file__)
path = basepath + '/pic/' + filename
urllib.urlretrieve(img_src, path)