import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from ui import Ui_MainWindow
import main as blog


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

main_ui = Ui_MainWindow()
NAME = 'Naver Blog Comments Macro'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_ui.setupUi(self)     
        self.show()
        self.setWindowTitle(NAME)

        window_ico = resource_path('favicon.ico')
        self.setWindowIcon(QIcon(window_ico))

        main_ui.keyword.returnPressed.connect(self.addKeyword)

        main_ui.btn_start.clicked.connect(self.btn_startClicked)
        main_ui.btn_add.clicked.connect(self.btn_addClicked)
        main_ui.btn_del.clicked.connect(self.btn_delClicked)
        main_ui.btn_clear.clicked.connect(self.btn_clearClicked)

    def btn_clearClicked(self):
        result = QMessageBox.question(self, NAME, "정말로 키워드를 초기화 시키시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            main_ui.keywords.clear()
        else:
            return

    def addKeyword(self):
        if main_ui.keyword.text().replace(" ", ""):
            main_ui.keywords.addItem(main_ui.keyword.text())
            main_ui.keyword.clear()
        return
    def btn_addClicked(self):
        self.addKeyword()
        return

    def btn_delClicked(self):
        if main_ui.keywords.currentItem():
            main_ui.keywords.takeItem(main_ui.keywords.currentRow())
        return 

    def btn_startClicked(self):
        id = main_ui.id.text()
        pwd = main_ui.pwd.text()
        keywords = []
        text = []

        if main_ui.keywords.count() > 0:
            for i in range(main_ui.keywords.count()):
                keywords.append(main_ui.keywords.item(i).text())
        else: keywords = None

        if main_ui.textEdit.toPlainText():
            text = main_ui.textEdit.toPlainText()
        else:
            text = None

        if all([id, pwd, keywords, text]):
            cmt_write_urls = blog.start_function(id, pwd, keywords, text)

            for i in cmt_write_urls:
                print(i)
            
            return
        else:
            QMessageBox.information(self,NAME,'빈칸을 모두 채워주세요')
            return


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())