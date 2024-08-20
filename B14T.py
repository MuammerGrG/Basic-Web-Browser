import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QComboBox, QMenu, QActionGroup, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QSize

class Tarayici(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Birlik14 Tarayıcı')
        self.setGeometry(100, 100, 1200, 800)
        
        self.current_search_engine = 'http://www.google.com/search?q='
        self.themes = {'Beyaz': 'white', 'Koyu': 'dark'}
        self.current_theme = 'Beyaz'
        
        self.languages = {'Türkçe': 'tr', 'English': 'en'}
        self.current_language = 'Türkçe'
        self.translations = {
            'tr': {
                'back': 'Geri',
                'forward': 'İleri',
                'refresh': 'Yenile',
                'search': "URL'yi veya arama terimini girin...",
                'theme': 'Tema',
                'search_engine': 'Arama Motoru',
                'spotify': 'Spotify',
                'youtube': 'YouTube',
                'steam': 'Steam'
            },
            'en': {
                'back': 'Back',
                'forward': 'Forward',
                'refresh': 'Refresh',
                'search': 'Enter URL or search term...',
                'theme': 'Theme',
                'search_engine': 'Search Engine',
                'spotify': 'Spotify',
                'youtube': 'YouTube',
                'steam': 'Steam'
            }
        }
        
        self.init_ui()

    def init_ui(self):
        self.tarayici = QWebEngineView()
        self.tarayici.setUrl(QUrl('http://www.google.com'))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.tarayici)

        arac_cubugu = QToolBar()
        arac_cubugu.setIconSize(QSize(24, 24))
        self.addToolBar(arac_cubugu)

        self.geri_butonu = QAction(self.translations[self.languages[self.current_language]]['back'], self)
        self.geri_butonu.triggered.connect(self.tarayici.back)
        arac_cubugu.addAction(self.geri_butonu)

        self.ileri_butonu = QAction(self.translations[self.languages[self.current_language]]['forward'], self)
        self.ileri_butonu.triggered.connect(self.tarayici.forward)
        arac_cubugu.addAction(self.ileri_butonu)

        self.yenile_butonu = QAction(self.translations[self.languages[self.current_language]]['refresh'], self)
        self.yenile_butonu.triggered.connect(self.tarayici.reload)
        arac_cubugu.addAction(self.yenile_butonu)

        self.url_cubugu = QLineEdit()
        self.url_cubugu.setPlaceholderText(self.translations[self.languages[self.current_language]]['search'])
        self.url_cubugu.returnPressed.connect(self.url_git)
        arac_cubugu.addWidget(self.url_cubugu)

        self.tarayici.urlChanged.connect(self.url_guncelle)
        
        self.arama_motoru_secimi = QComboBox()
        self.arama_motoru_secimi.addItem('Google', 'http://www.google.com/search?q=')
        self.arama_motoru_secimi.addItem('Bing', 'http://www.bing.com/search?q=')
        self.arama_motoru_secimi.addItem('DuckDuckGo', 'https://duckduckgo.com/?q=')
        self.arama_motoru_secimi.currentIndexChanged.connect(self.arama_motoru_degistir)
        arac_cubugu.addWidget(self.arama_motoru_secimi)
        
        tema_menusu = QMenu(self.translations[self.languages[self.current_language]]['theme'], self)
        tema_grubu = QActionGroup(self)
        for tema in self.themes:
            tema_eylemi = QAction(tema, self, checkable=True)
            if tema == self.current_theme:
                tema_eylemi.setChecked(True)
            tema_eylemi.triggered.connect(self.tema_degistir)
            tema_grubu.addAction(tema_eylemi)
            tema_menusu.addAction(tema_eylemi)
        arac_cubugu.addAction(tema_menusu.menuAction())

        spotify_butonu = QAction(self.translations[self.languages[self.current_language]]['spotify'], self)
        spotify_butonu.triggered.connect(lambda: self.tarayici.setUrl(QUrl('https://open.spotify.com')))
        arac_cubugu.addAction(spotify_butonu)

        youtube_butonu = QAction(self.translations[self.languages[self.current_language]]['youtube'], self)
        youtube_butonu.triggered.connect(lambda: self.tarayici.setUrl(QUrl('https://www.youtube.com')))
        arac_cubugu.addAction(youtube_butonu)

        steam_butonu = QAction(self.translations[self.languages[self.current_language]]['steam'], self)
        steam_butonu.triggered.connect(lambda: self.tarayici.setUrl(QUrl('https://store.steampowered.com')))
        arac_cubugu.addAction(steam_butonu)

        dil_menusu = QMenu('Dil', self)
        dil_grubu = QActionGroup(self)
        for dil in self.languages:
            dil_eylemi = QAction(dil, self, checkable=True)
            if dil == self.current_language:
                dil_eylemi.setChecked(True)
            dil_eylemi.triggered.connect(self.dil_degistir)
            dil_grubu.addAction(dil_eylemi)
            dil_menusu.addAction(dil_eylemi)
        arac_cubugu.addAction(dil_menusu.menuAction())

        self.tarayici.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.tarayici.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)

    def url_git(self):
        url = self.url_cubugu.text()
        if not url.startswith('http'):
            url = self.current_search_engine + url
        self.tarayici.setUrl(QUrl(url))

    def url_guncelle(self, q):
        self.url_cubugu.setText(q.toString())

    def arama_motoru_degistir(self):
        self.current_search_engine = self.arama_motoru_secimi.currentData()
    
    def tema_degistir(self):
        eylem = self.sender()
        self.current_theme = eylem.text()
        tema_stili = self.themes[self.current_theme]
        if tema_stili == 'dark':
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
            self.url_cubugu.setStyleSheet("background-color: #555555; color: white;")
        else:
            self.setStyleSheet("background-color: white; color: black;")
            self.url_cubugu.setStyleSheet("background-color: #ffffff; color: black;")

    def dil_degistir(self):
        eylem = self.sender()
        self.current_language = eylem.text()
        self.geri_butonu.setText(self.translations[self.languages[self.current_language]]['back'])
        self.ileri_butonu.setText(self.translations[self.languages[self.current_language]]['forward'])
        self.yenile_butonu.setText(self.translations[self.languages[self.current_language]]['refresh'])
        self.url_cubugu.setPlaceholderText(self.translations[self.languages[self.current_language]]['search'])
        tema_menusu_action = self.findChild(QAction, self.translations[self.languages[self.current_language]]['theme'])
        if tema_menusu_action:
            tema_menusu_action.setText(self.translations[self.languages[self.current_language]]['theme'])
        spotify_butonu_action = self.findChild(QAction, self.translations[self.languages[self.current_language]]['spotify'])
        if spotify_butonu_action:
            spotify_butonu_action.setText(self.translations[self.languages[self.current_language]]['spotify'])
        youtube_butonu_action = self.findChild(QAction, self.translations[self.languages[self.current_language]]['youtube'])
        if youtube_butonu_action:
            youtube_butonu_action.setText(self.translations[self.languages[self.current_language]]['youtube'])
        steam_butonu_action = self.findChild(QAction, self.translations[self.languages[self.current_language]]['steam'])
        if steam_butonu_action:
            steam_butonu_action.setText(self.translations[self.languages[self.current_language]]['steam'])

if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    pencere = Tarayici()
    pencere.show()
    sys.exit(uygulama.exec_())
