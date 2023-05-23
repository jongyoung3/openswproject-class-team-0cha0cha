from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    #메인창 내용물
    def setupUi(self, MainWindow):
        #메인창 관련
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 700)
        MainWindow.setMinimumSize(QtCore.QSize(1200, 700))
        MainWindow.setMaximumSize(QtCore.QSize(1200, 700))
        MainWindow.setAnimated(False)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        
        #ps창 관련
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        
        self.Psframe = QtWidgets.QFrame(self.centralwidget)
        self.Psframe.setGeometry(QtCore.QRect(590, 520, 591, 121))
        self.Psframe.setFrameShape(QtWidgets.QFrame.Box)
        self.Psframe.setObjectName("Psframe")
        
        self.PsTitle = QtWidgets.QLabel(self.Psframe)
        self.PsTitle.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.PsTitle.setFont(font)
        self.PsTitle.setObjectName("PsTitle")
        
        self.PsContents = QtWidgets.QLabel(self.Psframe)
        self.PsContents.setGeometry(QtCore.QRect(20, 30, 351, 31))
        self.PsContents.setObjectName("PsContents")
        
        
        #검색창 관련
        self.SearchFrame = QtWidgets.QFrame(self.centralwidget)
        self.SearchFrame.setGeometry(QtCore.QRect(590, 10, 591, 51))
        self.SearchFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.SearchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SearchFrame.setObjectName("SearchFrame")
        
        self.SearchEdit = QtWidgets.QLineEdit(self.SearchFrame)
        self.SearchEdit.setGeometry(QtCore.QRect(10, 10, 531, 31))
        self.SearchEdit.setObjectName("SearchEdit")
        
        self.SearchButton = QtWidgets.QPushButton(self.SearchFrame)
        self.SearchButton.setGeometry(QtCore.QRect(540, 10, 41, 31))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./ClueIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.SearchButton.setIcon(icon)
        self.SearchButton.setObjectName("SearchButton")
        
        
        #탭1 정의
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(590, 70, 591, 441))
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.Tab1 = QtWidgets.QWidget()
        self.Tab1.setObjectName("Tab1")
        
        
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
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 581, 729))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(411, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        
        #제목 로딩될 큰 글씨
        font = QtGui.QFont()
        font.setFamily("한컴산뜻돋움")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        
        self.NameLabel1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.NameLabel2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.NameLabel3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        
        self.NameLabel1.setGeometry(QtCore.QRect(10, 10, 361, 31))
        self.NameLabel2.setGeometry(QtCore.QRect(10, 180, 361, 31))
        self.NameLabel3.setGeometry(QtCore.QRect(10, 350, 361, 31))
        
        self.NameLabel1.setFont(font)
        self.NameLabel2.setFont(font)
        self.NameLabel3.setFont(font)
        
        self.NameLabel1.setObjectName("NameLabel1")
        self.NameLabel2.setObjectName("NameLabel2")
        self.NameLabel3.setObjectName("NameLabel3")
        
        
        #내용 로딩될 작은 글씨
        self.ContentLabel1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ContentLabel3 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        
        self.ContentLabel1.setGeometry(QtCore.QRect(150, 60, 93, 15))
        self.ContentLabel2.setGeometry(QtCore.QRect(150, 230, 93, 17))
        self.ContentLabel3.setGeometry(QtCore.QRect(150, 390, 411, 101))
        
        self.ContentLabel1.setMaximumSize(QtCore.QSize(411, 81))
        self.ContentLabel2.setMaximumSize(QtCore.QSize(411, 81))
        self.ContentLabel3.setMaximumSize(QtCore.QSize(411, 101))
        
        self.ContentLabel1.setObjectName("ContentLabel1")
        self.ContentLabel2.setObjectName("ContentLabel2")
        self.ContentLabel3.setObjectName("ContentLabel3")
        
        
        #사진 나오는 곳: 지금은 landscape 하나만 나오게 해놨음
        self.image1 = QLabel(self.scrollAreaWidgetContents)
        self.image2 = QLabel(self.scrollAreaWidgetContents)
        self.image3 = QLabel(self.scrollAreaWidgetContents)
        self.image1.resize(480,490)
        self.image2.resize(480,490)
        self.image3.resize(480,490)
        self.image1.setGeometry(10, 40, 131, 131)
        self.image2.setGeometry(10, 210, 131, 131)
        self.image3.setGeometry(10, 380, 131, 131)
        pixmap = QPixmap("landscape.png")
        self.image1.setPixmap(QPixmap(pixmap))
        self.image2.setPixmap(QPixmap(pixmap))
        self.image3.setPixmap(QPixmap(pixmap)) 
        
        #리뷰의 별점 관련: 지금은 최상단꺼 1개만 구현해놓음
        font = QtGui.QFont()
        font.setFamily("돋움")
        
        self.reviewPoint1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewPoint1.setGeometry(QtCore.QRect(140, 40, 51, 17))
        self.reviewPoint1.setMaximumSize(QtCore.QSize(411, 101))
        self.reviewPoint1.setFont(font)
        self.reviewPoint1.setObjectName("reviewPoint1")
        
        self.reviewStar1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviewStar1.setGeometry(QtCore.QRect(190, 40, 64, 15))
        self.reviewStar1.setObjectName("reviewStar1")
        
        self.reviews1 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.reviews1.setGeometry(QtCore.QRect(260, 40, 101, 16))
        self.reviews1.setObjectName("reviews1")
        
        
        #로딩된 곳 삭제 관련
        self.deleteButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.deleteButton.setGeometry(QtCore.QRect(430, 10, 131, 31))
        self.deleteButton.setObjectName("deleteButton")
        
        self.trashCan = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.trashCan.setGeometry(QtCore.QRect(520, 10, 31, 31))
        self.trashCan.setText("")
        self.trashCan.hide()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("TeamProjects/trashcan.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.trashCan.setIcon(icon1)
        self.trashCan.setIconSize(QtCore.QSize(30, 30))
        self.trashCan.setObjectName("pushButton")
        
        self.cancelBtn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.cancelBtn.setGeometry(QtCore.QRect(430, 10, 71, 31))
        self.cancelBtn.setObjectName("pushButton_2")
        self.cancelBtn.hide()
        
        #탭1 정의 완료, 탭2 정의 완료
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.Tab1, "")
        self.Tab2 = QtWidgets.QWidget()
        self.Tab2.setObjectName("Tab2")
        self.tabWidget.addTab(self.Tab2, "")
        
        
        #맵 관련: 지금은 같이 올린 html 파일 주소 입력되어 있음
        self.Map = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.Map.setGeometry(QtCore.QRect(20, 10, 551, 641))
        self.Map.setUrl(QtCore.QUrl("file:///C:/Users/31125/Desktop/python_files/TeamProjects/map.html"))
        self.Map.setObjectName("Map")
        
        
        #메뉴바 관련
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuabout = QtWidgets.QMenu(self.menuBar)
        self.menuabout.setObjectName("menuabout")
        MainWindow.setMenuBar(self.menuBar)
        
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setShortcutContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.actionAbout.setObjectName("actionAbout")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        
        self.menuabout.addSeparator()
        self.menuabout.addAction(self.actionAbout)
        self.menuabout.addAction(self.actionQuit)
        self.menuBar.addAction(self.menuabout.menuAction())

        #내용물 정의 완료, 시그널로 제어
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionAbout.triggered.connect(self.aboutOpen)
        self.actionQuit.triggered.connect(app.quit)
        self.SearchButton.clicked.connect(self.SearchClicked)
        self.deleteButton.clicked.connect(self.deleteButton.hide)
        self.deleteButton.clicked.connect(self.cancelBtn.show)
        self.deleteButton.clicked.connect(self.trashCan.show)
        self.cancelBtn.clicked.connect(self.deleteButton.show)
        self.cancelBtn.clicked.connect(self.trashCan.hide)
        self.cancelBtn.clicked.connect(self.cancelBtn.hide)
        self.trashCan.clicked.connect(self.deleteButton.show)
        self.trashCan.clicked.connect(self.trashCan.hide)
        self.trashCan.clicked.connect(self.cancelBtn.hide)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.Dialog = QDialog()

    #메인창 내용물에 한글로 번역된 글자들이 들어감
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TripWithGPT"))
        self.PsTitle.setText(_translate("MainWindow", "P.S."))
        self.PsContents.setText(_translate("MainWindow", "GPT의 TMI 설명부분"))
        self.NameLabel1.setText(_translate("MainWindow", "NameLabel1"))
        self.NameLabel2.setText(_translate("MainWindow", "NameLabel2"))
        self.NameLabel3.setText(_translate("MainWindow", "NameLabel3"))
        self.ContentLabel1.setText(_translate("MainWindow", "대충 내용물 1"))
        self.ContentLabel2.setText(_translate("MainWindow", "<html><head/><body><p>대충 내용물 2</p></body></html>"))
        self.ContentLabel3.setText(_translate("MainWindow", "<html><head/><body><p>대충 내용물 3</p></body></html>"))
        self.deleteButton.setText(_translate("MainWindow", "Check to delete"))
        self.reviewPoint1.setText(_translate("MainWindow", "4.2"))
        self.reviews1.setText(_translate("MainWindow", "(9, 487)"))
        self.reviewStar1.setText(_translate("MainWindow", "★★★★★"))
        self.cancelBtn.setText(_translate("MainWindow", "Cancel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab1), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab2), _translate("MainWindow", "Tab 2"))
        self.menuabout.setTitle(_translate("MainWindow", "Menu"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))

    #메뉴바에 about 누르면 팀 정보창 열리게
    def aboutOpen(self):
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(400, 300)
        
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(8)
        font.setKerning(True)
        
        self.label_2 = QtWidgets.QLabel(self.Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 130, 64, 15))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(self.Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 130, 231, 81))
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(self.Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.label_4.setFont(font)
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setIndent(-1)
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(self.Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 64, 15))
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        
        font = QtGui.QFont()
        font.setFamily("굴림")
        font.setPointSize(10)
        self.label = QtWidgets.QLabel(self.Dialog)
        self.label.setGeometry(QtCore.QRect(10, 70, 381, 71))
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.CloseButton = QtWidgets.QPushButton(self.Dialog)
        self.CloseButton.setGeometry(QtCore.QRect(280, 240, 93, 28))
        self.CloseButton.setObjectName("CloseButton")

        self.aboutRetranslateUi(self.Dialog)
        self.CloseButton.clicked.connect(self.Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)
        self.Dialog.show()

    #about 창도 한글로 글자들 넣어줌
    def aboutRetranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "About"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p>23-1학기 오픈소스 기초프로젝트</p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p>3팀 0차0차</p></body></html>"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\">★팀장: 2022041062 최상영 - 크롤링 및 총괄 담당★</p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p>2020039070 전종영 - 크롤링 담당</p><p>2022041081 홍준석 - API 담당</p><p>2022041056 윤정아 - GUI 담당</p><p><br/></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>팀원:</p></body></html>"))
        self.CloseButton.setText(_translate("Dialog", "닫기"))

    #검색 버튼 누르면 크롤링, API로 나온 내용들 로딩되게 구현할 예정
    #현재는 NameLabel1이 검색창에 입력한 내용으로 변함
    def SearchClicked(self):
        self.text = self.SearchEdit.text()
        self.NameLabel1.setText(self.text)
        #apis.APIS(1,self.text)
        #self.Map.setUrl(QtCore.QUrl("file:///C:/Users/31125/Desktop/python_files/TeamProjects/map.html"))
        


from PyQt5 import QtWebEngineWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

