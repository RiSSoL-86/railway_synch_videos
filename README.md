# Описание.

## Проект Railway_Synch_Videos.

## Технологии:
* Python 3.9
* PyQt5 5.15.10
* Qt Designer
* Python-telegram-bot 13.7
* Pyscreenshot 3.1
* OpenCV
  
## Описание проекта

Пробный проект Railway_Synch_Videos представляет из себя медиапроигрыватель для синхронного просмотра видеоизображений с 4-х камер видеонаблюдения, расположенных на Ж/Д путях,
с возможностью выполнения скриншота видеоизображений и отправки их в telegram.

## Как запустить проект:

Для корректной работы медиапроигрывателя все действия необходимо выполнять без использования виртуального окружения.
Установку вспомогательных библиотек необходимо производить в default - пути.

* Клонировать репозиторий и перейти в него в командной строке:

        git clone git@github.com:RiSSoL-86/railway_synch_videos.git
        cd railway_synch_videos

* Установить вспомогательные библиотеки:

        python -m pip install --upgrade pip
        pip install PyQt5==5.15.10
        pip install pyscreenshot==3.1
        pip install python-telegram-bot==13.7
        pip install opencv-python

* В переменную SCREEN_RESOLUTION необходимо указать своё разрешение экрана и запустить проект, где нас встретит Видеоплеер:
![image](https://github.com/RiSSoL-86/railway_synch_videos/assets/110422516/aeaf9f33-01bb-4d71-a0fb-9b15adba609d)

* Нажимая на кнопки Камера 1, Камера 2, Камера 3, Камера 4 необходимо указать путь к Видеофайлам одинаковой продолжительности,
и нажимая на кнопки Аннотация 1, Аннотация 2, Аннотация 3, Аннотация 4 указать путь к файлам аннотаций.
При корректном указании медиафайла или файла аннотации кнопки меняют цвет на 'Зелёный':
![image](https://github.com/RiSSoL-86/railway_synch_videos/assets/110422516/3aa62af3-d101-4f15-b73d-0355b84914db)

* После подгрузки всех 4 видеофайлов и файлов аннотации к ним необходимо произвести синхронизацию видеофайлов по временным меткам,
нажатием на кнопку Синхронизировать видео:
![image](https://github.com/RiSSoL-86/railway_synch_videos/assets/110422516/d5d7313f-2c8c-4958-8a7b-d2bbbe4b51f1)

* Через непродолжительное время файлы синхронизируются и можно приступить к просмотру видеофайлов:
![image](https://github.com/RiSSoL-86/railway_synch_videos/assets/110422516/cee7abcc-e9d6-45da-aac4-84a6dc7be397)
![image](https://github.com/RiSSoL-86/railway_synch_videos/assets/110422516/7d65d540-2651-4ee7-988f-d9b49cb3b067)

* Для отправки скриншота видеоизображений необходимо в графу TelegramID указать Ваш 10-изначный telegtam ID и нажать кнопку Send,
в следствии чего Вам в телеграм придёт скриншот программы:
![image](https://github.com/RiSSoL-86/railway_synch_videos/assets/110422516/dc92bcc1-adda-4777-9ef8-fae084ab95c0)
  





