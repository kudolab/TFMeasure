#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# ######################################################################
# 各種伝達関数測定用GUIツール
#
# Ryota Shimokawara (sr17805@tomakomai.kosen-ac.jp)
# 2018
# ######################################################################
# 206-207行目のファイル名変更及びITD_checkのエラー対処のためmeasure.pyも変更 @2019.5.23
# ######################################################################


import os
import re
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import measure
import rpi_client

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # このスクリプトのパス


class Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 測定データ保存先
        self.label_Save = QLabel('Save Directory:', self)
        self.edit_Save = QLineEdit(self)
        self.edit_Save.setFocusPolicy(Qt.ClickFocus)
        self.edit_Save.setText(SCRIPT_DIR)
        self.btn_Save = QPushButton('Open', self)
        self.btn_Save.setStyleSheet('background-color:white; color:black;')
        self.btn_Save.clicked.connect(self.showDialog)

        # 測定モードの選択
        self.label_Mode = QLabel('Mode:', self)
        self.combo_Mode = QComboBox(self)
        self.combo_Mode.addItems(['RSTF', 'SSTF', 'LSTF', 'Mic_Ajust'])

        # ターゲット
        self.label_Output = QLabel('Target:', self)
        self.combo_Output = QComboBox(self)
        self.combo_Output.addItem("Headphones")

        # 被験者記入欄
        self.label_Sub = QLabel('subject:', self)
        self.edit_Sub = QLineEdit(self)

        # 同期化算数記入欄
        self.label_averaging_time = QLabel('Avaraging Times:', self)
        self.edit_averaging_time = QLineEdit(self)
        self.edit_averaging_time.setText("10")

        # 測定開始ボタン
        self.btn_Start = QPushButton('START', self)
        self.btn_Start.setStyleSheet('background-color:cyan; color:black;')
        self.btn_Start.setFont(QFont("", 40))

        # イメージ
        self.image1 = QLabel(self)
        self.image1.setScaledContents(True)
        self.image1.setPixmap(QPixmap(SCRIPT_DIR + "/.texture/RSTF.png"))

        # プロット切り替えボタン
        self.btn_pltChange = QPushButton('↔', self)
        self.btn_pltChange.setStyleSheet('background-color:white; color:black;')
        self.btn_pltChange.setFont(QFont("", 28))
        self.btn_pltChange.setHidden(True)
        self.btn_pltChange.clicked.connect(self.plotChange)

        # ログ
        self.label_log = QLabel('Log:', self)
        self.te_log = QTextEdit(self)
        self.te_log.setReadOnly(True)
        self.te_log.setStyleSheet('background-color:black;')
        self.te_log.setTextColor(QColor(0, 255, 0))
        self.te_log.setFontPointSize(16)

        # プロットウィンドウ
        self.figure1 = plt.figure(figsize=(9, 5), dpi=60)
        self.axes1 = self.figure1.add_subplot(111)
        self.axes1.tick_params(labelsize=15)
        self.canvas1 = FigureCanvas(self.figure1)
        self.canvas1.setParent(self)

        # プロットウィンドウ2
        self.figure2 = plt.figure(figsize=(9, 5), dpi=60)
        self.axes2 = self.figure2.add_subplot(111)
        self.axes2.tick_params(labelsize=15)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setParent(self)

        # ナビゲーションツール
        self.toolbar1 = NavigationToolbar(self.canvas1, self)
        self.toolbar1.setGeometry(800, 80, 20, 30)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        self.toolbar2.setGeometry(800, 390, 20, 30)

        self.btn_Start.clicked.connect(self.measure)
        # ウィジェットイベント
        self.combo_Mode.currentIndexChanged.connect(self.wiget_setting)

        self.wigets_layout()

    def showDialog(self):
        frame = QFileDialog.getExistingDirectory(self)
        if frame != "": self.edit_Save.setText(frame + '/')

        # 各ウィジェットの配置

    def wigets_layout(self):
        x1 = 20;
        y1 = 350;
        y2 = 380
        x2 = 150;
        y3 = 450;
        y4 = 480

        self.setGeometry(300, 300, 900, 800)  # ウィンドウサイズ
        self.image1.setGeometry(20, 60, 250, 250)
        self.label_Save.move(x1, 10)
        self.edit_Save.setGeometry(130, 10, 650, 20)
        self.btn_Save.setGeometry(800, 10, 80, 20)
        self.label_Mode.move(x1, y1)
        self.combo_Mode.setGeometry(x1 - 3, y2, 120, 30)
        self.label_Output.move(x2, y1)
        self.combo_Output.setGeometry(x2 - 3, y2, 140, 30)
        self.label_Sub.move(x1, y3)
        self.edit_Sub.setGeometry(x1, y4, 100, 20)
        self.label_averaging_time.move(x2, y3)
        self.edit_averaging_time.setGeometry(x2, y4, 100, 20)
        self.btn_Start.setGeometry(60, 540, 180, 80)
        self.label_log.move(50, 640)
        self.te_log.setGeometry(50, 670, 800, 120)
        self.canvas1.move(300, 50)
        self.canvas2.move(300, 360)
        self.btn_pltChange.setGeometry(860, 55, 30, 30)

    # 測定モードごとのウィジェットの設定
    def wiget_setting(self):
        self.combo_Output.clear()
        self.edit_Sub.setReadOnly(True)

        # RSTF
        if self.combo_Mode.currentIndex() is 0:
            self.combo_Output.addItem("Headphones")
            self.edit_Sub.setReadOnly(False)
            self.edit_averaging_time.setText("10")
            self.image1.setPixmap(QPixmap(SCRIPT_DIR + "/.texture/RSTF.png"))


        # SSTF
        elif self.combo_Mode.currentIndex() is 1:
            self.combo_Output.addItems(
                ['angle: 0-85', 'angle: 90-175', 'angle: 180-265', 'angle: 270-355', 'ITD_Check'])
            self.edit_Sub.setReadOnly(False)
            self.edit_averaging_time.setText("10")
            self.image1.setPixmap(QPixmap(SCRIPT_DIR + "/.texture/SSTF.png"))

        # LSTF
        elif self.combo_Mode.currentIndex() is 2:
            self.combo_Output.addItems('Speaker No.' + str(n) for n in range(1, 19))
            self.edit_Sub.clear()
            self.edit_averaging_time.setText("10")
            self.image1.setPixmap(QPixmap(SCRIPT_DIR + "/.texture/LSTF.png"))

        # MicAjust
        elif self.combo_Mode.currentIndex() is 3:
            self.combo_Output.addItem("Speaker No.1")
            self.edit_Sub.clear()
            self.image1.setPixmap(QPixmap(SCRIPT_DIR + ""))

    # 測定
    def measure(self):
        self.averaging_times = self.edit_averaging_time.text()
        self.speaker_index = self.combo_Output.currentIndex()
        self.subject = self.edit_Sub.text()
        self.outdir = self.edit_Save.text() + "/" + self.subject
        self.Reverse = False  # プロット切り替えスイッチ
        self.btn_pltChange.setHidden(False)

        # RSTF
        if self.combo_Mode.currentIndex() is 0:
            if self.averaging_times is "":
                QMessageBox.warning(self, "Message", u"SANnum is invalid or empty")
                return
            if self.subject is "":
                QMessageBox.warning(self, "Message", u"subject Name is empty")
                return
            measure.RSTF(self.subject, self.averaging_times, 1, 255, 3801, 4823, self.outdir)
            self.te_log.append('cinv_cRSTF_L.DDB and cinv_cRSTF_R.DDB are measured. ('
                               + datetime.now().strftime("%H:%M:%S") + ')')
            self.plotChange()

        # SSTF
        elif self.combo_Mode.currentIndex() is 1:
            self.btn_pltChange.setHidden(True)
            if not rpi_client.is_healthy():
                QMessageBox.warning(self, "Message", u"Speaker selector is not connecting.")
                return
            if self.averaging_times is "":
                QMessageBox.warning(self, "Message", u"SANnum is invalid or empty")
                return
            if self.subject is "":
                QMessageBox.warning(self, "Message", u"subject Name is empty")
                return
            if self.speaker_index is 4:
                rpi_client.put_speaker_num(1)
                measure.SSTF(self.subject, self.averaging_times, 'check', 150, 405, self.outdir)
                self.plot(self.outdir + '/SSTF/cSSTF_check_L.DDB'
                          ,
                          self.outdir + '/SSTF/cSSTF_check_R.DDB')  # /SSTF/cSSTF_000_R.DDBから/SSTF/cSSTF_check_R.DDBに名称変更
                return

            for n in range(18):
                angle = self.speaker_index * 90 + n * 5
                rpi_client.put_speaker_num(n + 1)
                measure.SSTF(self.subject, self.averaging_times, angle, 150, 405, self.outdir)
                self.te_log.append('SSTF_' + str(angle) + '_L.DDB and SSTF_'
                                   + str(angle) + '_R.DDB are measured. (' + datetime.now().strftime("%H:%M:%S") + ')')
                self.plot(self.outdir + '/SSTF/cSSTF_' + str(angle) + '_L.DDB'
                          , self.outdir + '/SSTF/cSSTF_' + str(angle) + '_R.DDB')
                self.canvas1.flush_events()
                self.canvas2.flush_events()

        # LSTF
        elif self.combo_Mode.currentIndex() is 2:
            if not rpi_client.is_healthy():
                QMessageBox.warning(self, "Message", u"Speaker selector is not connecting.")
                return
            if self.averaging_times is "":
                QMessageBox.warning(self, "Message", u"SANnum is invalid or empty")
                return
            rpi_client.put_speaker_num(self.speaker_index + 1)
            measure.LSTF(self.speaker_index + 1, self.averaging_times, 150, 405, 3800, 4823, self.edit_Save.text())
            self.te_log.append('/LSTF_' + str(self.speaker_index + 1) + '.DDB is measured. ('
                               + datetime.now().strftime("%H:%M:%S") + ')')
            self.plotChange()

        # MicAjust
        elif self.combo_Mode.currentIndex() is 3:
            rpi_client.put_speaker_num(1)
            measure.mic_ajust()
            self.te_log.append('rec_L.DDB and rec_R.DDB are measured. (' + datetime.now().strftime("%H:%M:%S") + ')')
            self.plotChange()

        # elif self.combo_Mode.currentIndex() is 4:
        #     cpyconv.closedloop()
        #     with open(SCRIPT_DIR+"/DOUKI_START", 'r') as douki_start: iodelay = douki_start.read()
        #     QMessageBox.about(self, "Message", "The I/O delay is "+iodelay+" sample")

    # データのプロット
    def plot(self, file_L, file_R):
        data_bin = open(file_L, 'rb').read()
        data = np.fromstring(data_bin, dtype=np.float64)
        if file_R != None:
            data_bin2 = open(file_R, 'rb').read()
            data2 = np.fromstring(data_bin2, dtype=np.float64)

        # プロット1
        self.axes1.clear()
        self.axes1.set_title('Impulse Response', fontsize=15)
        self.axes1.set_xlabel("Sample", fontsize=15)
        self.axes1.set_ylabel("Level", fontsize=15)
        self.axes1.plot(data, '-', label=re.search("(.*)/(.*)", file_L).group(2), alpha=0.4)
        if file_R != None:
            self.axes1.plot(data2, '-', label=re.search("(.*)/(.*)", file_R).group(2))
        self.axes1.legend(bbox_to_anchor=(0., 1.02, 1., .102), borderaxespad=-0.2)
        self.canvas1.draw()

        # プロット2
        self.axes2.clear()
        self.axes2.set_title('Frequency Characteristic', fontsize=15)
        self.axes2.set_xlabel("Frequency [Hz]", fontsize=15)
        self.axes2.set_ylabel("Amplitude [dB]", fontsize=15)
        self.axes2.set_xlim(100, 24000)
        self.axes2.set_xscale('log')
        N = 255
        x = np.fft.fftfreq(N * 2, d=1.0 / 48000) * 2
        freq = np.fft.fft(data[0:N])
        data_amplitude = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in freq]
        data_decibel = 10.0 * np.log10(data_amplitude)
        self.axes2.plot(x[0:N], data_decibel, '-', label=re.search("(.*)/(.*)", file_L).group(2), alpha=0.4)

        if file_R != None:
            freq2 = np.fft.fft(data2[0:N])
            data_amplitude2 = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in freq2]
            data_decibel2 = 10.0 * np.log10(data_amplitude2)
            self.axes2.plot(x[0:N], data_decibel2, '-', label=re.search("(.*)/(.*)", file_R).group(2))

        self.axes2.legend(bbox_to_anchor=(0., 1.02, 1., .102), borderaxespad=-0.2)
        self.canvas2.draw()

    def plotChange(self):
        if self.Reverse is False:
            # RSTF
            if self.combo_Mode.currentIndex() is 0:
                self.plot(self.outdir + '/RSTF/cRSTF_L.DDB'
                          , self.outdir + '/RSTF/cRSTF_R.DDB')
            # LSTF
            elif self.combo_Mode.currentIndex() is 2:
                self.plot(self.edit_Save.text() + '/LSTF/cLSTF_' + str(self.speaker_index + 1) + '.DDB', None)
            # MicAjust
            elif self.combo_Mode.currentIndex() is 3:
                self.plot('/tmp/rec_L.DDB', '/tmp/rec_R.DDB')
            self.Reverse = True

        elif self.Reverse is True:
            # RSTF
            if self.combo_Mode.currentIndex() is 0:
                self.plot(self.outdir + '/RSTF/cinv_cRSTF_L.DDB'
                          , self.outdir + '/RSTF/cinv_cRSTF_R.DDB')
            # LSTF
            elif self.combo_Mode.currentIndex() is 2:
                self.plot(self.edit_Save.text() + '/LSTF/cinv_cLSTF_' + str(self.speaker_index + 1) + '.DDB', None)
            # MicAjust
            elif self.combo_Mode.currentIndex() is 3:
                self.plot('/tmp/rec_R.DDB', '/tmp/rec_L.DDB')
            self.Reverse = False

    # ウィンドウ内の座標を表示
    def mousePressEvent(self, event):
        print('x=' + str(event.x()) + ', y=' + str(event.y()))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.setWindowTitle('TFMeasure')
    main.show()

    sys.exit(app.exec_())
