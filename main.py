import cv2
import pyscreenshot
import telegram
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QStyle, QMessageBox)

import os
import sys
import shutil

from images import res_rc  # для отображения фона MainWindow

SCREEN_RESOLUTION = '1920x1080'  # <--- Укажите своё разрешение экрана
TELEGRAM_TOKEN = '6325628094:AAGQgXOnMTdKVx_G3uHFxaSAkZbTAqdq2GQ'
BBOX = {'1920x1080': (575, 240, 1340, 660),
        '1440x1080': (335, 240, 1100, 660)}
FRAMESIZE, FPS = (1280, 720), 5
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
        self.Camera1.clicked.connect(lambda: self.open_media(self.Camera1))
        self.Annot1.clicked.connect(lambda: self.open_txt(self.Annot1))
        self.media2 = QMediaPlayer(self)
        self.media2.setVideoOutput(self.Video2)
        self.Camera2.clicked.connect(lambda: self.open_media(self.Camera2))
        self.Annot2.clicked.connect(lambda: self.open_txt(self.Annot2))
        self.media3 = QMediaPlayer(self)
        self.media3.setVideoOutput(self.Video3)
        self.Camera3.clicked.connect(lambda: self.open_media(self.Camera3))
        self.Annot3.clicked.connect(lambda: self.open_txt(self.Annot3))
        self.media4 = QMediaPlayer(self)
        self.media4.setVideoOutput(self.Video4)
        self.Camera4.clicked.connect(lambda: self.open_media(self.Camera4))
        self.Annot4.clicked.connect(lambda: self.open_txt(self.Annot4))
        self.media4.stateChanged.connect(self.play_btn_changed)
        self.media4.positionChanged.connect(self.position_changed_slider)
        self.media4.durationChanged.connect(self.duration_changed_slider)
        # настройка кнопки SynchBtn
        self.SynchBtn.clicked.connect(lambda: self.synch_videos())
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

    def open_media(self, widget):
        "Выбрать видеофайл"
        file = QFileDialog.getOpenFileName(
            self, 'Выберите видеофайл', '.',
            'Video File (*.mp4 *.flv *.ts *.mts *.avi)')
        if file:
            widget.setStyleSheet(
                'background-color: rgb(50, 255, 50);')
            shutil.copy(file[0], 'media/videos')

    def open_txt(self, widget):
        "Выбрать файл аннотации"
        file = QFileDialog.getOpenFileName(
            self, 'Выберите файл с аннотацией', '.',
            '.txt File (*.txt)')
        if file:
            widget.setStyleSheet(
                'background-color: rgb(50, 255, 50);')
            shutil.copy(file[0], 'media/annotations')

    def synch_videos(self):
        "Синхронизация 4 видео по временным меткам из файлов аннотации"
        def file_read(file):
            "Чтение данных из файла в generator"
            with open(f'media/annotations/{file}', 'r') as file:
                lines = file.readlines()
                return (line.strip() for line in lines)

        msg = QMessageBox()
        msg.setWindowTitle('Статус синхронизации:')
        msg.setText('Подождите окончания синхронизации видео...')
        msg.show()
        msg.exec_()
        # открываем видеозаписи и читаем к ним аннотации
        camera1, camera2, camera3, camera4 = (
            cv2.VideoCapture(
                f'media/videos/{file}') for file in os.listdir('media/videos'))
        annotation1, annotation2, annotation3, annotation4 = (
            file_read(file) for file in os.listdir('media/annotations'))
        # получаем общее кол-во кадров в самом маленьком видео из 4-х
        frame_count = min(camera1.get(cv2.CAP_PROP_FRAME_COUNT),
                          camera2.get(cv2.CAP_PROP_FRAME_COUNT),
                          camera3.get(cv2.CAP_PROP_FRAME_COUNT),
                          camera4.get(cv2.CAP_PROP_FRAME_COUNT))
        screen_annotation1 = float(next(annotation1))
        screen_annotation2 = float(next(annotation2))
        screen_annotation3 = float(next(annotation3))
        screen_annotation4 = float(next(annotation4))
        # создаём видеозаписыватели для записи видео из получившихся кадров
        frameSize, fps = (1280, 720), 5
        out1, out2, out3, out4 = (
            cv2.VideoWriter(f'media/new_videos/new - {i}.avi',
                            cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                            fps, frameSize) for i in range(1, 5))
        counter = 0
        while counter < frame_count:
            # 4-я камера будет ведущей, т.к. она имеет наибольшее первое
            # значение аннотации
            _, camera4_image = camera4.read()
            cv2.imwrite(
                f'media/frames/camera4/{screen_annotation4} - {counter}.jpg',
                camera4_image)
            out4.write(camera4_image)
            while screen_annotation1 < screen_annotation4:
                screen_annotation1 = float(annotation1.__next__())
                _, camera1_image = camera1.read()
            cv2.imwrite(
                f"media/frames/camera1/{screen_annotation1} - {counter}.jpg",
                camera1_image)
            out1.write(camera1_image)
            while screen_annotation2 < screen_annotation4:
                screen_annotation2 = float(annotation2.__next__())
                _, camera2_image = camera2.read()
            cv2.imwrite(
                f"media/frames/camera2/{screen_annotation2} - {counter}.jpg",
                camera2_image)
            out2.write(camera2_image)
            while screen_annotation3 < screen_annotation4:
                screen_annotation3 = float(annotation3.__next__())
                _, camera3_image = camera3.read()
            cv2.imwrite(
                f"media/frames/camera3/{screen_annotation3} - {counter}.jpg",
                camera3_image)
            out3.write(camera3_image)
            counter += 1
            screen_annotation4 = float(next(annotation4))
        camera1.release()
        camera2.release()
        camera3.release()
        camera4.release()
        out1.release()
        out2.release()
        out3.release()
        out4.release()
        cv2.destroyAllWindows()
        self.media1.setMedia(QMediaContent(
            QUrl.fromLocalFile('media/new_videos/new - 1.avi')))
        self.media2.setMedia(QMediaContent(
            QUrl.fromLocalFile('media/new_videos/new - 2.avi')))
        self.media3.setMedia(QMediaContent(
            QUrl.fromLocalFile('media/new_videos/new - 3.avi')))
        self.media4.setMedia(QMediaContent(
            QUrl.fromLocalFile('media/new_videos/new - 4.avi')))
        self.Play.setEnabled(True)
        msg.setText('Синхронизация видео выполнена успешно!')
        msg.show()
        msg.exec_()

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
            self.Annot1.setStyleSheet(color)
            self.Annot2.setStyleSheet(color)
            self.Annot3.setStyleSheet(color)
            self.Annot4.setStyleSheet(color)

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
