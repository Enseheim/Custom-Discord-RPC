from pypresence import Presence
import time
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox, QWidget, QMenu, QAction
from PyQt5.uic import loadUi
from threading import Thread
import webbrowser
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QSize, QThread
from PyQt5.QtGui import QIcon


load_dotenv('config.env')

client_id = os.getenv("id")
text_state = os.getenv("text_state")
rpc_cover = os.getenv("rpc_image")


class DRPC(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ticks = 0

        self.RPC = Presence(client_id)

        self.start = time.time()

        loadUi('assets/ui/main.ui', self)

        
        self.discordbtn.setIcon(QIcon('assets/icons/discord.svg'))
        self.discordbtn.setIconSize(QSize(18, 18))

        self.idupdater.setIcon(QIcon('assets/icons/reload.svg'))
        self.idupdater.setIconSize(QSize(18, 18))

        self.githubbtn.setIcon(QIcon('assets/icons/github.svg'))
        self.githubbtn.setIconSize(QSize(20, 20))

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        try:
            self.RPC.connect()
        except:
            pass
        
        self.line_id.setText(client_id)
        self.line_state.setText(text_state)
        self.icon_name_line.setText(rpc_cover)

        self.line_id.textChanged.connect(self.rwrpc)
        self.line_state.textChanged.connect(self.rwrpc)
        self.icon_name_line.textChanged.connect(self.rwrpc)

        self.devportal.clicked.connect(lambda: webbrowser.open_new_tab("https://discord.com/developers/applications/"))
        self.discordbtn.clicked.connect(lambda: webbrowser.open_new_tab('https://discord.gg/y8xTQBAVwD'))
        self.githubbtn.clicked.connect(lambda: webbrowser.open_new_tab('https://github.com/Enseheim'))

        self.idupdater.clicked.connect(self.idreloader)

        self.minimizedhint.clicked.connect(self.programMinimize)
        self.closehint.clicked.connect(self.closeProgram)

        try:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.rpcupdate)
            self.timer.start(1000)

        except:
            pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)

            self.qss = """QWidget {
                background-color: #3c3c44;
            }


            QLabel {
                color: #757e8a;
            }


            QLineEdit {
                color: white;
                border-radius: 4px;
                border: 1px solid #f571f5;
                padding: 5px 15px;
            }


            QLineEdit:hover {
                background: #f571f5;
                border: 1px solid #f571f5;
            }


            QPushButton {
                color: white;
                background-color: #4e5058;
                border: none;
                border-radius: 4px
            }


            QPushButton:hover {
                background: #6d6f78;
            }


            QMenu {
                background-color: #111214;
                color: #9ca1a7;
                padding: 5px 5px;
                border: 1px solid #111214;
                border-radius: 4px;
            }


            QMenu::item:selected {
                background-color: #505cdc;
                color: white;
                padding: 5px 5px;
                border: 1px solid #505cdc;
                border-radius: 4px;
            }
            """
            
            self.centralwidget.setStyleSheet(self.qss)
            event.accept()
        

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:

            self.qss = """QWidget {
                background-color: #313338;
            }


            QLabel {
                color: #757e8a;
            }


            QLineEdit {
                color: white;
                border-radius: 4px;
                border: 1px solid #5865f2;
                padding: 5px 15px;
            }


            QLineEdit:hover {
                background: #4853c7;
                border: 1px solid #5865f2;
            }


            QPushButton {
                color: white;
                background-color: #4e5058;
                border: none;
                border-radius: 4px
            }


            QPushButton:hover {
                background: #6d6f78;
            }


            QMenu {
                background-color: #111214;
                color: #9ca1a7;
                padding: 5px 5px;
                border: 1px solid #111214;
                border-radius: 4px;
            }


            QMenu::item:selected {
                background-color: #505cdc;
                color: white;
                padding: 5px 5px;
                border: 1px solid #505cdc;
                border-radius: 4px;
            }
            """

            self.centralwidget.setStyleSheet(self.qss)
            event.accept()

    def rwrpc(self):
        new_state = self.line_state.text()
        new_id = self.line_id.text()
        new_rpc_cover = self.icon_name_line.text()
        
        with open('config.env', 'w', encoding='utf-8') as file:
            file.write(f'id="{new_id}"\ntext_state="{new_state}"\nrpc_image="{new_rpc_cover}"')
            
        print(new_id, new_state, new_rpc_cover)


    def idreloader(self):
        new_id = self.line_id.text()

        try:
            self.RPC.close()
            self.RPC = Presence(new_id)
            self.RPC.connect()

        except:
            self.clientIdError()
            self.line_id.setText("")

    def clientIdError(self):
        QMessageBox.about(self, "Ошибка", "Неправленный ID клиента")

    def rpcupdate(self):
        
        try:

            new_state = self.line_state.text()
            new_rpc_cover = self.icon_name_line.text()

            self.RPC.update(
                state=new_state,
                start=self.start,
                large_image=new_rpc_cover
            )

        except:
            pass


    def closeProgram(self):
        self.RPC.close()
        exit()


    def programMinimize(self):
        self.showMinimized()



if __name__ == "__main__":
    app = QApplication([])
    window = DRPC()
    window.show()
    app.exec_()