#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter
import os

app = QApplication([])
main_win = QWidget()
lb_image = QLabel('Image')
btn_dir = QPushButton("Папка")
btn_left = QPushButton("Влево")
btn_right = QPushButton("Вправо")
btn_mirror = QPushButton("Зеркало")
btn_contrast = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")
btn_blur = QPushButton("Размыть")
lw_files = QListWidget()

#направляющие линии
col1 = QVBoxLayout()
col2 = QVBoxLayout()
main_row = QHBoxLayout()
btn_row = QHBoxLayout()

#размещение виджетов
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

btn_row.addWidget(btn_left)
btn_row.addWidget(btn_mirror)
btn_row.addWidget(btn_right)
btn_row.addWidget(btn_contrast)
btn_row.addWidget(btn_bw)
btn_row.addWidget(btn_blur)

col2.addLayout(btn_row)
col2.addWidget(lb_image)

main_row.addLayout(col1, 20)
main_row.addLayout(col2, 80)

main_win.setLayout(main_row)

def chooseWorkdir():
    global workdir 
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
    return result

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    files = os.listdir(workdir)
    images = filter(files, extensions)
    lw_files.clear()
    for image in images:
        print('1')
        lw_files.addItem(image)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.modified= 'Modified'
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        lb_image.hide() 
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.modified, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(workdir, self.modified)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.modified, self.filename)
        self.showImage(image_path)
    def do_contrast(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.modified, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.modified, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.modified, self.filename)
        self.showImage(image_path)
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.modified, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_dir.clicked.connect(showFilenamesList)
btn_mirror.clicked.connect(workimage.do_flip)
btn_contrast.clicked.connect(workimage.do_contrast)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_blur.clicked.connect(workimage.do_blur)

main_win.show()
app.exec_()