#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信定时消息发送工具
基于PyAutoGUI模拟键盘操作，支持毫秒级定时发送
"""

import sys
import os
import time
import threading
from datetime import datetime, timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# 检查并安装依赖
def check_dependencies():
    """检查并提示安装依赖"""
    missing = []
    try:
        import pyautogui
    except ImportError:
        missing.append("pyautogui")
    try:
        import pyperclip
    except ImportError:
        missing.append("pyperclip")
    try:
        import pywinauto
    except ImportError:
        missing.append("pywinauto")
    try:
        import ntplib
    except ImportError:
        missing.append("ntplib")
    
    if missing:
        msg = f"缺少依赖库: {', '.join(missing)}\n\n请运行以下命令安装:\npip install {' '.join(missing)}"
        print(msg)
        return False
    return True

if not check_dependencies():
    sys.exit(1)

import pyautogui
import pyperclip
import ntplib


class TimeCalibrator:
    """时间校准器"""
    
    def __init__(self):
        self.offset = 0  # 时间偏差（秒）
        
    def calibrate(self):
        """
        使用NTP协议校准时间
        返回：时间偏差（秒），正数表示本地时间快，负数表示慢
        """
        try:
            client = ntplib.NTPClient()
            # 尝试多个NTP服务器
            servers = ['pool.ntp.org', 'time.windows.com', 'cn.pool.ntp.org']
            
            for server in servers:
                try:
                    response = client.request(server, timeout=2)
                    self.offset = response.offset
                    return self.offset
                except:
                    continue
                    
            # 如果NTP都失败，使用HTTP方式
            return self._http_calibrate()
            
        except Exception as e:
            print(f"时间校准失败: {e}")
            return 0
    
    def _http_calibrate(self):
        """使用HTTP请求校准时间（备用方案）"""
        try:
            import requests
            response = requests.head('https://www.baidu.com', timeout=3)
            server_time_str = response.headers.get('Date')
            if server_time_str:
                from email.utils import parsedate_to_datetime
                from datetime import timezone
                server_time = parsedate_to_datetime(server_time_str)
                # 转换为本地时间进行比较
                local_time = datetime.now(timezone.utc)
                self.offset = (server_time - local_time).total_seconds()
                return self.offset
        except Exception as e:
            print(f"HTTP校准失败: {e}")
        return 0
    
    def get_adjusted_time(self):
        """获取校准后的当前时间"""
        return datetime.now() + timedelta(seconds=self.offset)


class WeChatOperator:
    """微信操作类"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True  # 启用故障安全
        pyautogui.PAUSE = 0.01     # 操作间隔10ms
        
    def find_and_open_chat(self, contact_name, max_retry=3):
        """
        查找并打开聊天窗口（带重试）
        步骤：Ctrl+F → 输入名称 → 等待 → 回车
        返回：是否成功
        """
        for attempt in range(max_retry):
            try:
                # 激活微信窗口
                if not self._activate_wechat():
                    time.sleep(0.5)
                    continue
                
                # 打开搜索（Ctrl+F）
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(0.3)
                
                # 清空搜索框
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('delete')
                time.sleep(0.1)
                
                # 输入联系人名称
                pyperclip.copy(contact_name)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(1.0)  # 等待搜索结果
                
                # 直接回车打开第一个搜索结果
                pyautogui.press('enter')
                time.sleep(0.5)
                
                return True
                
            except Exception as e:
                print(f"打开聊天窗口失败 (尝试 {attempt+1}/{max_retry}): {e}")
                time.sleep(0.5)
        
        return False
    
    def prepare_message(self, message):
        """
        准备消息（输入但不发送）
        使用剪贴板支持中文
        """
        try:
            # 获取微信窗口位置，计算输入框相对坐标
            import win32gui
            
            # 找到微信窗口（标题为"微信"）
            hwnd = win32gui.FindWindow(None, "微信")
            
            if hwnd == 0:
                print("未找到微信窗口")
                return False
            
            # 获取窗口位置
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            
            # 计算输入框位置：窗口中央，底部往上100像素
            click_x = left + width // 2
            click_y = bottom - 100
            
            # 点击输入框
            pyautogui.click(click_x, click_y)
            time.sleep(0.1)
            
            # 清空输入框
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.1)
            
            # 使用剪贴板粘贴（支持中文）
            pyperclip.copy(message)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
                
            return True
            
        except Exception as e:
            print(f"准备消息失败: {e}")
            return False
    
    def send_at_precise_time(self, target_time, calibrator):
        """
        在精确时间点发送消息，返回偏差（毫秒）
        """
        try:
            # 忙等待直到目标时间
            while True:
                now = calibrator.get_adjusted_time()
                
                if now >= target_time:
                    break
                
                # 动态调整睡眠策略
                remaining = (target_time - now).total_seconds()
                
                if remaining > 1.0:
                    time.sleep(0.1)
                elif remaining > 0.1:
                    time.sleep(0.01)
                elif remaining > 0.005:
                    time.sleep(0.001)
                # 小于5ms时忙等待
            
            # 执行发送
            pyautogui.press('enter')
            
            # 计算偏差（实际发送时间 - 目标时间）
            actual_time = calibrator.get_adjusted_time()
            deviation = (actual_time - target_time).total_seconds() * 1000  # 转为毫秒
            
            return True, deviation
            
        except Exception as e:
            print(f"发送失败: {e}")
            return False, 0
    
    def _activate_wechat(self):
        """激活微信窗口到前台"""
        try:
            import pywinauto
            
            # 尝试找到微信窗口
            try:
                app = pywinauto.Application().connect(title_re="微信", timeout=2)
                window = app.window(title_re="微信")
                window.set_focus()
                time.sleep(0.3)
                return True
            except:
                pass
            
            # 备用：使用Alt+Tab切换
            pyautogui.keyDown('alt')
            pyautogui.keyDown('tab')
            pyautogui.keyUp('tab')
            pyautogui.keyUp('alt')
            time.sleep(0.3)
            
            return True
            
        except Exception as e:
            print(f"激活微信窗口失败: {e}")
            return False


class TaskScheduler(QObject):
    """任务调度器"""
    
    # 信号定义
    task_started = pyqtSignal(int, str)  # task_id, message
    task_completed = pyqtSignal(int, str)  # task_id, message
    task_error = pyqtSignal(int, str)  # task_id, error
    log_message = pyqtSignal(str)  # log message
    
    def __init__(self, calibrator):
        super().__init__()
        self.calibrator = calibrator
        self.tasks = []
        self.threads = {}
        self.running = False
        
    def add_task(self, contact, target_time, message):
        """添加定时任务"""
        task = {
            'id': len(self.tasks),
            'contact': contact,
            'target_time': target_time,
            'message': message,
            'status': 'pending',  # pending/running/completed/cancelled/error
            'created_at': datetime.now()
        }
        self.tasks.append(task)
        return task['id']
    
    def start_task(self, task_id):
        """启动指定任务"""
        if task_id >= len(self.tasks):
            return False
            
        task = self.tasks[task_id]
        if task['status'] != 'pending':
            return False
        
        # 创建线程
        thread = threading.Thread(
            target=self._execute_task,
            args=(task,),
            name=f"Task-{task_id}",
            daemon=True
        )
        thread.start()
        
        self.threads[task_id] = thread
        task['status'] = 'running'
        self.task_started.emit(task_id, f"开始执行任务: {task['contact']}")
        
        return True
    
    def start_all_pending(self):
        """启动所有待执行的任务"""
        count = 0
        for task in self.tasks:
            if task['status'] == 'pending':
                if self.start_task(task['id']):
                    count += 1
        return count
    
    def cancel_task(self, task_id):
        """取消任务"""
        if task_id < len(self.tasks):
            task = self.tasks[task_id]
            if task['status'] in ['pending', 'running']:
                task['status'] = 'cancelled'
                return True
        return False
    
    def _execute_task(self, task):
        """执行任务（在线程中运行）"""
        try:
            operator = WeChatOperator()
            
            # 计算准备时间（提前10秒）
            prepare_time = task['target_time'] - timedelta(seconds=10)
            
            # 等待到准备时间
            self.log_message.emit(f"[{task['contact']}] 等待准备时间...")
            while self.calibrator.get_adjusted_time() < prepare_time:
                if task['status'] == 'cancelled':
                    self.log_message.emit(f"[{task['contact']}] 任务已取消")
                    return
                time.sleep(0.1)
            
            # 准备阶段
            self.log_message.emit(f"[{task['contact']}] 正在准备...")
            if not operator.find_and_open_chat(task['contact']):
                task['status'] = 'error'
                self.task_error.emit(task['id'], f"无法打开聊天窗口: {task['contact']}")
                return
            
            if not operator.prepare_message(task['message']):
                task['status'] = 'error'
                self.task_error.emit(task['id'], "准备消息失败")
                return
            
            # 精确等待到发送时间
            self.log_message.emit(f"[{task['contact']}] 等待卡点发送...")
            success, deviation = operator.send_at_precise_time(task['target_time'], self.calibrator)
            if success:
                task['status'] = 'completed'
                self.task_completed.emit(task['id'], f"发送成功: {task['contact']}")
                self.log_message.emit(f"[{task['contact']}] ✓ 发送成功！偏差: {deviation:.1f}ms")
            else:
                task['status'] = 'error'
                self.task_error.emit(task['id'], "发送失败")
                
        except Exception as e:
            task['status'] = 'error'
            error_msg = str(e)
            self.task_error.emit(task['id'], error_msg)
            self.log_message.emit(f"[{task['contact']}] ✗ 错误: {error_msg}")


class WeChatTimerGUI(QMainWindow):
    """微信定时消息发送器 - GUI主窗口"""
    
    def __init__(self):
        super().__init__()
        
        self.calibrator = TimeCalibrator()
        self.scheduler = TaskScheduler(self.calibrator)
        
        # 连接信号
        self.scheduler.task_started.connect(self.on_task_started)
        self.scheduler.task_completed.connect(self.on_task_completed)
        self.scheduler.task_error.connect(self.on_task_error)
        self.scheduler.log_message.connect(self.on_log_message)
        
        self.initUI()
        
        # 启动后自动校准时间
        QTimer.singleShot(500, self.on_calibrate)
    
    def initUI(self):
        """初始化界面"""
        self.setWindowTitle("微信定时消息发送器")
        self.setGeometry(100, 100, 650, 800)
        
        # 设置窗口图标
        self.setWindowIcon(QIcon('wechat_timer.ico'))
        
        # 主布局
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        
        # 1. 时间校准区域
        self.create_calibration_section(layout)
        
        # 2. 任务输入区域
        self.create_input_section(layout)
        
        # 3. 按钮区域
        self.create_button_section(layout)
        
        # 4. 任务列表
        self.create_task_list(layout)
        
        # 5. 日志区域
        self.create_log_section(layout)
        
        # 状态栏
        self.statusBar().showMessage("就绪")
    
    def create_calibration_section(self, parent_layout):
        """时间校准区域"""
        group = QGroupBox("时间校准")
        layout = QHBoxLayout(group)
        
        self.calibration_label = QLabel("未校准")
        self.calibration_label.setStyleSheet("color: red; font-weight: bold;")
        
        calibrate_btn = QPushButton("重新校准")
        calibrate_btn.setToolTip("同步网络时间，确保发送精度")
        calibrate_btn.clicked.connect(self.on_calibrate)
        
        layout.addWidget(self.calibration_label)
        layout.addStretch()
        layout.addWidget(calibrate_btn)
        
        parent_layout.addWidget(group)
    
    def create_input_section(self, parent_layout):
        """任务输入区域"""
        group = QGroupBox("新建任务")
        layout = QFormLayout(group)
        
        # 联系人输入
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("输入联系人或群聊名称（如：张三、工作群）")
        
        # 时间输入
        self.time_input = QDateTimeEdit()
        self.time_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.time_input.setDateTime(QDateTime.currentDateTime().addSecs(60))
        self.time_input.setCalendarPopup(True)
        
        # 消息内容
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("输入要发送的消息内容...")
        self.message_input.setMaximumHeight(80)
        
        layout.addRow("联系人:", self.contact_input)
        layout.addRow("发送时间:", self.time_input)
        layout.addRow("消息内容:", self.message_input)
        
        parent_layout.addWidget(group)
    
    def create_button_section(self, parent_layout):
        """按钮区域"""
        layout = QHBoxLayout()
        
        add_btn = QPushButton("添加任务")
        add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        add_btn.clicked.connect(self.on_add_task)
        
        start_btn = QPushButton("启动所有任务")
        start_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        start_btn.clicked.connect(self.on_start_all)
        
        cancel_btn = QPushButton("取消并删除")
        cancel_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        cancel_btn.clicked.connect(self.on_cancel_selected)
        
        layout.addWidget(add_btn)
        layout.addWidget(start_btn)
        layout.addWidget(cancel_btn)
        
        parent_layout.addLayout(layout)
    
    def create_task_list(self, parent_layout):
        """任务列表"""
        group = QGroupBox('任务列表（选中后点击"取消并删除"可停止）')
        layout = QVBoxLayout(group)
        
        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.task_list.setMaximumHeight(150)
        
        layout.addWidget(self.task_list)
        parent_layout.addWidget(group)
    
    def create_log_section(self, parent_layout):
        """日志区域"""
        group = QGroupBox("运行日志")
        layout = QVBoxLayout(group)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        
        clear_btn = QPushButton("清空日志")
        clear_btn.clicked.connect(self.log_area.clear)
        
        layout.addWidget(self.log_area)
        layout.addWidget(clear_btn, alignment=Qt.AlignRight)
        
        parent_layout.addWidget(group)
    
    # === 事件处理 ===
    
    def on_calibrate(self):
        """校准时间"""
        self.calibration_label.setText("正在校准...")
        self.calibration_label.setStyleSheet("color: orange;")
        QApplication.processEvents()
        
        offset = self.calibrator.calibrate()
        
        if abs(offset) < 0.1:
            color = "green"
            status = "已校准"
        elif abs(offset) < 0.5:
            color = "orange"
            status = "偏差中等"
        else:
            color = "red"
            status = "偏差较大"
        
        self.calibration_label.setText(f"{status}  偏差: {offset:+.3f}秒")
        self.calibration_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        
        self.log(f"时间校准完成。偏差: {offset:+.3f}秒")
        self.statusBar().showMessage(f"时间校准完成，偏差: {offset:+.3f}秒", 3000)
    
    def on_add_task(self):
        """添加任务"""
        contact = self.contact_input.text().strip()
        target_time = self.time_input.dateTime().toPyDateTime()
        message = self.message_input.toPlainText().strip()
        
        # 验证输入
        if not contact:
            QMessageBox.warning(self, "提示", "请填写联系人名称")
            return
        
        if not message:
            QMessageBox.warning(self, "提示", "请填写消息内容")
            return
        
        # 检查时间是否在未来
        if target_time <= datetime.now():
            QMessageBox.warning(self, "提示", "发送时间必须在未来")
            return
        
        # 添加任务
        task_id = self.scheduler.add_task(contact, target_time, message)
        
        # 添加到列表显示
        item_text = f"[{task_id}] {contact} | {target_time.strftime('%Y-%m-%d %H:%M:%S')} | {message[:20]}..."
        self.task_list.addItem(item_text)
        
        self.log(f"添加任务 #{task_id}: {contact}")
        self.statusBar().showMessage(f"已添加任务 #{task_id}", 2000)
        
        # 清空输入（保留联系人）
        self.message_input.clear()
    
    def on_start_all(self):
        """启动所有任务"""
        count = self.scheduler.start_all_pending()
        
        if count > 0:
            self.log(f"启动了 {count} 个任务")
            self.statusBar().showMessage(f"已启动 {count} 个任务", 3000)
            QMessageBox.information(self, "提示", f"已启动 {count} 个任务\n请确保微信窗口已打开")
        else:
            QMessageBox.information(self, "提示", "没有待执行的任务")
    
    def on_cancel_selected(self):
        """取消选中的任务"""
        current_row = self.task_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "提示", "请先选择要取消的任务")
            return
        
        # 从列表中移除
        self.task_list.takeItem(current_row)
        
        # 取消任务
        if self.scheduler.cancel_task(current_row):
            self.log(f"取消任务 #{current_row}")
            self.statusBar().showMessage(f"已取消任务 #{current_row}", 2000)
    
    # === 信号处理 ===
    
    def on_task_started(self, task_id, message):
        """任务开始"""
        self.log(message)
    
    def on_task_completed(self, task_id, message):
        """任务完成"""
        self.log(message)
        self.statusBar().showMessage(message, 3000)
    
    def on_task_error(self, task_id, error):
        """任务错误"""
        self.log(f"任务 #{task_id} 错误: {error}")
        QMessageBox.warning(self, "任务错误", f"任务 #{task_id} 失败:\n{error}")
    
    def on_log_message(self, message):
        """接收日志消息"""
        self.log(message)
    
    def log(self, message):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f"[{timestamp}] {message}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    window = WeChatTimerGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
