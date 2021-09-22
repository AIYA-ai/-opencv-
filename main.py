import os
import time
import sys
import numpy as np
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QFileDialog,QMessageBox, QProgressBar
import distinguish
class Windows_qt5(QWidget):

    def __init__(self):
        super().__init__()
        self.imageScr1 ="./source material/1.jpg"
        self.imageScr2 ="./source material/2.jpg"
        # 设置布局
        self.setUI()

    def setUI(self):
        # 网格布局
        grid_layout = QGridLayout()
        grid_layout.setSpacing(30)  # 设置组件间间距
        self.setLayout(grid_layout)

        # 第一行按钮
        selectImageAButton = QPushButton(self)
        selectImageBButton = QPushButton(self)

        # 第一行设置
        b=1
        selectImageAButton.setText("选择要识别的图片A")
        selectImageAButton.clicked.connect(self.selectImageVoid1)
        selectImageBButton.setText("选择要识别的图片B")
        selectImageBButton.clicked.connect(self.selectImageVoid2)
        # 第二行
        self.imageALable = QLabel(self)
        startScreenButton = QPushButton(self)
        self.imageBLable = QLabel(self)
        # 第二行设置
        self.imageALable.setPixmap(QPixmap(self.imageScr1))  # 设置显示的图片
        self.imageALable.setScaledContents(True)
        self.imageALable.setAlignment(Qt.AlignCenter)  # 居中显示

        startScreenButton.setText("开始识别")
        startScreenButton.clicked.connect(self.showScreenNum)
        self.imageBLable.setPixmap(QPixmap(self.imageScr2))  # 设置显示的图片
        self.imageBLable.setScaledContents(True)
        self.imageBLable.setAlignment(Qt.AlignCenter)
        # 第三行
        imageTextLable = QLabel(self)
        operationLable = QLabel(self)
        endFrontLabel = QLabel(self)
        # 第三行设置
        imageTextLable.setText("需要识别的图片A")
        imageTextLable.setAutoFillBackground(True)
        imageTextLable.setAlignment(Qt.AlignCenter)

        operationLable.setText("操作")
        operationLable.setAutoFillBackground(True)
        operationLable.setAlignment(Qt.AlignCenter)

        endFrontLabel.setText("需要识别的图片B")
        endFrontLabel.setAutoFillBackground(True)
        endFrontLabel.setAlignment(Qt.AlignCenter)

        # 第四行
        self.progressBar = QProgressBar(self)
        # 第四行设置
        self.progressBar.setMinimum(0)  # 设置进度条最小值
        self.progressBar.setMaximum(100)  # 设置进度条最大值
        self.progressBar.setValue(0)  # 进度条初始值为0

        # 第一行
        grid_layout.addWidget(selectImageAButton, 0, 0)
        grid_layout.addWidget(selectImageBButton, 0, 2)
        # 第二行
        grid_layout.addWidget(self.imageALable, 1, 0)
        grid_layout.addWidget(startScreenButton, 1, 1)
        grid_layout.addWidget(self.imageBLable, 1, 2)
        # 第三行
        grid_layout.addWidget(imageTextLable, 2, 0)
        grid_layout.addWidget(operationLable, 2, 1)
        grid_layout.addWidget(endFrontLabel, 2, 2)
        # 第四行
        grid_layout.addWidget(self.progressBar, 3, 0, 1, 3)

        # 高度设置
        grid_layout.setRowMinimumHeight(1, 400)

        # 设置基本参数
        self.move(1024, 100)  # 改变位置
        # self.resize(1000, 660)
        self.setFixedSize(600, 600)
        self.setWindowTitle('笔迹识别软件v1.0')  # 设置标题
        self.setWindowIcon(QIcon('icon.png'))
        self.show()  # 显示窗口

    def selectImageVoid1(self):
        self.imageScr1, b = QFileDialog.getOpenFileName(None, "请选择要添加的文件", "./测试素材/","Text Files (*.png);;Text Files (*.jpg);;All Files (*)")
        if len(b) != 0:
            src = cv2.imdecode(np.fromfile(self.imageScr1, dtype=np.uint8), -1)
            if b=="Text Files (*.png)" :
                cv2.imencode(".png", src)[1].tofile(self.imageScr1)
                reply = QMessageBox.about(self, "提示", "图片选择成功")
            elif b=="Text Files (*.jpg)":
                cv2.imencode(".jpg", src)[1].tofile(self.imageScr1)
                reply = QMessageBox.about(self, "提示", "图片选择成功")
            else:
                reply = QMessageBox.about(self, "警告", "文件类型选择错误，请重新选择")
                self.imageScr1 = "./source material/1.jpg"
            self.imageALable.setPixmap(QPixmap(self.imageScr1))  # 设置显示的图片
            QApplication.processEvents()
        else:
            self.imageScr1 = "./source material/1.jpg"
            reply = QMessageBox.about(self, "警告", "图片未选取成功")
    def selectImageVoid2(self):
        self.imageScr2, b = QFileDialog.getOpenFileName(None, "请选择要添加的文件", "./测试素材/","Text Files (*.png);;Text Files (*.jpg);;All Files (*)")
        if len(b) != 0:
            src = cv2.imdecode(np.fromfile(self.imageScr2, dtype=np.uint8), -1)
            if b == "Text Files (*.png)":
                cv2.imencode(".png", src)[1].tofile(self.imageScr2)
                reply = QMessageBox.about(self, "提示", "图片选择成功")
            elif b == "Text Files (*.jpg)":
                cv2.imencode(".jpg", src)[1].tofile(self.imageScr2)
                reply = QMessageBox.about(self, "提示", "图片选择成功")
            else:
                reply = QMessageBox.about(self, "警告", "文件类型选择错误，请重新选择")
                self.imageScr2 = "./source material/2.jpg"
            self.imageBLable.setPixmap(QPixmap(self.imageScr2))  # 设置显示的图片
            QApplication.processEvents()
        else:
            self.imageScr2 = "./source material/2.jpg"
            reply = QMessageBox.about(self, "警告", "图片未选取成功")
    def showScreenNum(self):
        reply = QMessageBox.about(self, "提示", "开始识别，请稍等...")
        jg = distinguish.test(self.imageScr1,self.imageScr2)
        if len(jg)!=0:
            for i in range(0, 101):
                self.progressBar.setValue(i)
                time.sleep(0.01)
            reply = QMessageBox.about(self, "识别结果", jg)
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(r'工作日志.txt', mode="ta", encoding="utf-8") as ta:
                # a模式:打开文件指针直接跳到文件末尾
                ta.write(localtime + " 运行成功 "+jg+"\n")
        else:
            reply = QMessageBox.about(self, "警告", "程序运行错误请重试")
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open(r'工作日志.txt', mode="ta", encoding="utf-8") as ta:
                # a模式:打开文件指针直接跳到文件末尾
                ta.write(localtime +" 运行出现错误 ""\n")


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用对象
    ex = Windows_qt5()
    sys.exit(app.exec_())  # 设置安全退出
