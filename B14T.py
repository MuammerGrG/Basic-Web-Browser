import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QComboBox, QMenu, QActionGroup, 
                             QVBoxLayout, QWidget, QDialog, QListWidget, QPushButton, QFormLayout, QLabel, QLineEdit)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, QSize

class KisayolYonetici(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Kısayol Yöneticisi')
        self.setGeometry(200, 200, 400, 300)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.kisayol_listesi = QListWidget(self)
        self.kisayol_listesi.addItems(self.parent().kisayollar.keys())
        layout.addWidget(self.kisayol_listesi)

        self.kisayol_ekle_layout = QFormLayout()
        self.url_edit = QLineEdit(self)
        self.ad_edit = QLineEdit(self)
        self.kisayol_ekle_layout.addRow(QLabel('Kısayol Adı:'), self.ad_edit)
        self.kisayol_ekle_layout.addRow(QLabel('URL:'), self.url_edit)

        self.ekle_buton = QPushButton('Kısayol Ekle', self)
        self.ekle_buton.clicked.connect(self.kisayol_ekle)
        self.kisayol_ekle_layout.addWidget(self.ekle_buton)

        self.sil_buton = QPushButton('Kısayol Sil', self)
        self.sil_buton.clicked.connect(self.kisayol_sil)
        self.kisayol_ekle_layout.addWidget(self.sil_buton)

        layout.addLayout(self.kisayol_ekle_layout)

    def kisayol_ekle(self):
        ad = self.ad_edit.text()
        url = self.url_edit.text()
        if ad and url:
            self.parent().kisayollar[ad] = url
            self.kisayol_listesi.addItem(ad)
            self.ad_edit.clear()
            self.url_edit.clear()
            self.parent().update_kisayol_menusu()

    def kisayol_sil(self):
        selected_item = self.kisayol_listesi.currentItem()
        if selected_item:
            ad = selected_item.text()
            del self.parent().kisayollar[ad]
            self.kisayol_listesi.takeItem(self.kisayol_listesi.row(selected_item))
            self.parent().update_kisayol_menusu()

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
                'manage_shortcuts': 'Kısayolları Yönet',
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
                'manage_shortcuts': 'Manage Shortcuts',
                'spotify': 'Spotify',
                'youtube': 'YouTube',
                'steam': 'Steam'
            }
        }

        self.kisayollar = {}  # Kısayolları tutacak bir sözlük
        
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

        self.geri_butonu = self.create_action('back', self.tarayici.back)
        self.ileri_butonu = self.create_action('forward', self.tarayici.forward)
        self.yenile_butonu = self.create_action('refresh', self.tarayici.reload)

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

        self.kisayol_yonetici_butonu = QAction(self.translations[self.languages[self.current_language]]['manage_shortcuts'], self)
        self.kisayol_yonetici_butonu.triggered.connect(self.open_kisayol_yonetici)
        arac_cubugu.addAction(self.kisayol_yonetici_butonu)

        arac_cubugu.addAction(self.create_action('spotify', lambda: self.tarayici.setUrl(QUrl('https://open.spotify.com'))))
        arac_cubugu.addAction(self.create_action('youtube', lambda: self.tarayici.setUrl(QUrl('https://www.youtube.com'))))
        arac_cubugu.addAction(self.create_action('steam', lambda: self.tarayici.setUrl(QUrl('https://store.steampowered.com'))))

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
        self.update_ui()

    def create_action(self, key, slot):
        action = QAction(self.translations[self.languages[self.current_language]][key], self)
        action.triggered.connect(slot)
        return action

    def update_ui(self):
        self.geri_butonu.setText(self.translations[self.languages[self.current_language]]['back'])
        self.ileri_butonu.setText(self.translations[self.languages[self.current_language]]['forward'])
        self.yenile_butonu.setText(self.translations[self.languages[self.current_language]]['refresh'])
        self.url_cubugu.setPlaceholderText(self.translations[self.languages[self.current_language]]['search'])
        tema_menusu = self.findChild(QMenu, self.translations[self.languages[self.current_language]]['theme'])
        if tema_menusu:
            tema_menusu.setTitle(self.translations[self.languages[self.current_language]]['theme'])
        for action in self.findChildren(QAction):
            if action.text() in self.translations[self.languages[self.current_language]].values():
                action.setText(self.translations[self.languages[self.current_language]].get(action.text(), action.text()))

    def open_kisayol_yonetici(self):
        self.kisayol_yonetici = KisayolYonetici(self)
        self.kisayol_yonetici.exec_()

    def update_kisayol_menusu(self):
        self.findChild(QToolBar).clear()
        for ad, url in self.kisayollar.items():
            kisayol_butonu = QAction(ad, self)
            kisayol_butonu.triggered.connect(lambda checked, u=url: self.tarayici.setUrl(QUrl(u)))
            self.findChild(QToolBar).addAction(kisayol_butonu)

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
        self.update_ui()

if __name__ == '__main__':
    uygulama = QApplication(sys.argv)
    pencere = Tarayici()
    pencere.show()
    sys.exit(uygulama.exec_())
