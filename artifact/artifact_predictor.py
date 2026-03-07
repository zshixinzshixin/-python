#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QTabWidget, QGroupBox, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# 导入配置
import config

# 词条数值定义 - 五星
FIVE_STAR_VALUES = {
    'f': ['f16', 'f19', 'f21', 'f23'],
    's': ['s209', 's239', 's269', 's299'],
    'g': ['g14', 'g16', 'g18', 'g19'],
    'F': ['F51', 'F58', 'F66', 'F73'],
    'S': ['S41', 'S47', 'S53', 'S58'],
    'G': ['G41', 'G47', 'G53', 'G58'],
    'j': ['j16', 'j19', 'j21', 'j23'],
    'c': ['c45', 'c52', 'c58', 'c65'],
    'b': ['b27', 'b31', 'b35', 'b39'],
    'B': ['B54', 'B62', 'B7', 'B78']
}

# 词条类型映射
type_map = {
    'f': 0, 's': 1, 'g': 2, 'F': 3, 'S': 4,
    'G': 5, 'j': 6, 'c': 7, 'b': 8, 'B': 9
}

# 词条数值定义 - 三星（根据参考图）
THREE_STAR_VALUES = {
    'f': ['f8', 'f9', 'f10', 'f11'],
    's': ['s100', 's115', 's129', 's143'],
    'g': ['g7', 'g8', 'g9', 'g10'],
    'F': ['F31', 'F35', 'F39', 'F44'],
    'S': ['S25', 'S28', 'S32', 'S35'],
    'G': ['G25', 'G28', 'G32', 'G35'],
    'j': ['j10', 'j11', 'j13', 'j14'],
    'c': ['c27', 'c31', 'c35', 'c39'],
    'b': ['b16', 'b19', 'b21', 'b23'],
    'B': ['B33', 'B37', 'B42', 'B47']
}

class DataManager:
    """数据管理类：负责JSON数据的保存、读取和导出"""

    def __init__(self, base_dir=None):
        if base_dir is None:
            # 优先使用当前工作目录，这样打包后数据会保存在exe所在目录
            base_dir = os.getcwd()
        self.base_dir = base_dir
        self.records_dir = os.path.join(base_dir, '强化记录')
        self.exports_dir = os.path.join(self.records_dir, 'exports')
        self.models_dir = os.path.join(self.records_dir, 'models')

        # 创建必要的文件夹
        self._ensure_directories()

    def _ensure_directories(self):
        """确保所有必要的文件夹存在"""
        for dir_path in [self.records_dir, self.exports_dir, self.models_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def _get_json_file_path(self):
        """获取带时间戳的JSON文件路径（精确到秒，避免重复）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.records_dir, f'record_{timestamp}.json')

    def load_records(self):
        """加载所有强化记录（合并所有日期的文件）"""
        all_records = []
        last_updated = ""

        # 遍历所有record_*.json文件
        for filename in os.listdir(self.records_dir):
            if filename.startswith('record_') and filename.endswith('.json'):
                filepath = os.path.join(self.records_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_records.extend(data.get("records", []))
                        if data.get("metadata", {}).get("last_updated", "") > last_updated:
                            last_updated = data["metadata"]["last_updated"]
                except Exception as e:
                    print(f"加载文件 {filename} 失败: {e}")

        return {
            "records": all_records,
            "metadata": {
                "total_records": len(all_records),
                "last_updated": last_updated
            }
        }

    def save_record(self, entries, artifact_type=""):
        """
        保存一条强化记录到当天的JSON文件
        entries: list of dict, 每个dict包含value, gear, star, type, order
        """
        json_file = self._get_json_file_path()

        # 加载当天已有的记录
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                data = {"records": [], "metadata": {"total_records": 0, "last_updated": ""}}
        else:
            data = {"records": [], "metadata": {"total_records": 0, "last_updated": ""}}

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "entries": entries,
            "artifact_type": artifact_type
        }

        data["records"].append(record)
        data["metadata"]["total_records"] = len(data["records"])
        data["metadata"]["last_updated"] = record["timestamp"]

        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, json_file
        except Exception as e:
            print(f"保存记录失败: {e}")
            return False, str(e)

    def get_record_count(self):
        """获取记录总数"""
        data = self.load_records()
        return data["metadata"]["total_records"]

    def export_to_excel(self):
        """导出到Excel文件"""
        try:
            import pandas as pd

            data = self.load_records()
            if not data["records"]:
                return False, "没有数据可导出"

            # 构建DataFrame
            rows = []
            for record in data["records"]:
                for entry in record["entries"]:
                    rows.append({
                        "时间戳": record["timestamp"],
                        "词条值": entry["value"],
                        "档位": entry["gear"],
                        "星级": entry["star"],
                        "词条类型": entry["type"],
                        "强化顺序": entry["order"]
                    })

            df = pd.DataFrame(rows)

            # 生成文件名
            filename = f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(self.exports_dir, filename)

            df.to_excel(filepath, index=False, engine='openpyxl')
            return True, filepath
        except Exception as e:
            return False, str(e)


class ArtifactPredictor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_tab = "five_star"
        self.model_data = None
        self.input_rows = []
        self.data_manager = DataManager()
        self.set_window_icon()
        self.initUI()
        self.load_model_data()
        self.update_data_status()

    def set_window_icon(self):
        """设置应用窗口图标（兼容PyInstaller打包）"""
        # PyInstaller打包后的路径处理
        if getattr(sys, 'frozen', False):
            # 打包后的exe运行环境
            base_path = sys._MEIPASS
        else:
            # 开发环境
            base_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(base_path, 'icon', 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"图标文件不存在: {icon_path}")

    def initUI(self):
        self.setWindowTitle("原神圣遗物词条预测工具")
        self.setGeometry(100, 100, 1400, 900) # 窗口大小

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # 左侧：多标签页输入区
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(5)

        self.tab_widget = QTabWidget()

        # 五星标签页
        five_star_tab = QWidget()
        five_star_layout = QVBoxLayout(five_star_tab)
        five_star_layout.setSpacing(5)
        self.init_five_star_panel(five_star_layout)

        # 三星标签页
        three_star_tab = QWidget()
        three_star_layout = QVBoxLayout(three_star_tab)
        three_star_layout.setSpacing(5)
        self.init_three_star_panel(three_star_layout)

        # 胚子标签页
        embryo_tab = QWidget()
        embryo_layout = QVBoxLayout(embryo_tab)
        embryo_layout.setSpacing(5)
        self.init_embryo_panel(embryo_layout)

        self.tab_widget.addTab(five_star_tab, "五星")
        self.tab_widget.addTab(three_star_tab, "三星")
        self.tab_widget.addTab(embryo_tab, "胚子")
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        left_layout.addWidget(self.tab_widget)
        main_layout.addWidget(left_panel, 1)

        # 中间：共用录入区（可滚动）
        middle_panel = QWidget()
        middle_layout = QVBoxLayout(middle_panel)
        middle_layout.setSpacing(5)

        # 顶部按钮行
        top_btn_layout = QHBoxLayout()
        clear_btn = QPushButton("清空记录")
        clear_btn.clicked.connect(self.on_clear_clicked)
        delete_last_btn = QPushButton("删除上条")
        delete_last_btn.clicked.connect(self.on_delete_last_clicked)
        top_btn_layout.addWidget(clear_btn)
        top_btn_layout.addWidget(delete_last_btn)
        middle_layout.addLayout(top_btn_layout)

        # 表头（固定在顶部，不滚动）
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(5, 2, 5, 2)
        header_layout.addWidget(QLabel("档位"), 1)
        header_layout.addWidget(QLabel("词条"), 2)
        header_layout.addWidget(QLabel("星级"), 1)
        header_layout.addWidget(QLabel("录入"), 1)
        middle_layout.addWidget(header_widget)

        # 录入区域（可滚动）
        self.input_scroll = QScrollArea()
        self.input_scroll.setWidgetResizable(True)
        self.input_container = QWidget()
        self.input_layout = QVBoxLayout(self.input_container)
        self.input_layout.setSpacing(2)
        self.input_layout.setAlignment(Qt.AlignTop)

        self.input_scroll.setWidget(self.input_container)
        middle_layout.addWidget(self.input_scroll)

        main_layout.addWidget(middle_panel, 1)

        # 右侧：共用预测结果区
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)

        # 预测模式选择
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("预测模式:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["统计模式", "深度学习模式"])
        self.mode_combo.setEnabled(False)  # 初始禁用深度学习模式
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        right_layout.addLayout(mode_layout)

        # 数据操作按钮
        data_btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存数据")
        save_btn.clicked.connect(self.on_save_data_clicked)
        export_btn = QPushButton("导出Excel")
        export_btn.clicked.connect(self.on_export_excel_clicked)
        train_btn = QPushButton("训练模型")
        train_btn.clicked.connect(self.on_train_model_clicked)
        self.train_btn = train_btn
        data_btn_layout.addWidget(save_btn)
        data_btn_layout.addWidget(export_btn)
        data_btn_layout.addWidget(train_btn)
        right_layout.addLayout(data_btn_layout)

        # 数据状态显示
        self.status_label = QLabel("记录数: 0 | 模型状态: 未训练")
        right_layout.addWidget(self.status_label)

        # 表1：概率表
        table1_group = QGroupBox("表1：预测下一次词条")
        table1_layout = QVBoxLayout(table1_group)
        self.table1 = QTableWidget(1, 10)
        self.table1.setHorizontalHeaderLabels(["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"])
        self.table1.setVerticalHeaderLabels(["概率%"])
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table1.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置固定高度：表头高度 + 一行数据高度 + 边框
        self.table1.setFixedHeight(self.table1.horizontalHeader().height() + 40)
        table1_layout.addWidget(self.table1)

        # Top-3推荐显示（深度学习模式）
        self.top3_label = QLabel("Top-3推荐: -")
        self.top3_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        table1_layout.addWidget(self.top3_label)

        # 统计模式Top-3推荐显示（仅在深度学习模式下显示用于对比）
        self.stats_top3_label = QLabel("")
        self.stats_top3_label.setStyleSheet("font-weight: bold; color: black;")
        table1_layout.addWidget(self.stats_top3_label)

        # 置信度显示
        self.confidence_label = QLabel("置信度: -")
        self.confidence_label.setStyleSheet("font-weight: bold;")
        table1_layout.addWidget(self.confidence_label)

        right_layout.addWidget(table1_group)

        # 表2：胚子概率表
        table2_group = QGroupBox("表2：胚子强化概率")
        table2_layout = QVBoxLayout(table2_group)
        self.table2 = QTableWidget(1, 4)
        self.table2.setHorizontalHeaderLabels(["-", "-", "-", "-"])
        self.table2.setVerticalHeaderLabels(["概率%"])
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table2.setFixedHeight(self.table2.horizontalHeader().height() + 40)
        table2_layout.addWidget(self.table2)

        # 添加伸缩因子，均匀分布空白
        table2_layout.addStretch(2)

        # 胚子强化建议（上半部分）
        self.embryo_advice_label = QLabel("强化建议: -")
        self.embryo_advice_label.setStyleSheet("font-weight: bold;")
        table2_layout.addWidget(self.embryo_advice_label)

        # 中间空白
        table2_layout.addStretch(1)

        # 风险度标签（下半部分）
        self.risk_label = QLabel("")
        self.risk_label.setStyleSheet("font-weight: bold;")
        table2_layout.addWidget(self.risk_label)

        table2_layout.addStretch(2)

        right_layout.addWidget(table2_group)

        main_layout.addWidget(right_panel, 2)

    def init_five_star_panel(self, layout):
        info_label = QLabel("录入五星词条(补词条、强化)。")
        layout.addWidget(info_label)

        button_grid = QGridLayout()
        button_grid.setSpacing(5)

        row = 0
        for type_key, values in FIVE_STAR_VALUES.items():
            for col, value in enumerate(values):
                btn = QPushButton(value)
                btn.setFixedSize(70, 45)
                gear = col + 1
                star_type = "5星"
                btn.clicked.connect(lambda checked, v=value, g=gear, s=star_type: self.on_entry_clicked(v, g, s))
                button_grid.addWidget(btn, row, col)
            row += 1

        layout.addLayout(button_grid)
        layout.addStretch()

    def init_three_star_panel(self, layout):
        info_label = QLabel("录入三星词条(补词条、强化)。")
        layout.addWidget(info_label)

        button_grid = QGridLayout()
        button_grid.setSpacing(5)

        row = 0
        for type_key, values in THREE_STAR_VALUES.items():
            for col, value in enumerate(values):
                btn = QPushButton(value)
                btn.setFixedSize(70, 45)
                gear = col + 1
                star_type = "3星"
                btn.clicked.connect(lambda checked, v=value, g=gear, s=star_type: self.on_entry_clicked(v, g, s))
                button_grid.addWidget(btn, row, col)
            row += 1

        layout.addLayout(button_grid)
        layout.addStretch()

    def init_embryo_panel(self, layout):
        """初始化胚子标签页：选择4个目标词条"""
        info_label = QLabel("选择胚子的4个词条（点击勾选）：")
        layout.addWidget(info_label)

        # 存储选中的胚子词条
        self.embryo_selected = []
        self.embryo_buttons = {}

        # 词条类型名称
        type_names = ['小防', '小生', '小攻', '大防', '大生', '大攻', '精通', '充能', '暴击', '暴伤']
        type_keys = ['f', 's', 'g', 'F', 'S', 'G', 'j', 'c', 'b', 'B']

        # 创建2行5列的勾选按钮网格
        button_grid = QGridLayout()
        button_grid.setSpacing(10)

        for i, (name, key) in enumerate(zip(type_names, type_keys)):
            row = i // 5
            col = i % 5

            btn = QPushButton(f"{name}\n({key})")
            btn.setFixedSize(80, 60)
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    border: 2px solid #ccc;
                    border-radius: 5px;
                }
                QPushButton:checked {
                    background-color: #4CAF50;
                    color: white;
                    border: 2px solid #45a049;
                }
            """)
            btn.clicked.connect(lambda checked, k=key, b=btn: self.on_embryo_type_clicked(k, b))
            button_grid.addWidget(btn, row, col)
            self.embryo_buttons[key] = btn

        layout.addLayout(button_grid)

        # 显示当前选择
        self.embryo_status_label = QLabel("已选择：0/4")
        self.embryo_status_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        layout.addWidget(self.embryo_status_label)

        # 确认和清空按钮
        btn_layout = QHBoxLayout()
        confirm_btn = QPushButton("确认胚子")
        confirm_btn.clicked.connect(self.on_embryo_confirm)
        clear_btn = QPushButton("清空选择")
        clear_btn.clicked.connect(self.on_embryo_clear)
        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(clear_btn)
        layout.addLayout(btn_layout)

        # 当前胚子显示
        self.embryo_current_label = QLabel("当前胚子：未设置")
        self.embryo_current_label.setStyleSheet("font-weight: bold; color: #FF5722;")
        layout.addWidget(self.embryo_current_label)

        layout.addStretch()

    def on_embryo_type_clicked(self, type_key, btn):
        """处理胚子词条点击"""
        if btn.isChecked():
            if len(self.embryo_selected) < 4:
                self.embryo_selected.append(type_key)
            else:
                btn.setChecked(False)
                QMessageBox.warning(self, "提示", "最多只能选择4个词条！")
        else:
            if type_key in self.embryo_selected:
                self.embryo_selected.remove(type_key)

        self.update_embryo_status()

    def update_embryo_status(self):
        """更新胚子选择状态显示"""
        count = len(self.embryo_selected)
        self.embryo_status_label.setText(f"已选择：{count}/4")

        # 显示已选择的词条名称
        type_names = {'f': '小防', 's': '小生', 'g': '小攻', 'F': '大防', 'S': '大生',
                     'G': '大攻', 'j': '精通', 'c': '充能', 'b': '暴击', 'B': '暴伤'}
        selected_names = [type_names.get(k, k) for k in self.embryo_selected]
        if selected_names:
            self.embryo_status_label.setText(f"已选择：{count}/4 - {', '.join(selected_names)}")

    def on_embryo_confirm(self):
        """确认胚子选择"""
        if len(self.embryo_selected) != 4:
            QMessageBox.warning(self, "提示", "请选择恰好4个词条！")
            return

        type_names = {'f': '小防', 's': '小生', 'g': '小攻', 'F': '大防', 'S': '大生',
                     'G': '大攻', 'j': '精通', 'c': '充能', 'b': '暴击', 'B': '暴伤'}
        selected_names = [type_names.get(k, k) for k in self.embryo_selected]
        self.embryo_current_label.setText(f"当前胚子：{' + '.join(selected_names)}")

        # 更新表2显示
        self.update_embryo_table()

    def on_embryo_clear(self):
        """清空胚子选择"""
        self.embryo_selected = []
        for btn in self.embryo_buttons.values():
            btn.setChecked(False)
        self.update_embryo_status()
        self.embryo_current_label.setText("当前胚子：未设置")
        self.clear_embryo_table()

    def on_tab_changed(self, index):
        tabs = ["five_star", "three_star", "embryo"]
        self.current_tab = tabs[index]

    def on_entry_clicked(self, value, gear, star):
        # 创建新行
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setSpacing(5)

        gear_label = QLabel(str(gear))
        value_label = QLabel(value)
        star_label = QLabel(star)
        order_label = QLabel(str(len(self.input_rows) + 1))

        row_layout.addWidget(gear_label, 1)
        row_layout.addWidget(value_label, 2)
        row_layout.addWidget(star_label, 1)
        row_layout.addWidget(order_label, 1)

        # 插入到最前面（最新词条在最上面）
        self.input_layout.insertWidget(0, row_widget)

        self.input_rows.insert(0, {
            'widget': row_widget,
            'gear': gear,
            'value': value,
            'star': star
        })

        # 滚动到顶部显示最新词条
        self.input_scroll.verticalScrollBar().setValue(0)

        self.predict()

    def on_delete_last_clicked(self):
        """删除最新一条录入的数据（最上面的一条）"""
        if self.input_rows:
            last_row = self.input_rows.pop(0)
            last_row['widget'].deleteLater()
            self.predict()

    def on_clear_clicked(self):
        for row in self.input_rows:
            row['widget'].deleteLater()
        self.input_rows = []
        self.clear_tables()

    def clear_tables(self):
        for col in range(10):
            self.table1.setItem(0, col, QTableWidgetItem(""))
        self.top3_label.setText("Top-3推荐: -")
        self.stats_top3_label.setText("")
        self.confidence_label.setText("置信度: -")
        self.confidence_label.setStyleSheet("font-weight: bold;")

    def update_embryo_table(self):
        """更新胚子概率表（表2）"""
        if len(self.embryo_selected) != 4:
            return

        try:
            # 获取当前预测概率
            probs_percent = None
            if len(self.input_rows) >= 3:
                use_dl = (self.mode_combo.currentText() == "深度学习模式" and
                         self.mode_combo.isEnabled())
                if use_dl:
                    last_3 = list(reversed(self.input_rows[:3]))
                    probs_percent = self.predict_with_dl_smart(last_3)
                else:
                    probs_percent = self.predict_with_stats_sliding()

            if probs_percent is None:
                return

            # 计算胚子词条的条件概率
            artifact_probs, total_prob = self.calc_artifact_probs(probs_percent, self.embryo_selected)

            # 更新表2表头
            type_names = {'f': '小防', 's': '小生', 'g': '小攻', 'F': '大防', 'S': '大生',
                         'G': '大攻', 'j': '精通', 'c': '充能', 'b': '暴击', 'B': '暴伤'}
            headers = [type_names.get(k, k) for k in self.embryo_selected]
            self.table2.setHorizontalHeaderLabels(headers)

            # 更新表2数据（条件概率）
            for col, key in enumerate(self.embryo_selected):
                type_idx = type_map[key]
                prob = artifact_probs[type_idx]
                self.table2.setItem(0, col, QTableWidgetItem(f"{prob:.1f}"))

            # 更新强化建议（区分目标词条和其他词条）
            # 定义词条分类
            target_types = {'b': '暴击', 'B': '暴伤'}  # 目标词条（想要）

            # 计算双暴概率（目标词条）
            target_prob = sum(artifact_probs.get(type_map[t], 0) for t in self.embryo_selected if t in target_types)
            # 歪率 = 100% - 双暴%（除了bB之外的所有）
            bad_prob = 100 - target_prob

            # 计算风险度（方案3：风险倍数）
            # 获取bB和非bB各自的概率
            bb_probs = {t: artifact_probs.get(type_map[t], 0) for t in self.embryo_selected if t in target_types}
            non_bb_probs = {t: artifact_probs.get(type_map[t], 0) for t in self.embryo_selected if t not in target_types}

            if bb_probs and non_bb_probs:
                bb_min_val = min(bb_probs.values())
                non_bb_max_val = max(non_bb_probs.values())
                risk_ratio = non_bb_max_val / bb_min_val if bb_min_val > 0 else float('inf')

                # 找出最危险的对比
                non_bb_max_type = max(non_bb_probs.items(), key=lambda x: x[1])[0]
                bb_min_type = min(bb_probs.items(), key=lambda x: x[1])[0]
                type_names = {'f': '小防', 's': '小生', 'g': '小攻', 'F': '大防', 'S': '大生',
                             'G': '大攻', 'j': '精通', 'c': '充能', 'b': '暴击', 'B': '暴伤'}

                # 风险度显示（独立颜色）
                if risk_ratio > 1.5:
                    risk_color = "#F44336"  # 红色 - 高风险
                elif risk_ratio > 1.0:
                    risk_color = "#FF9800"  # 橙色 - 中风险
                else:
                    risk_color = "#4CAF50"  # 绿色 - 安全

                if risk_ratio > 1.0:
                    risk_text_html = f'<span style="color: {risk_color};">风险度：{risk_ratio:.2f}x ({type_names[non_bb_max_type]}{non_bb_max_val:.0f}% > {type_names[bb_min_type]}{bb_min_val:.0f}%)</span>'
                else:
                    risk_text_html = f'<span style="color: {risk_color};">风险度：{risk_ratio:.2f}x (安全)</span>'
            else:
                risk_text_html = ""

            # 建议逻辑：简化颜色规则（无星星图标）
            if target_prob >= 60:
                advice_text = f"强化建议: 双暴{target_prob:.0f}% 歪率{bad_prob:.0f}% 建议强化！"
                advice_color = "#4CAF50"  # 绿色
            elif target_prob >= 50:
                advice_text = f"强化建议: 双暴{target_prob:.0f}% 歪率{bad_prob:.0f}% 可考虑强化"
                advice_color = "#FF9800"  # 橙色
            else:
                advice_text = f"强化建议: 双暴{target_prob:.0f}% 歪率{bad_prob:.0f}% 建议继续垫刀"
                advice_color = "#F44336"  # 红色

            # 分开显示建议和风险度（均匀分布）
            self.embryo_advice_label.setText(advice_text)
            self.embryo_advice_label.setStyleSheet(f"font-weight: bold; color: {advice_color};")

            if risk_text_html:
                self.risk_label.setText(risk_text_html)
            else:
                self.risk_label.setText("")

        except Exception as e:
            print(f"更新胚子表错误: {e}")

    def clear_embryo_table(self):
        """清空胚子概率表"""
        for col in range(4):
            self.table2.setItem(0, col, QTableWidgetItem(""))
        self.table2.setHorizontalHeaderLabels(["-", "-", "-", "-"])
        self.embryo_advice_label.setText("强化建议: -")
        self.embryo_advice_label.setStyleSheet("font-weight: bold;")
        self.risk_label.setText("")

    def calc_artifact_probs(self, probs, artifact_types):
        """
        计算胚子词条的条件概率
        probs: 10个词条的概率数组
        artifact_types: 胚子的4个词条类型（如['b', 'B', 'f', 'g']）
        返回: (条件概率字典, 胚子总概率)
        """
        # 获取胚子词条的索引
        artifact_indices = [type_map[t] for t in artifact_types]

        # 计算胚子总概率
        total_prob = sum(probs[i] for i in artifact_indices)

        # 计算条件概率 P(X | 出现胚子词条) = P(X) / P(胚子)
        conditional_probs = {}
        for idx in artifact_indices:
            if total_prob > 0:
                conditional_probs[idx] = probs[idx] / total_prob * 100
            else:
                conditional_probs[idx] = 25.0  # 均匀分布

        return conditional_probs, total_prob

    def value_to_index(self, value, star):
        """将词条值转换为0-39的索引（NPY文件只支持0-39）"""
        type_char = value[0]
        type_idx = type_map[type_char]
        if star == "5星":
            values_list = FIVE_STAR_VALUES[type_char]
        else:
            values_list = THREE_STAR_VALUES[type_char]
        try:
            gear_idx = values_list.index(value)
        except ValueError:
            gear_idx = 0
        return type_idx * 4 + gear_idx

    def predict(self):
        if len(self.input_rows) < 3:
            self.clear_tables()
            return

        try:
            # 检查预测模式
            use_dl = (self.mode_combo.currentText() == "深度学习模式" and
                     self.mode_combo.isEnabled())

            # 获取最近3个词条（input_rows[0]是最新的）
            # input_rows是[最新, ..., 最旧]，取前3个就是最新的
            last_3 = list(reversed(self.input_rows[:3]))  # 取前3个，然后反转为[最旧, 中间, 最新]

            if use_dl:
                # 深度学习模式：同时计算两种模式用于对比
                dl_probs = self.predict_with_dl_smart(last_3)
                stats_probs = self.predict_with_stats_sliding()
                probs_percent = dl_probs
                # 更新统计模式Top-3（用于对比）
                self.update_stats_top3(stats_probs)
            else:
                # 统计模式：只计算统计模式
                probs_percent = self.predict_with_stats_sliding()
                # 清除统计模式Top-3显示
                self.stats_top3_label.setText("")

            # 更新表格（只显示概率%）
            if probs_percent is not None:
                for col in range(10):
                    self.table1.setItem(0, col, QTableWidgetItem(f"{probs_percent[col]:.1f}"))

                # 更新Top-3推荐
                self.update_top3_recommendation(probs_percent)

                # 更新置信度
                self.update_confidence(probs_percent)

                # 更新胚子表（如果已设置胚子）
                if len(self.embryo_selected) == 4:
                    self.update_embryo_table()

        except Exception as e:
            print(f"预测错误: {e}")
            self.clear_tables()

    def predict_with_stats(self, past_3):
        """使用统计方法预测"""
        if not self.model_data:
            return None

        # 转换为索引
        indices = [self.value_to_index(row['value'], row['star']) for row in past_3]
        i1, i2, i3 = indices

        # 获取统计数据
        S3 = self.model_data['S3']
        W3 = self.model_data['W3']

        # 决定使用哪个矩阵
        star_count = sum(1 for row in past_3 if row['star'] == "5星")
        if star_count >= 2: # 至少有2个5星，就用W3
            counts = W3[i1, i2, i3, :].astype(float)
            if counts.sum() < 10:
                counts = counts + S3[i1, i2, i3, :].astype(float)
        else: # 否则用S3
            counts = S3[i1, i2, i3, :].astype(float)
            if counts.sum() < 10:
                counts = counts + W3[i1, i2, i3, :].astype(float)

        # 计算概率
        total = counts.sum()
        if total == 0:
            probs = np.ones(10) / 10
        else:
            probs = counts / total

        return probs * 100

    def predict_with_stats_sliding(self, max_entries=7):
        """使用滑动窗口统计预测
        max_entries: 最多使用最近多少个词条（默认7个，即最多5个窗口）
        """
        if not self.model_data or len(self.input_rows) < 3:
            return None

        # 获取最近max_entries个词条（input_rows是[最新, ..., 最旧]）
        # 取前max_entries个（最新的），然后反转为[最旧, ..., 最新]
        recent_rows = self.input_rows[:max_entries]
        all_rows = list(reversed(recent_rows))
        n = len(all_rows)

        # 生成滑动窗口
        windows = []
        weights = []

        # 窗口大小为3，步长为1
        num_windows = n - 2
        for i in range(num_windows):
            window = all_rows[i:i+3]  # [i, i+1, i+2]
            # 权重：越近的窗口权重越高
            weight = (i + 1) / num_windows  # 线性递增权重
            windows.append(window)
            weights.append(weight)

        # 归一化权重
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]

        # 每个窗口查表并加权平均
        final_probs = np.zeros(10)

        for window, weight in zip(windows, weights):
            probs = self.predict_with_stats(window)
            if probs is not None:
                final_probs += probs * weight

        return final_probs

    def predict_with_dl(self, past_3):
        """使用深度学习预测 - 单skip预测（保留用于兼容）"""
        try:
            from dl_model import ModelTrainer

            trainer = ModelTrainer(self.data_manager)

            # 将所有已录入的词条转换为entries格式
            all_entries = [{'value': row['value'], 'gear': row['gear'], 'star': row['star']} for row in past_3]

            # 使用skip=1预测
            probs = trainer.predict(all_entries, skip=1)
            return probs
        except Exception as e:
            print(f"深度学习预测失败: {e}")
            return None

    def predict_with_dl_smart(self, last_3):
        """使用深度学习智能预测 - 根据所有录入词条选择skip策略"""
        try:
            from dl_model import ModelTrainer

            trainer = ModelTrainer(self.data_manager)

            # 将所有已录入的词条（不只是最近3个）转换为entries格式
            all_entries = [{'value': row['value'], 'gear': row['gear'], 'star': row['star']} 
                          for row in reversed(self.input_rows)]  # 从最旧到最新

            # 使用智能预测（根据词条数量选择skip策略）
            probs = trainer.predict_dl_smart(all_entries)
            return probs
        except Exception as e:
            print(f"深度学习智能预测失败: {e}")
            # 失败时回退到统计模式
            return self.predict_with_stats(last_3)

    def update_top3_recommendation(self, probs_percent):
        """更新Top-3推荐"""
        # 词条名称映射
        type_names = ["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"]

        # 获取概率最高的3个索引
        top3_indices = np.argsort(probs_percent)[-3:][::-1]

        # 构建推荐文本
        recommendations = []
        for i, idx in enumerate(top3_indices, 1):
            name = type_names[idx]
            prob = probs_percent[idx]
            recommendations.append(f"{i}.{name}({prob:.1f}%)")

        self.top3_label.setText(f"Top-3推荐: {' | '.join(recommendations)}")

    def update_stats_top3(self, probs_percent):
        """更新统计模式Top-3推荐（用于深度学习模式对比）"""
        if probs_percent is None or len(probs_percent) == 0:
            self.stats_top3_label.setText("")
            return

        try:
            # 词条名称映射
            type_names = ["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"]

            # 获取概率最高的3个索引
            top3_indices = np.argsort(probs_percent)[-3:][::-1]

            # 构建推荐文本
            recommendations = []
            for i, idx in enumerate(top3_indices, 1):
                name = type_names[idx]
                prob = probs_percent[idx]
                recommendations.append(f"{i}.{name}({prob:.1f}%)")

            self.stats_top3_label.setText(f"Top-3统计: {' | '.join(recommendations)}")
        except Exception as e:
            # 出错时隐藏统计模式显示，不影响主预测
            self.stats_top3_label.setText("")
            print(f"统计模式Top-3更新失败: {e}")

    def update_confidence(self, probs_percent):
        """更新置信度显示"""
        # 计算置信度指标
        max_prob = np.max(probs_percent)
        std_prob = np.std(probs_percent)

        # 综合置信度评分 (0-100)
        # 公式：最高概率 - 标准差/2
        # 标准差越大（分布越分散），置信度越低
        confidence_score = max_prob - std_prob / 2
        confidence_score = max(0, min(100, confidence_score))

        # 根据预测模式选择阈值
        # 统计模式：查表分布集中，阈值较高
        # 深度学习模式：softmax分布平滑，阈值较低
        current_mode = self.mode_combo.currentText()
        if current_mode == "深度学习模式":
            high_threshold = config.CONFIDENCE_HIGH_DL
            medium_threshold = config.CONFIDENCE_MEDIUM_DL
        else:
            high_threshold = config.CONFIDENCE_HIGH_STATS
            medium_threshold = config.CONFIDENCE_MEDIUM_STATS

        # 确定置信度等级
        if confidence_score >= high_threshold:
            level = "高"
            color = "#4CAF50"
        elif confidence_score >= medium_threshold:
            level = "中"
            color = "#FF9800"
        else:
            level = "低"
            color = "#F44336"

        self.confidence_label.setText(f"置信度: {level} ({confidence_score:.1f})")
        self.confidence_label.setStyleSheet(f"font-weight: bold; color: {color};")

    def load_model_data(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(script_dir, 'genmat401.npy')
            self.model_data = np.load(model_path, allow_pickle=True).item()
            print(f"模型数据加载成功: {model_path}")
        except Exception as e:
            print(f"模型加载失败: {e}")
            self.model_data = None

    def update_data_status(self):
        """更新数据状态显示"""
        count = self.data_manager.get_record_count()
        model_exists = os.path.exists(os.path.join(self.data_manager.models_dir, 'best_model.pt'))

        model_status = "已训练 ✓" if model_exists else "未训练"
        self.status_label.setText(f"记录数: {count} | 模型状态: {model_status}")

        # 启用/禁用深度学习模式
        # 只要有模型文件就启用深度学习模式（预测不需要记录数）
        if model_exists:
            self.mode_combo.setEnabled(True)
        else:
            self.mode_combo.setEnabled(False)

        # 训练按钮：需要≥10条记录才能训练（降低门槛方便测试）
        if count >= 10:
            self.train_btn.setEnabled(True)
            self.train_btn.setToolTip("")
        else:
            self.train_btn.setEnabled(False)
            self.train_btn.setToolTip(f"需要至少10条记录，当前{count}条")

    def on_save_data_clicked(self):
        """保存当前录入的数据到JSON"""
        if len(self.input_rows) < 4:
            QMessageBox.warning(self, "数据不足", "需要至少4个词条才能保存一条强化记录")
            return

        # 构建entries列表（保存所有已录入的词条，按录入顺序）
        # input_rows: [最新, ..., 最旧]，需要反转为 [最旧, ..., 最新]
        entries = []
        reversed_rows = list(reversed(self.input_rows))
        for i, row in enumerate(reversed_rows):
            entry = {
                "value": row['value'],
                "gear": row['gear'],
                "star": row['star'],
                "type": row['value'][0],
                "order": i + 1  # 最旧的order=1，最新的order=最后
            }
            entries.append(entry)

        success, result = self.data_manager.save_record(entries)
        if success:
            QMessageBox.information(self, "保存成功", f"强化记录已保存到:\n{result}\n共{len(entries)}个词条")
            self.update_data_status()
        else:
            QMessageBox.critical(self, "保存失败", f"保存记录时发生错误:\n{result}")

    def on_export_excel_clicked(self):
        """导出当前录入的数据到Excel"""
        if not self.input_rows:
            QMessageBox.warning(self, "没有数据", "当前没有录入的词条数据")
            return

        try:
            import pandas as pd

            # 构建当前录入的数据
            rows = []
            for i, row in enumerate(self.input_rows):
                rows.append({
                    "录入顺序": i + 1,
                    "词条值": row['value'],
                    "档位": row['gear'],
                    "星级": row['star'],
                    "词条类型": row['value'][0]
                })

            df = pd.DataFrame(rows)

            # 生成文件名
            from datetime import datetime
            filename = f"current_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(self.data_manager.exports_dir, filename)

            df.to_excel(filepath, index=False, engine='openpyxl')
            QMessageBox.information(self, "导出成功", f"当前录入数据已导出到:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出失败: {str(e)}")

    def on_train_model_clicked(self):
        """训练深度学习模型"""
        count = self.data_manager.get_record_count()
        if count < 10:
            QMessageBox.warning(self, "数据不足", f"需要至少10条记录才能训练模型\n当前只有{count}条")
            return

        # 导入训练模块
        try:
            from dl_model import ModelTrainer

            reply = QMessageBox.question(self, "确认训练",
                f"当前有 {count} 条记录\n训练可能需要几分钟，是否继续？",
                QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                trainer = ModelTrainer(self.data_manager)
                success, message = trainer.train(epochs=50)

                if success:
                    QMessageBox.information(self, "训练完成", message)
                else:
                    QMessageBox.critical(self, "训练失败", message)

                self.update_data_status()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"训练过程出错:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ArtifactPredictor()
    ex.show()
    sys.exit(app.exec_())
