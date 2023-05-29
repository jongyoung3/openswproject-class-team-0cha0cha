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
        self.PsContents.setGeometry(QtCore.QRect(20, 10, 561, 110))
        self.PsContents.setWordWrap(True)
        
        
        #검색창 관련
        self.SearchFrame = QtWidgets.QFrame(self.centralwidget)
        self.SearchFrame.setGeometry(QtCore.QRect(590, 10, 591, 51))
        self.SearchFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.SearchFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        
        self.SearchEdit = QtWidgets.QLineEdit(self.SearchFrame)
        self.SearchEdit.setGeometry(QtCore.QRect(10, 10, 531, 31))
        
        self.SearchButton = QtWidgets.QPushButton(self.SearchFrame)
        self.SearchButton.setGeometry(QtCore.QRect(540, 10, 40, 32))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("TeamProjects/ClueIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.SearchButton.setIcon(icon)
        
        
        #스크롤바 관련
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(590, 100, 591, 411))
        self.scrollArea.setMinimumSize(QtCore.QSize(591, 411))
        self.scrollArea.setMaximumSize(QtCore.QSize(591, 16777215))
        self.scrollArea.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(False)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 591, 1770))
             
        
        #삭제 관련, 교체 관련
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(1050, 65, 131, 31))
        
        self.trashCan = QtWidgets.QPushButton(self.centralwidget)
        self.trashCan.setGeometry(QtCore.QRect(1150, 65, 31, 31))
        self.trashCan.hide()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("TeamProjects/trashcan.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.trashCan.setIcon(icon1)
        
        self.cancelBtn = QtWidgets.QPushButton(self.centralwidget)
        self.cancelBtn.setGeometry(QtCore.QRect(1070, 65, 71, 31))
        self.cancelBtn.hide()
        
        self.changeButton = QtWidgets.QPushButton(self.centralwidget)
        self.changeButton.setGeometry(QtCore.QRect(590, 65, 70, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("TeamProjects/change.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.changeButton.setIconSize(QtCore.QSize(70,25))
        self.changeButton.setIcon(icon1)
        
        
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
        self.makeReviews()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.setTexts(MainWindow)
        
        self.changeButton.clicked.connect(self.changeOpen)
        self.actionAbout.triggered.connect(self.aboutOpen)
        self.actionQuit.triggered.connect(app.quit)
        self.SearchButton.clicked.connect(self.SearchClicked)
        
        self.deleteButton.clicked.connect(self.deleteClicked)
        self.cancelBtn.clicked.connect(self.removeEnd)
        self.trashCan.clicked.connect(self.removeItems)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.Dialog = QDialog()
        self.Form = QDialog()


    #메인창 내용물에 글자들 넣기
    def setTexts(self, MainWindow):
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.PsTitle.setFont(font)
        
        #글자 내용들
        MainWindow.setWindowTitle("TripWithGPT")
        self.PsTitle.setText("P.S.")
        self.PsContents.setText("일본은 최첨단 기술뿐만 아니라 고대 문화가 풍부한 대조적인 나라로 가득합니다. 상징적인 랜드마크와 번화한 도시부터 산과 바다의 고요한 자연의 아름다움까지, 이 매혹적인 나라에는 모두를 위한 무언가가 있습니다. 전통과 현대의 독특한 조화를 경험할 준비를 하시고 여행 중에 맛있는 현지 요리를 맛보는 것도 잊지 마세요!")
        self.deleteButton.setText("Check to delete")
        self.cancelBtn.setText("Cancel")
        self.menuabout.setTitle("Menu")
        self.actionAbout.setText("About")
        self.actionQuit.setText("Exit")


    #리뷰들에 들어가는 제목, 내용물, 리뷰 별과 갯수, 이미지를 생성
    def makeReviews(self):
        self.names = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.contents = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.imgs = [QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents),QtWebEngineWidgets.QWebEngineView(self.scrollAreaWidgetContents)]
        self.reviewPoints = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.reviewStars = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.reviews = [QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents),QtWidgets.QLabel(self.scrollAreaWidgetContents)]
        self.checkBoxes = [QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents),QtWidgets.QCheckBox(self.scrollAreaWidgetContents)]

        font = QtGui.QFont()
        font.setFamily("한컴산뜻돋움")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)

        for i in range(0,10,1):
            self.names[i].setGeometry(QtCore.QRect(10, 8+175*i, 415, 31))
            self.names[i].setFont(font)
            self.names[i].setText(("%s번째") % str(i+1))
            
            self.contents[i].setGeometry(QtCore.QRect(145, 64+175*i, 420, 110))
            self.contents[i].setText(("%s번째 내용물") % str(i+1))
            self.contents[i].setWordWrap(True)
            
            self.imgs[i].setGeometry(QtCore.QRect(10, 42+175*i, 130, 130))
            self.reviewPoints[i].setGeometry(QtCore.QRect(144, 44+175*i, 51, 17))
            self.reviewPoints[i].setText("4.3")
            self.reviewStars[i].setGeometry(QtCore.QRect(175, 44+175*i, 62, 15))
            self.reviewStars[i].setText("★★★★★")
            self.reviews[i].setGeometry(QtCore.QRect(258, 44+175*i, 101, 16))
            self.reviews[i].setText("1,234")
            self.checkBoxes[i].setGeometry(13, 0+175*i, 130, 55)
            self.checkBoxes[i].hide()
            
        self.imgs[0].setUrl(QtCore.QUrl("https://lh3.googleusercontent.com/places/ANJU3DuXkXR4mLpUC8HveQxr6Q6xNSxuiaEWj2fTS0wCxhqg37hk_96rjlQyKfH7mD7tk8AwXdqb9ylUc5pdMO7pd2f8rdHD18-yZis=s1600-w400"))
        self.names[0].setText("도쿄 디즈니랜드(우라야스, 지바현, 일본)")
        self.names[1].setText("오사카 성(오사카, 일본)")
        self.names[2].setText("후시미이나리 신사(교토, 일본)")
        self.contents[0].setText("가족과 디즈니 팬이라면 꼭 방문해야 하는 도쿄 디즈니랜드는 캘리포니아에 있는 오리지널 디즈니랜드의 모든 마법을 체험할 수 있는 곳입니다. 다양한 테마 공간, 화려한 퍼레이드와 쇼, 다양한 캐릭터를 만날 수 있는 도쿄 디즈니랜드는 즐거운 당일치기 여행에 완벽한 장소입니다.")
        self.contents[1].setText("일본에서 가장 유명한 성 중 하나인 오사카 성은 방문객들에게 일본의 풍부한 역사와 문화를 엿볼 수 있는 곳입니다. 언덕 꼭대기에 위치한 이 성에는 도시의 숨막히는 전경을 감상할 수 있는 박물관과 전망대가 있습니다. 멋진 건축물과 아름다운 정원이 있는 오사카 성은 여유로운 산책을 즐기기에 완벽한 장소입니다.")
        self.contents[2].setText("수천 개의 밝은 주황색 도리이 문으로 유명한 후시미이나리 신사는 교토의 상징이자 일본의 가장 상징적인 명소 중 하나입니다. 산의 산책로는 계절에 관계없이 신비롭고 고요한 경험을 제공하며 교토의 멋진 전망을 감상할 수 있는 유명한 정상으로 이어집니다. 카메라를 꼭 지참하세요!")
        self.reviewPoints[0].setText("4.2")
        self.reviewPoints[1].setText("4.7")
        self.reviewPoints[2].setText("3.4")
        self.reviews[0].setText("(9, 487)")
        self.reviews[1].setText("(16, 529)")
        self.reviews[2].setText("(1, 326)")
        self.reviewStars[0].setText("★★★★★")
        self.reviewStars[1].setText("★★★★★")
        self.reviewStars[2].setText("★★★★★")
        
        
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
    #현재는 첫 번째 리뷰 제목이 검색창에 입력한 내용으로 변함
    def SearchClicked(self):
        self.text = self.SearchEdit.text()
        self.names[0].setText(self.text)
        #apis.APIS(1,self.text)
        #self.Map.setUrl(QtCore.QUrl("file:///C:/Users/31125/Desktop/python_files/TeamProjects/map.html"))
        
        
    #deleteButton 눌렀을 때 버튼들 나타나고 사라지게, 체크박스 표시
    def deleteClicked(self):
        self.deleteButton.hide()
        self.cancelBtn.show()
        self.trashCan.show()
        for i in range(0,10,1):
            self.checkBoxes[i].show()
            self.names[i].setGeometry(QtCore.QRect(35, 8+175*i, 415, 31))
        
        
    #cancelBtn 눌렀을 때 체크박스 안보이게 원상복귀, 체크상태 해제
    def removeEnd(self):
        self.deleteButton.show()
        self.trashCan.hide()
        self.cancelBtn.hide()
        for i in range(0,10,1):
            self.checkBoxes[i].hide()
            self.checkBoxes[i].setChecked(False)
            self.names[i].setGeometry(QtCore.QRect(10, 8+175*i, 415, 31))
        
        
    #trashCan 클릭시엔 아이템들 지우고 복구하기: 현재는 그 칸의 기본 세팅된 내용 지워짐
    #삭제 후 정렬 기능은 후에 구현 예정
    def removeItems(self):
        self.deleteButton.show()
        self.trashCan.hide()
        self.cancelBtn.hide()
            
        for i in range(0,10,1):
            if (self.checkBoxes[i].isChecked()):
                self.names[i].clear()
                self.contents[i].clear()
                self.reviewPoints[i].clear()
                self.reviews[i].clear()
                self.reviewStars[i].clear()
                self.imgs[i].hide()
            self.checkBoxes[i].hide()
            self.checkBoxes[i].setChecked(False)
            self.names[i].setGeometry(QtCore.QRect(10, 8+175*i, 415, 31))
            
            
    #리뷰들 위치 교환할 창 열림
    def changeOpen(self, Form):
        self.Form.resize(392, 800)
        
        #시작하면 나오는 1~10번 리뷰들 제목 있는 버튼들
        self.LabelBtns = [QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form)]
        #라벨버튼 눌렀을 때 나오는 1~10번 제목 라벨들
        self.changeLabels = [QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form),QtWidgets.QLabel(self.Form)]
        #라벨버튼 눌렀을 때 나오는 이동버튼
        self.changeBtns = [QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form)]
        #1~10번중 선택했을 때 'n번 선택됨' 띄우는 disabled된 버튼
        self.disableLabelBtns = [QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form),QtWidgets.QPushButton(self.Form)]
        
        for i in range(0,10,1):
            #각 changeLables, disalbeLabelBtns, LabelBtns 위치 지정 및 글자 내용 세팅
            self.changeLabels[i].setGeometry(QtCore.QRect(20,70+70*i,350,22))
            self.changeLabels[i].setAlignment(QtCore.Qt.AlignCenter)
            self.changeLabels[i].setText("%s번"%str(i+1))
            self.changeLabels[i].hide()
            
            self.disableLabelBtns[i].setGeometry(QtCore.QRect(20,70+70*i,350,25))
            self.disableLabelBtns[i].setText("%s번 선택됨"%str(i+1))
            self.disableLabelBtns[i].setDisabled(True)
            self.disableLabelBtns[i].hide()
            
            self.LabelBtns[i].setGeometry(QtCore.QRect(20,70+70*i,350,23))
            self.LabelBtns[i].setText("%s번"%str(i+1))
            
        for i in range(0,11,1):
            #changeBtn 위치 지정, 글자 내용 세팅
            #얘만 따로 뺀 이유는 얘만 총 11개라서
            self.changeBtns[i].setGeometry(QtCore.QRect(150, 35+70*i, 90, 23))
            self.changeBtns[i].setText("이동")
            self.changeBtns[i].hide()
            
        #for문 썼더니 자꾸 열번째 꺼만 되더라구요...
        self.LabelBtns[0].clicked.connect(lambda: self.LabelSelect(0))    
        self.LabelBtns[1].clicked.connect(lambda: self.LabelSelect(1))
        self.LabelBtns[2].clicked.connect(lambda: self.LabelSelect(2))
        self.LabelBtns[3].clicked.connect(lambda: self.LabelSelect(3))
        self.LabelBtns[4].clicked.connect(lambda: self.LabelSelect(4))    
        self.LabelBtns[5].clicked.connect(lambda: self.LabelSelect(5))
        self.LabelBtns[6].clicked.connect(lambda: self.LabelSelect(6))
        self.LabelBtns[7].clicked.connect(lambda: self.LabelSelect(7))
        self.LabelBtns[8].clicked.connect(lambda: self.LabelSelect(8))
        self.LabelBtns[9].clicked.connect(lambda: self.LabelSelect(9))
        
        #취소버튼 
        self.cancelChangeBtn = QtWidgets.QPushButton(self.Form)
        self.cancelChangeBtn.setGeometry(QtCore.QRect(332, 10, 50, 28)) 
        self.cancelChangeBtn.setText("취소")
        self.cancelChangeBtn.hide()
        self.cancelChangeBtn.clicked.connect(self.cancelChange)


        self.Form.setWindowTitle("옮기기")
        QtCore.QMetaObject.connectSlotsByName(self.Form)
        self.Form.show()
        

    #시작하고서 1~10번 제목버튼 누르면 라벨로 전환되고 이동 버튼들 나옴
    def LabelSelect(self,num):
        self.disableLabelBtns[num].show()
        for i in range(0,10,1):
            self.LabelBtns[i].hide()
            self.changeBtns[i].show()
            self.changeLabels[i].show()
            self.cancelChangeBtn.show()
        self.changeBtns[num].hide()
        self.changeBtns[num+1].hide()
        
        
        
        self.changeBtns[0].clicked.connect(lambda: self.changeSelect(num,0))
        self.changeBtns[1].clicked.connect(lambda: self.changeSelect(num,1))
        self.changeBtns[2].clicked.connect(lambda: self.changeSelect(num,2))
        self.changeBtns[3].clicked.connect(lambda: self.changeSelect(num,3))
        self.changeBtns[4].clicked.connect(lambda: self.changeSelect(num,4))
        self.changeBtns[5].clicked.connect(lambda: self.changeSelect(num,5))
        self.changeBtns[6].clicked.connect(lambda: self.changeSelect(num,6))
        self.changeBtns[7].clicked.connect(lambda: self.changeSelect(num,7))
        self.changeBtns[8].clicked.connect(lambda: self.changeSelect(num,8))
        self.changeBtns[9].clicked.connect(lambda: self.changeSelect(num,9))
        self.changeBtns[10].clicked.connect(lambda: self.changeSelect(num,10))
        
        
    #취소 누르면 다시 버튼으로 돌아감
    def cancelChange(self):
        for i in range(0,10,1):
            self.disableLabelBtns[i].hide()
            self.changeBtns[i].hide()
            self.changeLabels[i].hide()
            self.cancelChangeBtn.hide()
            self.LabelBtns[i].show()
            
            
    #첫번째 지정된 리뷰랑 두번째 지정된 리뷰랑 자리 바꾸기
    def changeSelect(self,first_num,second_num):
        #이게 생각해보니까 아래에서 위로 가는 거랑 위에서 아래로 가는 거랑 따로 생각해야 하더라고요
        if (first_num < second_num):
            second_num -=1
            
        self.temps = [str(self.names[first_num].text()),str(self.contents[first_num].text()),str(self.imgs[first_num].url().toString()),str(self.reviewPoints[first_num].text()),str(self.reviews[first_num].text()),str(self.reviewStars[first_num].text())]
        
        self.names[first_num].setText(self.names[second_num].text())
        self.contents[first_num].setText(self.contents[second_num].text())
        self.imgs[first_num].setUrl(QtCore.QUrl(self.imgs[second_num].url().toString()))
        self.reviewPoints[first_num].setText(self.reviewPoints[second_num].text())
        self.reviews[first_num].setText(self.reviews[second_num].text())
        self.reviewStars[first_num].setText(self.reviewStars[second_num].text())
        
        self.names[second_num].setText(self.temps[0])
        self.contents[second_num].setText(self.temps[1])
        self.imgs[second_num].setUrl(QtCore.QUrl(self.temps[2]))
        self.reviewPoints[second_num].setText(self.temps[3])
        self.reviews[second_num].setText(self.temps[4])
        self.reviewStars[second_num].setText(self.temps[5])
               
               
        for i in range(0,10,1):
            self.disableLabelBtns[i].hide()
            self.changeBtns[i].hide()
            self.changeLabels[i].hide()
            self.cancelChangeBtn.hide()
            self.LabelBtns[i].show()       
        self.Form.close()





from PyQt5 import QtWebEngineWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())