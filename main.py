import pyscreenshot
import telegram
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QStyle

import sys

from images import res_rc  # для отображения фона MainWindow

SCREEN_RESOLUTION = '1920x1080'  # <--- Укажите своё разрешение экрана

TELEGRAM_TOKEN = '6325628094:AAGQgXOnMTdKVx_G3uHFxaSAkZbTAqdq2GQ'
BBOX = {'1920x1080': (575, 240, 1340, 660),
        '1440x1080': (335, 240, 1100, 660)}

bot = telegram.Bot(token=TELEGRAM_TOKEN)


class MainWindow(QMainWindow):
    "Главное окно программы."
    def __init__(self):
        super().__init__()
        # загрузка окна проигрывателя из файла программы QtDesigner
        uic.loadUi('qtdesigner/window.ui', self)
        # настройка медиапроигрывателей 4шт.
        self.media1 = QMediaPlayer(self)
        self.media1.setVideoOutput(self.Video1)
        self.Camera1.clicked.connect(lambda: self.open(
            self.media1, self.Camera1))
        self.media1.stateChanged.connect(self.play_btn_changed)
        self.media1.positionChanged.connect(self.position_changed_slider)
        self.media1.durationChanged.connect(self.duration_changed_slider)
        self.media2 = QMediaPlayer(self)
        self.media2.setVideoOutput(self.Video2)
        self.Camera2.clicked.connect(lambda: self.open(
            self.media2, self.Camera2))
        self.media3 = QMediaPlayer(self)
        self.media3.setVideoOutput(self.Video3)
        self.Camera3.clicked.connect(lambda: self.open(
            self.media3, self.Camera3))
        self.media4 = QMediaPlayer(self)
        self.media4.setVideoOutput(self.Video4)
        self.Camera4.clicked.connect(lambda: self.open(
            self.media4, self.Camera4))
        # настройка кнопки Start/Stop
        self.Play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.Play.clicked.connect(self.plays)
        # настройка Slider
        self.Slider.sliderMoved.connect(self.set_position_slider)
        # настройка кнопок скорости воспроизведения
        self.Speed1.clicked.connect(lambda: self.set_play_rate(0.2))
        self.Speed2.clicked.connect(lambda: self.set_play_rate(1))
        self.Speed3.clicked.connect(lambda: self.set_play_rate(10))
        # настройка кнопки Send
        self.Send.clicked.connect(lambda: self.send_screenshot(
            self.LineEdit.text()))
        # Настройка фона главного окна
        self.Label.setStyleSheet(
            "background-image: url(:/images/background_image.png);")
        self.Label.setPixmap(QtGui.QPixmap(":/background_image.png"))
        self.Label.setScaledContents(True)

    def open(self, media, widget):
        "Выбрать видеофайл"
        file = QFileDialog.getOpenFileName(
            self, 'Выберите видеофайл', '.',
            'Video Files (*.mp4 *.flv *.ts *.mts *.avi)')
        if file:
            widget.setStyleSheet(
                'background-color: rgb(50, 255, 50);')
            media.setMedia(QMediaContent(QUrl.fromLocalFile(file[0])))
            self.Play.setEnabled(True)

    def plays(self):
        "Воспроизвести/остановить видео с 4-х камер"
        if self.media1.state() == QMediaPlayer.PlayingState:
            self.media1.pause()
            self.media2.pause()
            self.media3.pause()
            self.media4.pause()
        else:
            self.media1.play()
            self.media2.play()
            self.media3.play()
            self.media4.play()
            color = 'background-color: rgb(148, 171, 255);'
            self.Camera1.setStyleSheet(color)
            self.Camera2.setStyleSheet(color)
            self.Camera3.setStyleSheet(color)
            self.Camera4.setStyleSheet(color)

    def play_btn_changed(self):
        "Корректное отображение кнопки Start/Stop"
        if self.media1.state() == QMediaPlayer.PlayingState:
            self.Play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.Play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def set_position_slider(self, position):
        "Выбор расположения Slider"
        self.media1.setPosition(position)
        self.media2.setPosition(position)
        self.media3.setPosition(position)
        self.media4.setPosition(position)

    def position_changed_slider(self, position):
        "Смена позиции расположения Slider"
        self.Slider.setValue(position)

    def duration_changed_slider(self, duration):
        "Длина Slider"
        self.Slider.setRange(0, duration)

    def set_play_rate(self, speed):
        "Настройка кнопок скорости воспроизведения"
        self.media1.setPlaybackRate(speed)
        self.media2.setPlaybackRate(speed)
        self.media3.setPlaybackRate(speed)
        self.media4.setPlaybackRate(speed)

    def send_screenshot(self, telegram_id):
        "Отправка скриншота в телеграм"
        image = pyscreenshot.grab(bbox=BBOX[SCREEN_RESOLUTION])
        image.save('screenshots/screenshot.png')
        try:
            bot.send_photo(telegram_id, photo=open(
                           'screenshots/screenshot.png', 'rb'))
        except ValueError('Error Telegram ID!!!'):
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
