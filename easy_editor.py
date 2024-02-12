import os
from PyQt5.QtWidgets import (
   QApplication, QWidget, QFileDialog,QLabel, 
   QPushButton, QListWidget,QHBoxLayout, QVBoxLayout
)
 
from PyQt5.QtCore import Qt # потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
from PyQt5.QtGui import QPixmap # оптимізована для показу на екрані картинка
from PIL import Image, ImageFilter

#створюємо додаток та його вікно
app = QApplication([])
win = QWidget()      
win.resize(700, 500)
win.setWindowTitle('Easy Editor')

#створюємо необхідні віджети
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_files = QListWidget()
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Відзеркалити")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")

row = QHBoxLayout()          # Головна лінія
col1 = QVBoxLayout()         # ділиться на два стовпці
col2 = QVBoxLayout()

col1.addWidget(btn_dir)      # в першому - кнопка вибору каталогу
col1.addWidget(lw_files)     # і список файлов
col2.addWidget(lb_image, 95) # в другому - картинка

row_tools = QHBoxLayout()    # і ряд кнопок
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)
win.show()


#глобальна змінна, яка зберігатиме шлях до обраної папки
workdir = ''

#функція, яка визначає шлях до обраної користувачем папки
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

#функція, яка повертає із списку файлів лише графічні
def filter(files, extensions):
   result = []
   for filename in files:
      for ext in extensions:
         if filename.endswith(ext):
            result.append(filename)
   return result
 
#функція, яка показує у віджеті-списку відфільтровані графічні файли (що мають розширення як в extensions)
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.svg']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)
   lw_files.clear()
   for filename in filenames:
      lw_files.addItem(filename)
 
 
#Клас, який визначає основну логіку роботи фоторедактора
class ImageProcessor():
   def __init__(self):
      self.image = None
      self.dir = None
      self.filename = None
      self.save_dir = "Modified/"
    
   #метод для завантаження обраного користувачем зображення
   def loadImage(self, dir, filename):
      self.dir = dir
      self.filename = filename
      image_path = os.path.join(dir, filename)
      self.image = Image.open(image_path)

   #метод для накадання чорно-білого фільтру
   def do_bw(self):
      self.image = self.image.convert("L")
      self.saveImage()
      image_path = os.path.join(self.dir, self.save_dir, self.filename)
      self.showImage(image_path)

   #метод повороту зображення вліво на 90°
   def do_left(self):
      self.image = self.image.transpose(Image.ROTATE_90)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)
    
   #метод повороту зображення вправо на 90°
   def do_right(self):
      self.image = self.image.transpose(Image.ROTATE_270)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)
    
   #метод для віддзеркалення зображення
   def do_flip(self):
      self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)
    
   #метод для розмиття зображення
   def do_sharpen(self):
      self.image = self.image.filter(ImageFilter.BLUR)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_dir, self.filename)
      self.showImage(image_path)
    
   #метод, що зберігає оброблену копію оригінального зображення в підпапку
   def saveImage(self):
      path = os.path.join(self.dir, self.save_dir)
      if not(os.path.exists(path) or os.path.isdir(path)):
         os.mkdir(path)
      image_path = os.path.join(path, self.filename)
      self.image.save(image_path)
    
   #метод, який відображає зображення, що знаходиться за заданим шляхом path
   def showImage(self, path):
      lb_image.hide()
      pixmapimage = QPixmap(path)
      w, h = lb_image.width(), lb_image.height()
      pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
      lb_image.setPixmap(pixmapimage)
      lb_image.show()


#функція-обробник натискання на назву зображення у віджеті-списку (зчитує назву файлу, завантажує його та відкриває у фоторедакторі)
def showChosenImage():
   if lw_files.currentRow() >= 0:
      filename = lw_files.currentItem().text()
      workimage.loadImage(workdir, filename)
      image_path = os.path.join(workimage.dir, workimage.filename)
      workimage.showImage(image_path)
 
#поточне робоче зображення для роботи
workimage = ImageProcessor() 

#підключаємо функції-обробники до відповідних віджетів
lw_files.currentRowChanged.connect(showChosenImage)
btn_dir.clicked.connect(showFilenamesList)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)

#запускаємо обробку подій
app.exec()
