import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QRadioButton, QFileDialog, QPushButton

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.radio = []

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.setfilename = QPushButton('파일 선택', self)
        self.setfilename.clicked.connect(self.showDialog)
        
        self.radio.append(QRadioButton('windows', self))
        self.radio.append(QRadioButton('Mac OS', self))
        self.radio.append(QRadioButton('android', self))
        self.radio.append(QRadioButton('IOS', self))

        self.filename = QLabel('미선택')
        self.name = QLineEdit()
        self.name.setPlaceholderText('미입력시 전체 분석')

        grid.addWidget(QLabel('대화 파일:'), 0, 0)
        grid.addWidget(QLabel('데이터\n운영체제:'), 1, 0, 4, 1)
        grid.addWidget(QLabel('분석할 이름:'), 5, 0)

        grid.addWidget(self.filename, 0, 1)
        grid.addWidget(self.setfilename, 0, 2)
        for i in range(len(self.radio)):
            grid.addWidget(self.radio[i], i+1, 1)
        grid.addWidget(self.name, 5, 1)

        self.setWindowTitle('test')
        self.setGeometry(300, 300, 300, 250)
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            f = open(fname[0], 'r', encoding='UTF8')
            with f:
                data = f.read()
                self.filename.setText(fname[0].split('/')[-1])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())