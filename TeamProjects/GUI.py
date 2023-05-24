from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    #메인창 내용물
    def setupUi(self, MainWindow):
        #메인창 관련
        MainWindow.resize(1200, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 700))
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        
        #ps창 관련
        self.Psframe = QtWidgets.QFrame(self.centralwidget)
        self.Psframe.setGeometry(QtCore.QRect(590, 520, 591, 121))
        self.Psframe.setFrameShape(QtWidgets.QFrame.Box)
        
        self.PsTitle = QtWidgets.QLabel(self.Psframe)
        self.PsTitle.setGeometry(QtCore.QRect(10, 10, 91, 21))
        
        self.PsContents = QtWidgets.QLabel(self.Psframe)
        self.PsContents.setGeometry(QtCore.QRect(20, 30, 351, 31))
        
        
        #검색창 관련
        self.SearchFrame = QtWidgets.QFrame(self.centralwidget)
        self.SearchFrame.setGeometry(QtCore.QRect(590, 10, 591, 51))
        self.SearchFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.SearchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.SearchEdit = QtWidgets.QLineEdit(self.SearchFrame)
        self.SearchEdit.setGeometry(QtCore.QRect(10, 10, 531, 31))
        
        self.SearchButton = QtWidgets.QPushButton(self.SearchFrame)
        self.SearchButton.setGeometry(QtCore.QRect(540, 10, 41, 31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("TeamProjects/ClueIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.SearchButton.setIcon(icon)
        
        
        #탭1 정의
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(590, 70, 591, 441))
        self.tabWidget.setDocumentMode(True)
        self.Tab1 = QtWidgets.QWidget()
        
        
        #스크롤바 관련
        self.scrollArea = QtWidgets.QScrollArea(self.Tab1)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 591, 411))
        self.scrollArea.setMinimumSize(QtCore.QSize(591, 411))
        self.scrollArea.setMaximumSize(QtCore.QSize(591, 16777215))
        self.scrollArea.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(False)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 581, 729))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(411, 0))
        
        
        #제목 로딩될 큰 글씨
        self.NameLabel1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.NameLabel2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.NameLabel3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        
        self.NameLabel1.setGeometry(QtCore.QRect(10, 8, 415, 31))
        self.NameLabel2.setGeometry(QtCore.QRect(10, 183, 415, 31))
        self.NameLabel3.setGeometry(QtCore.QRect(10, 357, 415, 31))
        
        
        #내용 로딩될 작은 글씨
        self.ContentLabel1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel1.setWordWrap(True)
        self.ContentLabel2.setWordWrap(True)
        self.ContentLabel3.setWordWrap(True)
        
        self.ContentLabel1.setGeometry(QtCore.QRect(150, 60, 420, 110))
        self.ContentLabel2.setGeometry(QtCore.QRect(150, 235, 420, 110))
        self.ContentLabel3.setGeometry(QtCore.QRect(150, 410, 420, 110))
        
        
        #사진 나오는 곳: 지금은 landscape 하나만 나오게 해놨음
        self.image1 = QLabel(self.scrollAreaWidgetContents)
        self.image2 = QLabel(self.scrollAreaWidgetContents)
        self.image3 = QLabel(self.scrollAreaWidgetContents)
        self.image1.resize(130,130)
        self.image2.resize(130,130)
        self.image3.resize(130,130)
        self.image1.setGeometry(10, 42, 130, 130)
        self.image2.setGeometry(10, 217, 130, 130)
        self.image3.setGeometry(10, 392, 130, 130)
        pixmap = QPixmap("TeamProjects/landscape.png")
        pixmap = pixmap.scaled(130,130)
        self.image1.setPixmap(QPixmap(pixmap))
        pixmap = QPixmap("TeamProjects/hotel.png")
        pixmap = pixmap.scaled(130,130)
        self.image2.setPixmap(QPixmap(pixmap))
        pixmap = QPixmap("TeamProjects/night.png")
        pixmap = pixmap.scaled(130,130)
        self.image3.setPixmap(QPixmap(pixmap)) 
        
        
        #리뷰의 별점 관련: 지금은 상단 3개만 구현해놓음
        self.reviewPoint1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewPoint2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewPoint3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewPoint1.setGeometry(QtCore.QRect(146, 40, 51, 17))
        self.reviewPoint2.setGeometry(QtCore.QRect(146, 215, 51, 17))
        self.reviewPoint3.setGeometry(QtCore.QRect(146, 390, 51, 17))
        
        self.reviewStar1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewStar2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewStar3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewStar1.setGeometry(QtCore.QRect(177, 40, 62, 15))
        self.reviewStar2.setGeometry(QtCore.QRect(177, 215, 66, 15))
        self.reviewStar3.setGeometry(QtCore.QRect(177, 390, 49, 15))
        
        self.reviews1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviews2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviews3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviews1.setGeometry(QtCore.QRect(260, 40, 101, 16))
        self.reviews2.setGeometry(QtCore.QRect(260, 215, 101, 16))
        self.reviews3.setGeometry(QtCore.QRect(260, 390, 101, 16))
        
        
        #로딩된 곳 삭제 관련
        self.deleteButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.deleteButton.setGeometry(QtCore.QRect(430, 10, 131, 31))
        
        self.trashCan = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.trashCan.setGeometry(QtCore.QRect(520, 10, 31, 31))
        self.trashCan.hide()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("TeamProjects/trashcan.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.trashCan.setIcon(icon1)
        self.trashCan.setIconSize(QtCore.QSize(30, 30))
        
        self.cancelBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.cancelBtn.setGeometry(QtCore.QRect(430, 10, 71, 31))
        self.cancelBtn.hide()
        
        
        #deleteButton 클릭시 체크박스로 선택 가능
        self.checkBox1 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox1.setGeometry(13, 0, 130, 55)
        self.checkBox2.setGeometry(13, 175, 130, 55)
        self.checkBox3.setGeometry(13, 350, 130, 55)
        self.checkBox1.hide() 
        self.checkBox2.hide() 
        self.checkBox3.hide() 
        
        
        #탭1 정의 완료, 탭2 정의 완료
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.Tab1, "")
        self.Tab2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.Tab2, "")
        
        
        #맵 관련: 지금은 같이 올린 html 파일 주소 입력되어 있음
        self.Map = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.Map.setGeometry(QtCore.QRect(20, 10, 551, 641))
        self.Map.setUrl(QtCore.QUrl("file:///C:/Users/31125/Desktop/python_files/TeamProjects/map.html"))
        
        
        #메뉴바 관련
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menuabout = QtWidgets.QMenu(self.menuBar)
        MainWindow.setMenuBar(self.menuBar)
        
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        
        self.menuabout.addSeparator()
        self.menuabout.addAction(self.actionAbout)
        self.menuabout.addAction(self.actionQuit)
        self.menuBar.addAction(self.menuabout.menuAction())


        #내용물 정의 완료, 시그널로 제어
        self.setTexts(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionAbout.triggered.connect(self.aboutOpen)
        self.actionQuit.triggered.connect(app.quit)
        self.SearchButton.clicked.connect(self.SearchClicked)
        
        self.deleteButton.clicked.connect(self.deleteClicked)
        self.cancelBtn.clicked.connect(self.removeEnd)
        self.trashCan.clicked.connect(self.removeItems)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.Dialog = QDialog()

    #메인창 내용물에 글자들 넣기
    def setTexts(self, MainWindow):
        #폰트들 정리
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.PsTitle.setFont(font)
        
        font = QtGui.QFont()
        font.setFamily("한컴산뜻돋움")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.NameLabel1.setFont(font)
        self.NameLabel2.setFont(font)
        self.NameLabel3.setFont(font)
        
        font = QtGui.QFont()
        font.setFamily("돋움")
        self.reviewPoint1.setFont(font)
        
        
        #글자 내용들
        MainWindow.setWindowTitle("TripWithGPT")
        self.PsTitle.setText("P.S.")
        self.PsContents.setText("GPT의 TMI 설명부분")
        self.NameLabel1.setText("김용택 / 달이 떴다고 전화를 주시다니요")
        self.NameLabel2.setText("백석 / 여승")
        self.NameLabel3.setText("길 / 윤동주")
        self.ContentLabel1.setText("<html><head/><body><p>달이 떴다고 전화를 주시다니요</p>이 밤 너무나 신나고 근사해요</p><p>내 마음에도 생전 처음 보는</p><p>환한 달이 떠오르고</p><p>산 아래 작은 마을이 그려집니다.</p></body></html>")
        self.ContentLabel2.setText("<html><head/><body><p>여승은 합장하고 절을 했다.</p><p>가지취의 내음새가 났다.</p><p>쓸쓸한 낯이 옛날같이 늙었다.</p><p>나는 불경처럼 서러워졌다.</p></body></html>")
        self.ContentLabel3.setText("<html><head/><body><p>잃어버렸습니다</p><p>무얼 어디다 잃었는지 몰라</p><p>두 손이 주머니를 더듬어</p><p>길에 나아갑니다")
        self.deleteButton.setText("Check to delete")
        self.reviewPoint1.setText("4.2")
        self.reviewPoint2.setText("4.7")
        self.reviewPoint3.setText("3.4")
        self.reviews1.setText("(9, 487)")
        self.reviews2.setText("(16, 529)")
        self.reviews3.setText("(1, 326)")
        self.reviewStar1.setText("★★★★★")
        self.reviewStar2.setText("★★★★★")
        self.reviewStar3.setText("★★★★★")
        self.cancelBtn.setText("Cancel")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), "Tab 1")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), "Tab 2")
        self.menuabout.setTitle("Menu")
        self.actionAbout.setText("About")
        self.actionQuit.setText("Exit")

    #메뉴바에 about 누르면 팀 정보창 열리게
    def aboutOpen(self):
        self.Dialog.resize(400, 300)
        
        self.lectureName = QtWidgets.QLabel(self.Dialog)
        self.lectureName.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.teamName = QtWidgets.QLabel(self.Dialog)
        self.teamName.setGeometry(QtCore.QRect(10, 30, 64, 15))
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setGeometry(QtCore.QRect(60, 130, 64, 15))
        
        self.teamLeader = QtWidgets.QLabel(self.Dialog)
        self.teamLeader.setGeometry(QtCore.QRect(10, 70, 381, 71))
        self.teamMem = QtWidgets.QLabel(self.Dialog)
        self.teamMem.setGeometry(QtCore.QRect(100, 130, 231, 81))
        
        self.CloseButton = QtWidgets.QPushButton(self.Dialog)
        self.CloseButton.setGeometry(QtCore.QRect(280, 240, 93, 28))

        self.aboutSetTexts(self.Dialog)
        self.CloseButton.clicked.connect(self.Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.show()

    #about 창도 글자들 채워줌
    def aboutSetTexts(self, Dialog):
        font = QtGui.QFont()
        font.setFamily("굴림")
        
        font.setPointSize(8)
        self.lectureName.setFont(font)
        self.teamName.setFont(font)
        
        font.setPointSize(10)
        self.teamLeader.setFont(font)
        
        Dialog.setWindowTitle("About")
        self.lectureName.setText("23-1학기 오픈소스 기초프로젝트")
        self.teamName.setText("3팀 0차0차")
        self.teamLeader.setText("<html><head/><body><p align=\"center\">★팀장: 2022041062 최상영 - 크롤링 및 총괄 담당★</p></body></html>")
        self.label.setText("팀원:")
        self.teamMem.setText("<html><head/><body><p>2020039070 전종영 - 크롤링 담당</p><p>2022041081 홍준석 - API 담당</p><p>2022041056 윤정아 - GUI 담당</p><p><br/></p></body></html>")
        self.CloseButton.setText("닫기")

    #검색 버튼 누르면 크롤링, API로 나온 내용들 로딩되게 구현할 예정
    #현재는 NameLabel1이 검색창에 입력한 내용으로 변함
    def SearchClicked(self):
        self.text = self.SearchEdit.text()
        self.NameLabel1.setText(self.text)
        #apis.APIS(1,self.text)
        #self.Map.setUrl(QtCore.QUrl("file:///C:/Users/31125/Desktop/python_files/TeamProjects/map.html"))
        
    #deleteButton 눌렀을 때 버튼들 나타나고 사라지게, 체크박스 표시
    def deleteClicked(self):
        self.deleteButton.hide()
        self.cancelBtn.show()
        self.trashCan.show()
        self.checkBox1.show()
        self.checkBox2.show()
        self.checkBox3.show()
        self.NameLabel1.setGeometry(QtCore.QRect(35, 8, 415, 31))
        self.NameLabel2.setGeometry(QtCore.QRect(35, 183, 415, 31))
        self.NameLabel3.setGeometry(QtCore.QRect(35, 357, 415, 31))
        
    #cancelBtn 눌렀을 때 체크박스 안보이게 원상복귀, 체크상태 해제
    def removeEnd(self):
        self.deleteButton.show()
        self.trashCan.hide()
        self.cancelBtn.hide()
        self.checkBox1.hide()
        self.checkBox2.hide()
        self.checkBox3.hide()
        
        self.checkBox1.setChecked(False)
        self.checkBox2.setChecked(False)
        self.checkBox3.setChecked(False)
        self.NameLabel1.setGeometry(QtCore.QRect(10, 8, 415, 31))
        self.NameLabel2.setGeometry(QtCore.QRect(10, 183, 415, 31))
        self.NameLabel3.setGeometry(QtCore.QRect(10, 357, 415, 31))
        
    #trashCan 클릭시엔 아이템들 지우고 복구하기: 현재는 기본 세팅된 내용 지워짐
    #삭제 후 정렬 기능은 후에 구현 예정
    def removeItems(self):
        self.deleteButton.show()
        self.trashCan.hide()
        self.cancelBtn.hide()
        
        if (self.checkBox1.isChecked()):
            self.NameLabel1.clear()
            self.ContentLabel1.clear()
            self.reviewPoint1.clear()
            self.reviews1.clear()
            self.reviewStar1.clear()
            self.image1.hide()
        
        if (self.checkBox2.isChecked()):
            self.NameLabel2.clear()
            self.ContentLabel2.clear()
            self.reviewPoint2.clear()
            self.reviews2.clear()
            self.reviewStar2.clear()
            self.image2.hide()
            
        if (self.checkBox3.isChecked()):
            self.NameLabel3.clear()
            self.ContentLabel3.clear()
            self.reviewPoint3.clear()
            self.reviews3.clear()
            self.reviewStar3.clear()
            self.image3.hide()
            
            
        self.checkBox1.hide()
        self.checkBox2.hide()
        self.checkBox3.hide()
        self.checkBox1.setChecked(False)
        self.checkBox2.setChecked(False)
        self.checkBox3.setChecked(False)
        self.NameLabel1.setGeometry(QtCore.QRect(10, 8, 415, 31))
        self.NameLabel2.setGeometry(QtCore.QRect(10, 183, 415, 31))
        self.NameLabel3.setGeometry(QtCore.QRect(10, 357, 415, 31))

from PyQt5 import QtWebEngineWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

