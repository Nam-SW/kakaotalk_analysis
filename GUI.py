import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QRadioButton, QFileDialog, QPushButton, QMessageBox
from analysis import analysis
# import analysis as an

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.an = analysis()
        self.radio = []

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # 위젯 생성
        self.setfilename = QPushButton('파일 선택', self)
        
        self.radio.append(QRadioButton('windows', self))
        self.radio.append(QRadioButton('Mac OS', self))
        self.radio.append(QRadioButton('android', self))
        self.radio.append(QRadioButton('IOS', self))

        self.Fname_Label = QLabel('미선택')
        self.input_name = QLineEdit()
        self.submit = QPushButton('분석 시작', self)

        # 위젯 설정
        self.input_name.setPlaceholderText('미입력시 전체 분석')
        self.setfilename.clicked.connect(self.showDialog)
        self.submit.clicked.connect(self.start_Analysis)

        # 배치
        grid.addWidget(QLabel('대화 파일:'), 0, 0)
        grid.addWidget(QLabel('데이터\n운영체제:'), 1, 0, 4, 1)
        grid.addWidget(QLabel('분석할 이름:'), 5, 0)

        grid.addWidget(self.Fname_Label, 0, 1)
        grid.addWidget(self.setfilename, 0, 2)
        for i in range(len(self.radio)):
            grid.addWidget(self.radio[i], i+1, 1)
        grid.addWidget(self.input_name, 5, 1)
        grid.addWidget(self.submit, 5, 2)

        self.setWindowTitle('test')
        self.setGeometry(300, 300, 300, 250)
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.filename = fname[0]
            self.Fname_Label.setText(fname[0].split('/')[-1])
    
    def start_Analysis(self):
        if self.Fname_Label == '미선택':
            QMessageBox.about(self, 'Error', '분석할 파일을 선택하세요.')
            return

        for i in range(len(self.radio)):
            if self.radio[i].isChecked():
                os = i+1
                break
        else:
            QMessageBox.about(self, 'Error', '데이터셋을 추출한 os를 선택하세요.')
            return

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())