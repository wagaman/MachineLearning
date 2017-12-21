__author__ = 'sss'
'''
matplotlib 和 pyqt版本相冲突时

对matplotlib重新安装
conda remove matplotlib
pip install matplotlib

手动安装pyqt4等..

'''

import matplotlib.pyplot as plt

if __name__ == '__main__':
    plt.figure(figsize=(15, 5))
    plt.show()
