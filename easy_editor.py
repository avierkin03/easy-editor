import os
from PyQt5.QtWidgets import *
 
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

#підключаємо функції-обробники до відповідних віджетів
btn_dir.clicked.connect(showFilenamesList)


#запускаємо обробку подій
win.show()
app.exec()