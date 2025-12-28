from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow

#test git

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
