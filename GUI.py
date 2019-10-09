import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QRadioButton, QFileDialog, QPushButton, QMessageBox, QProgressBar
from analysis import analysis
import operator

class Communicate(QObject):
    bar_on = pyqtSignal()
    bar_off = pyqtSignal()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.an = analysis()
        self.radio = []
        self.rank = []
        self.c = Communicate()
        self.c.bar_on.connect(self.bar_unlimit_on)
        self.c.bar_off.connect(self.bar_unlimit_off)

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

        self.pbar = QProgressBar()

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
        grid.addWidget(QLabel('가장 많이 한 말 top 5'), 7, 0, 1, 3)

        grid.addWidget(self.Fname_Label, 0, 1)
        grid.addWidget(self.setfilename, 0, 2)
        for i in range(len(self.radio)):
            grid.addWidget(self.radio[i], i+1, 1)
        grid.addWidget(self.input_name, 5, 1)
        grid.addWidget(self.submit, 5, 2)

        grid.addWidget(self.pbar, 6, 0, 1, 3)

        for i in range(5):
            self.rank.append(QLabel(str(i+1) + '. '))
            grid.addWidget(self.rank[i], i+8, 0, 1, 4)

        self.setWindowTitle('test')
        # self.setGeometry(300, 300, 300, 250)
        self.show()

    def showDialog(self):
        self.pbar.setValue(0)
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            self.filename = fname[0]
            self.Fname_Label.setText(fname[0].split('/')[-1])
    
    def start_Analysis(self):
        # 입력 에러 검사
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

        # 분석 시작
        self.c.bar_on.emit()
        state = self.an.fileload(self.filename, os)
        if not state:
            QMessageBox.about(self, 'Error', '파일 로드에 실패했습니다.')
            return
        
        self.an.analysis(self.input_name.text())

        # 가장 많이 한 말 5위 단어 및 빈도 출력
        for i in self.an.get_rank(5):
            self.rank[i[0]].setText(self.rank[i[0]].text()[:3]+i[1]+': '+str(i[2]))

        self.c.bar_off.emit()
        self.an.write_wordcloud()


    def bar_unlimit_on(self):
        self.pbar.setRange(0, 0)

    def bar_unlimit_off(self):
        self.pbar.setRange(0, 100)
        self.pbar.setValue(100)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())