from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt
import sys
import serial
import serial.tools.list_ports


class ArduinoLEDController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Arduino LED Controller')
        self.resize(400, 200)
        
        self.arduino = None
        
        # 전체 레이아웃
        main_layout = QVBoxLayout()
        
        # 상단 제목 라벨
        title_label = QLabel("<h2>Hoyeon LED Controller</h2>")
        title_label.setAlignment(Qt.AlignCenter)

        title_label.setStyleSheet("""
            QLabel {
                background-color: #001f4d;
                color: white;
                font-size: 20px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)

        main_layout.addWidget(title_label)
        
        # 포트 선택 + 새로고침 부분
        port_layout = QHBoxLayout()
        
        self.port_combo = QComboBox()

        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_ports)
        
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_arduino)
        
        port_layout.addWidget(QLabel("Select Port:"))
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_btn)
        port_layout.addWidget(self.connect_btn)
        
        main_layout.addLayout(port_layout)
        self.refresh_ports()
        
        # LED 제어 부분
        led_layout = QHBoxLayout()
        
        self.led_combo = QComboBox()
        self.led_combo.addItems(["OFF", "RED", "GREEN", "BLUE", "RANDOM"])
        self.led_combo.currentTextChanged.connect(self.change_led)
        
        led_layout.addWidget(QLabel("LED Control:"))
        led_layout.addWidget(self.led_combo)
        
        main_layout.addLayout(led_layout)
        
        # 하단 종료 버튼 우측 정렬
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        exit_btn = QPushButton("종료")
        exit_btn.clicked.connect(self.close)
        
        bottom_layout.addWidget(exit_btn)
        
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        self.port_combo.clear()
        
        arduino_ports = []
        
        for port in ports:
            desc = port.description.lower()
            if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
                arduino_ports.append(port.device)
        
        if arduino_ports:
            self.port_combo.addItems(arduino_ports)
        else:
            self.port_combo.addItem("select an Arduino port")

        # Connect 버튼 초기화
        self.connect_btn.setText("Connect")
        self.connect_btn.setEnabled(True)
        self.connect_btn.setStyleSheet("")  # 스타일 초기화 (기본 스타일로 복귀)
    
    def connect_arduino(self):
        port = self.port_combo.currentText()

        if port == "아두이노를 연결해주세요":
            QMessageBox.warning(self, "경고", "먼저 아두이노를 연결하세요.")
            return

        if self.arduino and self.arduino.is_open:
            QMessageBox.information(self, "알림", "이미 연결되어 있습니다.")
            return

        try:
            self.arduino = serial.Serial(port, 9600, timeout=1)
            QMessageBox.information(self, "성공", f"{port}에 연결되었습니다.")

            # 버튼 텍스트 변경 및 비활성화
            self.connect_btn.setText("Connected")
            self.connect_btn.setEnabled(False)
            
            # 버튼 배경색 변경 (초록색 계열 예시)
            self.connect_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                }
            """)
        except Exception as e:
            QMessageBox.critical(self, "에러", f"연결 실패: {e}")

    def change_led(self, selection):
        if not self.arduino or not self.arduino.is_open:
            QMessageBox.warning(self, "경고", "먼저 아두이노를 연결하세요.")
            # 콤보박스 값을 OFF로 강제 변경 (시그널 차단 후 설정)
            self.led_combo.blockSignals(True)
            self.led_combo.setCurrentText("OFF")
            self.led_combo.blockSignals(False)
            return
        
        if selection == "OFF":
            self.arduino.write(b'0')
        elif selection == "RED":
            self.arduino.write(b'1')
        elif selection == "GREEN":
            self.arduino.write(b'2')
        elif selection == "BLUE":
            self.arduino.write(b'3')
        elif selection == "RANDOM":
            self.arduino.write(b'4')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArduinoLEDController()
    window.show()
    sys.exit(app.exec_())
