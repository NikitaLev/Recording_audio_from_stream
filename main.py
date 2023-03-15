from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication
import pyaudio
import wave

list_device = {}

Form, Window = uic.loadUiType("Recording.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)


class TestThread(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.running = False  # Флаг выполнения
        self.count = 0
        self.input_device_index = 2

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        frames = []
        chunk = 1024  # Запись кусками по 1024 сэмпла
        sample_format = pyaudio.paInt16  # 16 бит на выборку
        channels = 2
        rate = 44100  # Запись со скоростью 44100 выборок(samples) в секунду
        filename = "output_sound.wav"
        p = pyaudio.PyAudio()
        print('device', self.input_device_index)
        stream = p.open(format=sample_format,
                             channels=channels,
                             rate=rate,
                             frames_per_buffer=chunk,
                             input_device_index=self.input_device_index,  # индекс устройства с которого будет идти запись звука
                             input=True)
        print(1)
        while self.running:   # Проверяем значение флага
            data2 = stream.read(chunk)
            frames.append(data2)
            #print(self.count,  self.running)

        print(9)
        stream.stop_stream()
        stream.close()
        print(10)

        p.terminate()
        print(11)
        print('Finished recording!')
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
"""            
            self.count += 1
            self.sleep(1)     # Имитируем процесс
            print(self.count)
"""


testThread = TestThread()


async def record():
    timer = 0


def start_record():
    print(form.comboBox.currentText())
    print(list_device.get(form.comboBox.currentText()))


def on_stop(self):
    testThread.stop() # Изменяем флаг выполнения


def on_start(self):
    print('device', list_device.get(form.comboBox.currentText()))
    if not testThread.isRunning():
        testThread.input_device_index = list_device.get(form.comboBox.currentText())
        testThread.start()
        print(7)


if __name__ == '__main__':
    p = pyaudio.PyAudio()
    print(u'', p.get_default_input_device_info())
    list = []
    for i in range(p.get_device_count()):
        data = {p.get_device_info_by_index(i)['name']: p.get_device_info_by_index(i)['index']}
        #list_device.__setitem__(p.get_device_info_by_index(i)['name'], p.get_device_info_by_index(i)['index'])
        if not p.get_device_info_by_index(i)['name'] in list_device:
            list_device[p.get_device_info_by_index(i)['name']] = p.get_device_info_by_index(i)['index']
        list.append(p.get_device_info_by_index(i)['name'])
        print(i, p.get_device_info_by_index(i))
    print(list_device)
    for i in list_device:
        print(i)

    window.show()

    form.comboBox.addItems(list_device)

    form.pushButton.clicked.connect(on_start)
    form.pushButton_2.clicked.connect(on_stop)
    app.exec()
