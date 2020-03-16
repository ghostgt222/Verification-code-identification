from PIL import Image
import time
import os,sys
import math
os.chdir(sys.path[0])

# 向量空间搜索引擎
class VectorCompare:
    # 计算矢量大小
    def magnitude(self,vector):
        total = 0
        for _,count in vector.items():
            total += count ** 2
        return math.sqrt(total)
    # 计算矢量之间的 cos 值
    def relation(self,vector1, vector2):
        topvalue = 0
        for word, count in vector1.items():
            if word in vector2.keys():
                topvalue += count * vector2[word]
        return topvalue / (self.magnitude(vector1) * self.magnitude(vector2)) # cos=a*b/(|a|*|b|)

# 将图片转换为矢量
def buildvector(im):
    dic = {}
    for count,i in enumerate(im.getdata()):
        dic[count] = i
    return dic

# 加载训练集
iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
imageset = []
for letter in iconset:
    for img in os.listdir('./iconset/{}/'.format(letter)):
        temp = buildvector(Image.open("./iconset/{}/{}".format(letter,img)))
        imageset.append({letter:temp})


im = Image.open("captcha.gif")
im2 = Image.new("P",im.size,255)
im.convert("P") # 将图片转换为8位像素模式
temp = {}

for x in range(im.size[0]):
    for y in range(im.size[1]):
        pix = im.getpixel((x,y))
        temp[pix] = pix
        if pix == 220 or pix == 227: # these are the numbers to get
            im2.putpixel((x,y),0)

# 得到单个字符的像素集合
inletter = False
foundletter=False
start = 0
end = 0
letters = []
for y in range(im2.size[0]): # slice across
    for x in range(im2.size[1]): # slice down
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    # 左边缘
    if foundletter == False and inletter == True:
        foundletter = True
        start = y
    # 右边缘
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))
    inletter=False

# 对验证码图片进行切割并比对
v = VectorCompare()
for letter in letters:
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    guess = []
    # 将切割得到的验证码小片段与每个训练片段进行比较
    for image in imageset:
        for letter,y in image.items():
            guess.append((v.relation(y,buildvector(im3)),letter))
    guess.sort(reverse=True)    # 降序排列
    print(guess[0])


