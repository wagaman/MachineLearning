# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 11:20:21 2017

@author: TF Liu
"""

import random
import string

from PIL import Image, ImageDraw, ImageFont, ImageFilter
 
#字体的位置，不同版本的系统会有不同
font_path = 'C:\\Windows\\Fonts\\Arial.ttf'
#生成几位数的验证码
number = 4
#生成验证码图片的高度和宽度
size = (132,40)
#背景颜色，默认为白色
bgcolor = (255,255,255)
linecolor = (192, 192, 192)
#是否要加入干扰线和点
draw_line = True
draw_point = True
#加入干扰线和干扰点
line_number = 2
point_number = 10
 
Char = list(string.ascii_letters) + list(string.digits)
#用来随机生成一个字符串
def rndChar():
    return Char[random.randint(0,len(Char)-1)] #number是生成验证码的位数
#用来绘制干扰线
def gene_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height)) #线起点，tuple
    end = (random.randint(0, width), random.randint(0, height)) #线终点， tuple
#    linecolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.line([begin, end], fill = linecolor)

def gene_point(draw, width, height):    
    begin = (random.randint(0, width),random.randint(0,height))
    end = begin
    pointcolor = (random.randint(0, 127), random.randint(0, 255), random.randint(0, 255))
    draw.point([begin, end], fill = pointcolor)
 
#生成验证码
def gene_code():
    width,height = size #宽和高
    image = Image.new('RGB',(width,height),bgcolor) #创建图片
    
#    font = ImageFont.truetype() #验证码的字体
    draw = ImageDraw.Draw(image)  #创建画笔
    
#    font_width, font_height = font.getsize(text)
    text=''
    for t in range(number):
        font = ImageFont.truetype(font_path, random.randint(16, 26)) #验证码的字体
        fontcolor = (random.randint(0, 127), random.randint(0, 255), random.randint(0, 255))
        draw.text((33*t+random.randint(0,20), random.randint(0,20)), rndChar(), font=font, fill = fontcolor)
#    draw.text(((width - font_width) / number, (height - font_height) / number),text,font= font,fill=fontcolor) #填充字符串
        text += t

    if draw_line:
        for i in range(line_number):
            gene_line(draw,width,height)
    if draw_point:
        for i in range(point_number):
            gene_point(draw, width, height)     

#    image = image.transform((width+20,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
#    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
    image.show()
#    image.save('idencode.png') #保存验证码图片
if __name__ == "__main__":
    gene_code()
    
        