#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
圣遗物预测器 - 轻量版
只保留深度学习预测功能
"""

import sys
import os
import json
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QTabWidget, QGroupBox, QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QScrollArea, QMessageBox
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

# 词条数值定义 - 三星
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
            base_dir = os.getcwd()
        self.base_dir = base_dir
        self.records_dir = os.path.join(base_dir, '强化记录')
        self.exports_dir = os.path.join(self.records_dir, 'exports')
        self.models_dir = os.path.join(self.records_dir, 'models')
        self._ensure_directories()

    def _ensure_directories(self):
        """确保所有必要的文件夹存在"""
        for dir_path in [self.records_dir, self.exports_dir, self.models_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

    def _get_json_file_path(self):
        """获取带时间戳的JSON文件路径"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.records_dir, f'record_{timestamp}.json')

    def load_records(self):
        """加载所有强化记录"""
        all_records = []
        last_updated = ""

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

    def save_record(self, entries):
        """保存一条强化记录"""
        try:
            filepath = self._get_json_file_path()
            record_data = {
                "records": [{
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "entries": entries
                }],
                "metadata": {
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "version": "1.0"
                }
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(record_data, f, ensure_ascii=False, indent=2)

            return True, filepath
        except Exception as e:
            return False, str(e)

    def get_record_count(self):
        """获取记录总数"""
        data = self.load_records()
        return len(data['records'])


class ArtifactPredictor(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("原神圣遗物词条预测工具 - 轻量版")
        self.setMinimumSize(1200, 700)

        # 设置图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon', 'icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 数据管理器
        self.data_manager = DataManager()

        # 深度学习预测器
        from dl_model import ModelPredictor
        self.dl_predictor = ModelPredictor(self.data_manager.models_dir)

        # 初始化数据
        self.input_rows = []  # 已录入的词条列表（最新的在最后）
        self.embryo_selected = []  # 胚子选择的词条

        self.init_ui()
        self.update_data_status()

    def init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)

        # 左侧：标签页（五星、三星、胚子）
        left_tabs = QTabWidget()
        left_tabs.addTab(self.create_five_star_tab(), "五星")
        left_tabs.addTab(self.create_three_star_tab(), "三星")
        left_tabs.addTab(self.create_embryo_tab(), "胚子")
        main_layout.addWidget(left_tabs, 1)

        # 中间：录入记录区
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

        # 表头
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

        # 右侧：预测结果区
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(5)

        # 数据操作按钮
        data_btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存数据")
        save_btn.clicked.connect(self.on_save_data_clicked)
        export_btn = QPushButton("导出Excel")
        export_btn.clicked.connect(self.on_export_excel_clicked)
        data_btn_layout.addWidget(save_btn)
        data_btn_layout.addWidget(export_btn)
        right_layout.addLayout(data_btn_layout)

        # 数据状态显示
        self.status_label = QLabel("记录数: 0")
        right_layout.addWidget(self.status_label)

        # 表1：概率表
        table1_group = QGroupBox("表1：预测下一次词条")
        table1_layout = QVBoxLayout(table1_group)
        self.table1 = QTableWidget(1, 10)
        self.table1.setHorizontalHeaderLabels(["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"])
        self.table1.setVerticalHeaderLabels(["概率%"])
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table1.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table1.setFixedHeight(self.table1.horizontalHeader().height() + 40)
        table1_layout.addWidget(self.table1)

        # Top-3推荐显示
        self.top3_label = QLabel("Top-3推荐: -")
        self.top3_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        table1_layout.addWidget(self.top3_label)

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

        # 强化建议
        self.suggestion_label = QLabel("强化建议: -")
        self.suggestion_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        table2_layout.addWidget(self.suggestion_label)

        # 风险度标签
        self.risk_label = QLabel("")
        self.risk_label.setStyleSheet("font-weight: bold;")
        table2_layout.addWidget(self.risk_label)

        right_layout.addWidget(table2_group)
        right_layout.addStretch()

        main_layout.addWidget(right_panel, 2)

    def create_five_star_tab(self):
        """创建五星词条标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(5)

        info_label = QLabel("录入五星词条（补词条、强化）。")
        layout.addWidget(info_label)

        # 创建按钮网格
        grid = QGridLayout()
        grid.setSpacing(5)

        row = 0
        col = 0
        for type_key, values in FIVE_STAR_VALUES.items():
            for value in values:
                btn = QPushButton(value)
                btn.setFixedSize(60, 30)
                btn.clicked.connect(lambda checked, v=value: self.on_entry_clicked(v, "5星"))
                grid.addWidget(btn, row, col)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1

        layout.addLayout(grid)
        layout.addStretch()
        return tab

    def create_three_star_tab(self):
        """创建三星词条标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(5)

        info_label = QLabel("录入三星词条（垫刀）。")
        layout.addWidget(info_label)

        grid = QGridLayout()
        grid.setSpacing(5)

        row = 0
        col = 0
        for type_key, values in THREE_STAR_VALUES.items():
            for value in values:
                btn = QPushButton(value)
                btn.setFixedSize(60, 30)
                btn.clicked.connect(lambda checked, v=value: self.on_entry_clicked(v, "3星"))
                grid.addWidget(btn, row, col)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1

        layout.addLayout(grid)
        layout.addStretch()
        return tab

    def create_embryo_tab(self):
        """创建胚子标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(5)

        info_label = QLabel("选择4个初始词条类型作为胚子，查看强化概率。")
        layout.addWidget(info_label)

        # 词条类型名称和键
        type_names = ['小防', '小生', '小攻', '大防', '大生', '大攻', '精通', '充能', '暴击', '暴伤']
        type_keys = ['f', 's', 'g', 'F', 'S', 'G', 'j', 'c', 'b', 'B']

        # 创建2行5列的勾选按钮网格
        self.embryo_buttons = {}
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
        return tab

    def on_entry_clicked(self, value, star):
        """处理词条按钮点击"""
        gear = self.get_gear_from_value(value, star)

        # 创建行widget
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(5, 2, 5, 2)
        row_layout.setSpacing(5)

        row_layout.addWidget(QLabel(str(gear)), 1)
        row_layout.addWidget(QLabel(value), 2)
        row_layout.addWidget(QLabel(star), 1)
        # 序号（录入顺序，最新的序号最大）
        order_label = QLabel(str(len(self.input_rows) + 1))
        row_layout.addWidget(order_label, 1)

        # 插入到最前面（最新词条在最上面）
        self.input_layout.insertWidget(0, row_widget)

        # 保存数据（包括widget引用）
        self.input_rows.insert(0, {
            'widget': row_widget,
            'gear': gear,
            'value': value,
            'star': star
        })

        # 滚动到顶部显示最新词条
        self.input_scroll.verticalScrollBar().setValue(0)

        self.update_prediction()

    def get_gear_from_value(self, value, star="5星"):
        """从词条值获取档位"""
        type_char = value[0]
        # 根据星级选择对应的词条定义
        if star == "3星":
            values_list = THREE_STAR_VALUES.get(type_char, [])
        else:
            values_list = FIVE_STAR_VALUES.get(type_char, [])
        try:
            return values_list.index(value) + 1
        except ValueError:
            return 1

    def on_embryo_type_clicked(self, type_key, btn):
        """处理胚子词条类型点击"""
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

    def update_embryo_table(self):
        """更新胚子概率表"""
        if len(self.embryo_selected) != 4:
            self.clear_embryo_table()
            return

        try:
            # 获取当前预测概率
            probs_percent = None
            if len(self.input_rows) >= 3:
                last_3 = list(reversed(self.input_rows[:3]))
                probs_percent = self.dl_predictor.predict_dl_smart(last_3)

            if probs_percent is not None:
                # 计算条件概率
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

                # 更新强化建议
                self.update_embryo_suggestion(artifact_probs)
            else:
                self.clear_embryo_table()
        except Exception as e:
            print(f"胚子表更新错误: {e}")
            self.clear_embryo_table()

    def calc_artifact_probs(self, probs_percent, embryo_types):
        """计算胚子条件概率
        probs_percent: 10种词条的原始概率
        embryo_types: 4个胚子词条类型键（如 ['b', 'B', 'f', 's']）
        返回: (条件概率字典, 总概率)
        """
        # 计算胚子中4个词条的总概率
        total_prob = sum(probs_percent[type_map[t]] for t in embryo_types)

        # 计算条件概率（归一化到胚子内）
        artifact_probs = {}
        for t in embryo_types:
            type_idx = type_map[t]
            if total_prob > 0:
                artifact_probs[type_idx] = probs_percent[type_idx] / total_prob * 100
            else:
                artifact_probs[type_idx] = 25.0  # 如果总概率为0，平均分配

        return artifact_probs, total_prob

    def update_embryo_suggestion(self, artifact_probs):
        """更新胚子强化建议和风险度"""
        # 定义目标词条类型（双暴）
        target_types = ['b', 'B']  # 暴击、暴伤
        type_names = {'f': '小防', 's': '小生', 'g': '小攻', 'F': '大防', 'S': '大生',
                     'G': '大攻', 'j': '精通', 'c': '充能', 'b': '暴击', 'B': '暴伤'}

        # 计算双暴概率和歪率
        target_prob = sum(artifact_probs.get(type_map[t], 0) for t in self.embryo_selected if t in target_types)
        bad_prob = 100 - target_prob

        # 计算风险度（方案3：风险倍数）
        bb_probs = {t: artifact_probs.get(type_map[t], 0) for t in self.embryo_selected if t in target_types}
        non_bb_probs = {t: artifact_probs.get(type_map[t], 0) for t in self.embryo_selected if t not in target_types}

        if bb_probs and non_bb_probs:
            bb_min_val = min(bb_probs.values())
            non_bb_max_val = max(non_bb_probs.values())
            risk_ratio = non_bb_max_val / bb_min_val if bb_min_val > 0 else float('inf')

            # 找出最危险的对比
            bb_min_type = min(bb_probs.keys(), key=lambda t: bb_probs[t])
            non_bb_max_type = max(non_bb_probs.keys(), key=lambda t: non_bb_probs[t])

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

        # 分开显示建议和风险度
        self.suggestion_label.setText(advice_text)
        self.suggestion_label.setStyleSheet(f"font-weight: bold; color: {advice_color};")

        if risk_text_html:
            self.risk_label.setText(risk_text_html)
        else:
            self.risk_label.setText("")

    def clear_embryo_table(self):
        """清除胚子表"""
        self.table2.setHorizontalHeaderLabels(["-", "-", "-", "-"])
        for col in range(4):
            self.table2.setItem(0, col, QTableWidgetItem("-"))
        self.suggestion_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        self.suggestion_label.setText("强化建议: -")
        self.risk_label.setText("")

    def update_prediction(self):
        """更新预测"""
        if len(self.input_rows) < 3:
            self.clear_tables()
            return

        try:
            # 获取所有已录入的词条（从最旧到最新）
            all_entries = [{'value': row['value'], 'gear': row['gear'], 'star': row['star']} 
                          for row in reversed(self.input_rows)]

            # 使用深度学习智能预测（根据所有词条数量选择skip策略）
            probs = self.dl_predictor.predict_dl_smart(all_entries)

            if probs is not None:
                # 更新表格
                for col in range(10):
                    self.table1.setItem(0, col, QTableWidgetItem(f"{probs[col]:.1f}"))

                # 更新Top-3推荐
                self.update_top3_recommendation(probs)

                # 更新置信度
                self.update_confidence(probs)

                # 更新胚子表
                if len(self.embryo_selected) == 4:
                    self.update_embryo_table()
            else:
                self.clear_tables()

        except Exception as e:
            print(f"预测错误: {e}")
            self.clear_tables()

    def update_top3_recommendation(self, probs):
        """更新Top-3推荐"""
        top_indices = np.argsort(probs)[-3:][::-1]

        type_names = ["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"]

        recommendations = []
        for idx in top_indices:
            recommendations.append(f"{type_names[idx]}({probs[idx]:.1f}%)")

        self.top3_label.setText(f"Top-3推荐: {' > '.join(recommendations)}")

    def update_confidence(self, probs):
        """更新置信度"""
        # 计算置信度：最高概率与次高概率的差距
        sorted_probs = np.sort(probs)[::-1]
        gap = sorted_probs[0] - sorted_probs[1]

        if gap > 20:
            confidence = "高"
            color = "#4CAF50"  # 绿色
        elif gap > 10:
            confidence = "中"
            color = "#FF9800"  # 橙色
        else:
            confidence = "低"
            color = "#F44336"  # 红色

        self.confidence_label.setStyleSheet(f"font-weight: bold; color: {color};")
        self.confidence_label.setText(f"置信度: {confidence} (差距: {gap:.1f}%)")

    def clear_tables(self):
        """清除表格"""
        for col in range(10):
            self.table1.setItem(0, col, QTableWidgetItem(""))
        self.top3_label.setText("Top-3推荐: -")
        self.confidence_label.setText("置信度: -")

    def on_clear_clicked(self):
        """清空所有录入"""
        self.input_rows = []
        # 清除UI
        while self.input_layout.count():
            child = self.input_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.clear_tables()

    def on_delete_last_clicked(self):
        """删除最新一条录入的数据（最上面的一条）"""
        if self.input_rows:
            # 删除最上面的widget
            last_row = self.input_rows.pop(0)
            last_row['widget'].deleteLater()
            self.update_prediction()

    def update_data_status(self):
        """更新数据状态显示"""
        count = self.data_manager.get_record_count()
        self.status_label.setText(f"记录数: {count}")

    def on_save_data_clicked(self):
        """保存当前录入的数据"""
        if len(self.input_rows) < 4:
            QMessageBox.warning(self, "数据不足", "需要至少4个词条才能保存")
            return

        entries = []
        reversed_rows = list(reversed(self.input_rows))
        for i, row in enumerate(reversed_rows):
            entry = {
                "value": row['value'],
                "gear": row['gear'],
                "star": row['star'],
                "type": row['value'][0],
                "order": i + 1
            }
            entries.append(entry)

        success, result = self.data_manager.save_record(entries)
        if success:
            QMessageBox.information(self, "保存成功", f"强化记录已保存\n共{len(entries)}个词条")
            self.update_data_status()
        else:
            QMessageBox.critical(self, "保存失败", f"保存失败: {result}")

    def on_export_excel_clicked(self):
        """导出当前录入数据到Excel"""
        if len(self.input_rows) < 3:
            QMessageBox.warning(self, "数据不足", "需要至少3个词条才能导出")
            return

        try:
            import pandas as pd

            data = []
            reversed_rows = list(reversed(self.input_rows))
            for i, row in enumerate(reversed_rows):
                data.append({
                    '顺序': i + 1,
                    '词条': row['value'],
                    '档位': row['gear'],
                    '星级': row['star']
                })

            df = pd.DataFrame(data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.data_manager.exports_dir, f'entries_{timestamp}.xlsx')

            df.to_excel(filepath, index=False, engine='openpyxl')
            QMessageBox.information(self, "导出成功", f"数据已导出到:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ArtifactPredictor()
    ex.show()
    sys.exit(app.exec_())
