import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QPushButton, 
                            QSlider, QLineEdit, QTextEdit, QGroupBox, 
                            QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt, QTimer


class MotorControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("步进电机控制系统")
        self.setGeometry(100, 100, 800, 600)
        
        # 串口对象
        self.ser = None
        self.is_connected = False
        
        # 电机参数
        self.motor1_mode = 0  # 0=停止, 4=正向, 5=反向
        self.motor1_speed = 0  # 0-100
        self.motor2_mode = 0
        self.motor2_speed = 0
        self.motor3_mode = 0  # 0=停止, 1=运行
        self.motor3_speed = 0
        self.motor3_max = 0  # 0-999
        
        # 初始化界面
        self.init_ui()
        
        # 定时刷新串口列表
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_serial_ports)
        self.timer.start(2000)  # 每2秒刷新一次
        
        # 初始化串口列表
        self.refresh_serial_ports()
    
    def init_ui(self):
        # 主窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 串口设置区域
        serial_group = QGroupBox("串口设置")
        serial_layout = QFormLayout()
        
        self.port_combo = QComboBox()
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baud_combo.setCurrentText("9600")
        
        self.connect_btn = QPushButton("连接")
        self.connect_btn.clicked.connect(self.toggle_connection)
        
        serial_layout.addRow("串口端口:", self.port_combo)
        serial_layout.addRow("波特率:", self.baud_combo)
        serial_layout.addRow("", self.connect_btn)
        serial_group.setLayout(serial_layout)
        
        # 电机控制区域
        motor_group = QGroupBox("电机控制")
        motor_layout = QVBoxLayout()
        
        # 电机1控制
        motor1_box = QGroupBox("电机1")
        motor1_layout = QFormLayout()
        
        self.motor1_mode_combo = QComboBox()
        self.motor1_mode_combo.addItems(["停止", "正向", "反向"])
        self.motor1_mode_combo.currentIndexChanged.connect(self.update_motor1_mode)
        
        self.motor1_speed_slider = QSlider(Qt.Horizontal)
        self.motor1_speed_slider.setRange(0, 100)
        self.motor1_speed_slider.valueChanged.connect(self.update_motor1_speed)
        
        self.motor1_speed_label = QLabel("0")
        
        motor1_layout.addRow("模式:", self.motor1_mode_combo)
        motor1_layout.addRow("速度:", self.motor1_speed_slider)
        motor1_layout.addRow("当前速度:", self.motor1_speed_label)
        motor1_box.setLayout(motor1_layout)
        
        # 电机2控制
        motor2_box = QGroupBox("电机2")
        motor2_layout = QFormLayout()
        
        self.motor2_mode_combo = QComboBox()
        self.motor2_mode_combo.addItems(["停止", "正向", "反向"])
        self.motor2_mode_combo.currentIndexChanged.connect(self.update_motor2_mode)
        
        self.motor2_speed_slider = QSlider(Qt.Horizontal)
        self.motor2_speed_slider.setRange(0, 100)
        self.motor2_speed_slider.valueChanged.connect(self.update_motor2_speed)
        
        self.motor2_speed_label = QLabel("0")
        
        motor2_layout.addRow("模式:", self.motor2_mode_combo)
        motor2_layout.addRow("速度:", self.motor2_speed_slider)
        motor2_layout.addRow("当前速度:", self.motor2_speed_label)
        motor2_box.setLayout(motor2_layout)
        
        # 电机3控制
        motor3_box = QGroupBox("电机3")
        motor3_layout = QFormLayout()
        
        self.motor3_mode_combo = QComboBox()
        self.motor3_mode_combo.addItems(["停止", "运行"])
        self.motor3_mode_combo.currentIndexChanged.connect(self.update_motor3_mode)
        
        self.motor3_speed_slider = QSlider(Qt.Horizontal)
        self.motor3_speed_slider.setRange(0, 100)
        self.motor3_speed_slider.valueChanged.connect(self.update_motor3_speed)
        
        self.motor3_speed_label = QLabel("0")
        
        self.motor3_max_edit = QLineEdit("0")
        self.motor3_max_edit.textChanged.connect(self.update_motor3_max)
        
        motor3_layout.addRow("模式:", self.motor3_mode_combo)
        motor3_layout.addRow("速度:", self.motor3_speed_slider)
        motor3_layout.addRow("当前速度:", self.motor3_speed_label)
        motor3_layout.addRow("最大行程:", self.motor3_max_edit)
        motor3_box.setLayout(motor3_layout)
        
        # 发送按钮
        self.send_btn = QPushButton("发送指令")
        self.send_btn.clicked.connect(self.send_command)
        
        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        
        # 添加到布局
        motor_layout.addWidget(motor1_box)
        motor_layout.addWidget(motor2_box)
        motor_layout.addWidget(motor3_box)
        motor_layout.addWidget(self.send_btn)
        motor_layout.addWidget(QLabel("状态信息:"))
        motor_layout.addWidget(self.status_text)
        motor_group.setLayout(motor_layout)
        
        # 主布局
        main_layout.addWidget(serial_group)
        main_layout.addWidget(motor_group)
    
    def refresh_serial_ports(self):
        """刷新可用串口列表"""
        current_port = self.port_combo.currentText()
        self.port_combo.clear()
        
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)
        
        if current_port:
            index = self.port_combo.findText(current_port)
            if index != -1:
                self.port_combo.setCurrentIndex(index)
    
    def toggle_connection(self):
        """切换串口连接状态"""
        if self.is_connected:
            # 断开连接
            try:
                self.ser.close()
                self.is_connected = False
                self.connect_btn.setText("连接")
                self.status_text.append("串口已断开")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"断开串口失败: {str(e)}")
        else:
            # 连接串口
            port = self.port_combo.currentText()
            baud = int(self.baud_combo.currentText())
            
            try:
                self.ser = serial.Serial(port, baud, timeout=1)
                self.is_connected = True
                self.connect_btn.setText("断开")
                self.status_text.append(f"串口已连接: {port} ({baud}bps)")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"连接串口失败: {str(e)}")
    
    def update_motor1_mode(self, index):
        """更新电机1模式"""
        self.motor1_mode = [0, 4, 5][index]
    
    def update_motor1_speed(self, value):
        """更新电机1速度"""
        self.motor1_speed = value
        self.motor1_speed_label.setText(str(value))
    
    def update_motor2_mode(self, index):
        """更新电机2模式"""
        self.motor2_mode = [0, 4, 5][index]
    
    def update_motor2_speed(self, value):
        """更新电机2速度"""
        self.motor2_speed = value
        self.motor2_speed_label.setText(str(value))
    
    def update_motor3_mode(self, index):
        """更新电机3模式"""
        self.motor3_mode = index
    
    def update_motor3_speed(self, value):
        """更新电机3速度"""
        self.motor3_speed = value
        self.motor3_speed_label.setText(str(value))
    
    def update_motor3_max(self, text):
        """更新电机3最大行程"""
        try:
            self.motor3_max = int(text)
            if self.motor3_max < 0:
                self.motor3_max = 0
                self.motor3_max_edit.setText("0")
            elif self.motor3_max > 999:
                self.motor3_max = 999
                self.motor3_max_edit.setText("999")
        except:
            self.motor3_max = 0
    
    def generate_command(self):
        """生成控制命令"""
        # 构造17字节命令
        # 格式: [电机1模式][电机1速度(3位)][电机2模式][电机2速度(3位)][电机3模式][电机3速度(3位)][电机3最大行程(3位)][保留(2位)]
        cmd = ""
        
        # 电机1模式 (1位)
        cmd += str(self.motor1_mode)
        # 电机1速度 (3位)
        cmd += f"{self.motor1_speed:03d}"
        
        # 电机2模式 (1位)
        cmd += str(self.motor2_mode)
        # 电机2速度 (3位)
        cmd += f"{self.motor2_speed:03d}"
        
        # 电机3模式 (1位)
        cmd += str(self.motor3_mode)
        # 电机3速度 (3位)
        cmd += f"{self.motor3_speed:03d}"
        
        # 电机3最大行程 (3位)
        cmd += f"{self.motor3_max:03d}"
        
        # 保留位 (2位)
        cmd += "00"
        
        # 确保长度为17
        if len(cmd) != 17:
            self.status_text.append(f"命令长度错误: {len(cmd)}")
            return None
        
        return cmd
    
    def send_command(self):
        """发送控制命令"""
        if not self.is_connected:
            QMessageBox.warning(self, "警告", "请先连接串口")
            return
        
        cmd = self.generate_command()
        if not cmd:
            return
        
        try:
            self.ser.write(cmd.encode())
            self.status_text.append(f"发送命令: {cmd}")
            
            # 读取Arduino返回的数据
            if self.ser.in_waiting:
                response = self.ser.readline().decode().strip()
                self.status_text.append(f"接收响应: {response}")
        except Exception as e:
            self.status_text.append(f"发送失败: {str(e)}")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.is_connected:
            try:
                self.ser.close()
            except:
                pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotorControlGUI()
    window.show()
    sys.exit(app.exec_())
