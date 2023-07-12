import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import naverCafeApi as cafe
from ui import Ui_MainWindow


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

main_ui = Ui_MainWindow()
NAME = "Naver Cafe"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_ui.setupUi(self)     
        self.show()
        self.setWindowTitle(NAME)
        self.browser = None
        self.PATH_IMG1 = None
        self.PATH_IMG2 = None

        window_ico = resource_path('favicon.ico')
        self.setWindowIcon(QIcon(window_ico))

        main_ui.id.setText("itthere2")
        main_ui.pwd.setText("naver1!2@L")

        main_ui.btn_start.clicked.connect(self.btn_startClicked)

    def btn_startClicked(self):
        id = main_ui.id.text()
        pwd = main_ui.pwd.text()
        nick = main_ui.nick.text()
        cafename = main_ui.cafe.text()
        category = main_ui.category.text()
        keyword = main_ui.keyword.text()
        comment = main_ui.comment.toPlainText()

        if all([id, pwd, nick, cafename, category, comment]):
            self.cmt_urls = cafe.naverCafeCrawling(id, pwd, cafename, category, nick, keyword, comment)
        else:
            QMessageBox.information(self, NAME, '빈 칸을 모두 채워주세요')
            return 
        


        

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())