from PIL import Image

__author__ = 'sss'

IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160

if __name__ == '__main__':
    image = Image.open("C:\\Users\sss\Desktop\\2907.jpg")
    image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT)) #resize image with high-quality
    image.save("C:\\Users\sss\Desktop\\bbb.png", 'png')