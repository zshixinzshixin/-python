#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置编辑器 - Qt界面版
用于方便地修改模型参数
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QMessageBox,
    QScrollArea, QFrame, QDoubleSpinBox, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ConfigEditor(QMainWindow):
    """配置编辑器主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("圣遗物预测器 - 配置编辑器")
        self.setMinimumSize(600, 700)

        # 当前配置值
        self.config_values = {}

        # 初始化UI
        self.init_ui()

        # 加载当前配置
        self.load_config()

    def init_ui(self):
        """初始化界面"""
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("模型参数配置")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 说明标签
        desc_label = QLabel("修改参数后点击保存，部分参数修改后需要重新训练模型")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: gray;")
        main_layout.addWidget(desc_label)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        main_layout.addWidget(scroll)

        # 滚动内容
        scroll_content = QWidget()
        scroll.setWidget(scroll_content)
        self.form_layout = QVBoxLayout(scroll_content)
        self.form_layout.setSpacing(15)

        # 创建参数组
        self.create_data_weight_group()
        self.create_sliding_window_group()
        self.create_skip_prediction_group()
        self.create_model_structure_group()
        self.create_training_group()
        self.create_confidence_group()

        # 按钮区域
        button_layout = QHBoxLayout()

        self.save_btn = QPushButton("保存配置")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.save_btn.clicked.connect(self.save_config)

        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_config)

        self.reload_btn = QPushButton("重新加载")
        self.reload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.reload_btn.clicked.connect(self.load_config)

        button_layout.addWidget(self.reset_btn)
        button_layout.addWidget(self.reload_btn)
        button_layout.addWidget(self.save_btn)

        main_layout.addLayout(button_layout)

    def create_param_row(self, parent_layout, label_text, tooltip, min_val, max_val, decimals=0):
        """创建参数行"""
        row = QHBoxLayout()

        label = QLabel(label_text)
        label.setToolTip(tooltip)
        label.setMinimumWidth(200)
        row.addWidget(label)

        if decimals > 0:
            spin_box = QDoubleSpinBox()
            spin_box.setDecimals(decimals)
        else:
            spin_box = QSpinBox()

        spin_box.setRange(min_val, max_val)
        spin_box.setToolTip(f"范围: {min_val} - {max_val}")
        spin_box.setMinimumWidth(100)
        row.addWidget(spin_box)

        desc_label = QLabel(tooltip)
        desc_label.setStyleSheet("color: gray; font-size: 11px;")
        desc_label.setWordWrap(True)
        row.addWidget(desc_label, 1)

        parent_layout.addLayout(row)
        return spin_box

    def create_data_weight_group(self):
        """数据权重组"""
        group = QGroupBox("数据权重")
        layout = QVBoxLayout(group)

        self.star_transition_weight = self.create_param_row(
            layout,
            "跨星级样本权重:",
            "3星→5星转换样本的权重倍数",
            1.0, 5.0, 1
        )

        self.form_layout.addWidget(group)

    def create_sliding_window_group(self):
        """滑动窗口组"""
        group = QGroupBox("滑动窗口预测")
        layout = QVBoxLayout(group)

        self.sliding_window_base = self.create_param_row(
            layout,
            "基础权重:",
            "最早样本的基础权重",
            0.1, 0.5, 2
        )

        self.sliding_window_range = self.create_param_row(
            layout,
            "变化范围:",
            "权重变化范围（最近样本权重 = 基础 + 范围）",
            0.5, 0.9, 2
        )

        self.form_layout.addWidget(group)

    def create_skip_prediction_group(self):
        """Skip预测组"""
        group = QGroupBox("Skip预测（修改后需重新训练）")
        group.setStyleSheet("QGroupBox { color: red; }")
        layout = QVBoxLayout(group)

        self.max_skip = self.create_param_row(
            layout,
            "最大Skip步数:",
            "1=只预测下一个, 2=跳过1个, 3=跳过2个",
            1, 5, 0
        )

        self.skip_1_weight_7plus = self.create_param_row(
            layout,
            "Skip=1权重(7+词条):",
            "7词条以上时近期预测权重",
            0.5, 1.0, 2
        )

        self.skip_1_weight_5to6 = self.create_param_row(
            layout,
            "Skip=1权重(5-6词条):",
            "5-6词条时近期预测权重",
            0.5, 1.0, 2
        )

        self.skip_2_weight = self.create_param_row(
            layout,
            "Skip=2权重:",
            "中期预测权重",
            0.2, 0.4, 2
        )

        self.skip_3_weight = self.create_param_row(
            layout,
            "Skip=3权重:",
            "长期预测权重",
            0.05, 0.2, 2
        )

        self.form_layout.addWidget(group)

    def create_model_structure_group(self):
        """模型结构组"""
        group = QGroupBox("模型结构（修改后需重新训练）")
        group.setStyleSheet("QGroupBox { color: red; }")
        layout = QVBoxLayout(group)

        self.embed_dim = self.create_param_row(
            layout,
            "词嵌入维度:",
            "Embedding层维度",
            8, 32, 0
        )

        self.hidden_dim = self.create_param_row(
            layout,
            "LSTM隐藏层:",
            "LSTM隐藏层维度",
            32, 128, 0
        )

        self.num_layers = self.create_param_row(
            layout,
            "LSTM层数:",
            "LSTM层数",
            1, 3, 0
        )

        self.dropout = self.create_param_row(
            layout,
            "Dropout比率:",
            "防止过拟合的Dropout比率",
            0.1, 0.5, 2
        )

        self.num_classes = self.create_param_row(
            layout,
            "输出类别数:",
            "10=只预测类型, 20=预测星级+类型",
            10, 20, 0
        )

        self.form_layout.addWidget(group)

    def create_training_group(self):
        """训练参数组"""
        group = QGroupBox("训练参数")
        layout = QVBoxLayout(group)

        self.epochs = self.create_param_row(
            layout,
            "训练轮数:",
            "最大训练轮数",
            50, 200, 0
        )

        self.learning_rate = self.create_param_row(
            layout,
            "学习率:",
            "优化器学习率",
            0.0001, 0.01, 4
        )

        self.patience = self.create_param_row(
            layout,
            "早停耐心值:",
            "多少轮不提升就停止",
            5, 20, 0
        )

        self.batch_size = self.create_param_row(
            layout,
            "批次大小:",
            "每批次样本数",
            16, 64, 0
        )

        self.min_records = self.create_param_row(
            layout,
            "最小记录数:",
            "训练所需最少记录数",
            5, 50, 0
        )

        self.form_layout.addWidget(group)

    def create_confidence_group(self):
        """置信度组"""
        group = QGroupBox("置信度计算（双模式）")
        layout = QVBoxLayout(group)

        self.confidence_std_factor = self.create_param_row(
            layout,
            "标准差系数:",
            "标准差对置信度的影响系数",
            5, 20, 0
        )

        # 统计模式阈值
        stats_label = QLabel("【统计模式阈值】")
        stats_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        layout.addWidget(stats_label)

        self.confidence_high_stats = self.create_param_row(
            layout,
            "  高置信度阈值:",
            "统计模式：高于此值为高置信度（查表分布集中）",
            30, 60, 0
        )

        self.confidence_medium_stats = self.create_param_row(
            layout,
            "  中置信度阈值:",
            "统计模式：高于此值为中置信度",
            15, 40, 0
        )

        # 深度学习模式阈值
        dl_label = QLabel("【深度学习模式阈值】")
        dl_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        layout.addWidget(dl_label)

        self.confidence_high_dl = self.create_param_row(
            layout,
            "  高置信度阈值:",
            "深度学习模式：高于此值为高置信度（建议20）",
            15, 30, 0
        )

        self.confidence_medium_dl = self.create_param_row(
            layout,
            "  中置信度阈值:",
            "深度学习模式：高于此值为中置信度（建议15）",
            10, 20, 0
        )

        self.form_layout.addWidget(group)

    def load_config(self):
        """加载当前配置"""
        try:
            import config

            self.star_transition_weight.setValue(config.STAR_TRANSITION_WEIGHT)
            self.sliding_window_base.setValue(config.SLIDING_WINDOW_BASE)
            self.sliding_window_range.setValue(config.SLIDING_WINDOW_RANGE)
            self.max_skip.setValue(config.MAX_SKIP)
            self.skip_1_weight_7plus.setValue(config.SKIP_1_WEIGHT_7PLUS)
            self.skip_1_weight_5to6.setValue(config.SKIP_1_WEIGHT_5TO6)
            self.skip_2_weight.setValue(config.SKIP_2_WEIGHT)
            self.skip_3_weight.setValue(config.SKIP_3_WEIGHT)
            self.embed_dim.setValue(config.EMBED_DIM)
            self.hidden_dim.setValue(config.HIDDEN_DIM)
            self.num_layers.setValue(config.NUM_LAYERS)
            self.dropout.setValue(config.DROPOUT)
            self.num_classes.setValue(config.NUM_CLASSES)
            self.epochs.setValue(config.EPOCHS)
            self.learning_rate.setValue(config.LEARNING_RATE)
            self.patience.setValue(config.PATIENCE)
            self.batch_size.setValue(config.BATCH_SIZE)
            self.min_records.setValue(config.MIN_RECORDS_FOR_TRAINING)
            self.confidence_std_factor.setValue(config.CONFIDENCE_STD_FACTOR)
            self.confidence_high_stats.setValue(config.CONFIDENCE_HIGH_STATS)
            self.confidence_medium_stats.setValue(config.CONFIDENCE_MEDIUM_STATS)
            self.confidence_high_dl.setValue(config.CONFIDENCE_HIGH_DL)
            self.confidence_medium_dl.setValue(config.CONFIDENCE_MEDIUM_DL)

            print("配置已加载")

        except Exception as e:
            QMessageBox.warning(self, "加载失败", f"无法加载配置: {e}")

    def save_config(self):
        """保存配置"""
        try:
            # 读取当前配置文件
            with open('config.py', 'r', encoding='utf-8') as f:
                content = f.read()

            # 更新各个参数
            updates = [
                ('STAR_TRANSITION_WEIGHT', self.star_transition_weight.value()),
                ('SLIDING_WINDOW_BASE', self.sliding_window_base.value()),
                ('SLIDING_WINDOW_RANGE', self.sliding_window_range.value()),
                ('MAX_SKIP', self.max_skip.value()),
                ('SKIP_1_WEIGHT_7PLUS', self.skip_1_weight_7plus.value()),
                ('SKIP_1_WEIGHT_5TO6', self.skip_1_weight_5to6.value()),
                ('SKIP_2_WEIGHT', self.skip_2_weight.value()),
                ('SKIP_3_WEIGHT', self.skip_3_weight.value()),
                ('EMBED_DIM', self.embed_dim.value()),
                ('HIDDEN_DIM', self.hidden_dim.value()),
                ('NUM_LAYERS', self.num_layers.value()),
                ('DROPOUT', self.dropout.value()),
                ('NUM_CLASSES', self.num_classes.value()),
                ('EPOCHS', self.epochs.value()),
                ('LEARNING_RATE', self.learning_rate.value()),
                ('PATIENCE', self.patience.value()),
                ('BATCH_SIZE', self.batch_size.value()),
                ('MIN_RECORDS_FOR_TRAINING', self.min_records.value()),
                ('CONFIDENCE_STD_FACTOR', self.confidence_std_factor.value()),
                ('CONFIDENCE_HIGH_STATS', self.confidence_high_stats.value()),
                ('CONFIDENCE_MEDIUM_STATS', self.confidence_medium_stats.value()),
                ('CONFIDENCE_HIGH_DL', self.confidence_high_dl.value()),
                ('CONFIDENCE_MEDIUM_DL', self.confidence_medium_dl.value()),
            ]

            for param_name, new_value in updates:
                # 查找并替换参数
                import re
                pattern = rf'({param_name}\s*=\s*)([^\s#]+)'
                replacement = rf'\g<1>{new_value}'
                content = re.sub(pattern, replacement, content)

            # 保存文件
            with open('config.py', 'w', encoding='utf-8') as f:
                f.write(content)

            QMessageBox.information(self, "保存成功", "配置已保存到 config.py\n\n注意：如果修改了模型结构参数，需要重新训练模型！")

        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"无法保存配置: {e}")

    def reset_config(self):
        """恢复默认配置"""
        reply = QMessageBox.question(
            self, "确认恢复",
            "确定要恢复默认配置吗？\n当前配置将被覆盖！",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # 创建默认配置
                default_config = '''"""
模型配置文件
调节这些参数来优化预测效果
"""

# ==================== 数据权重配置 ====================

# 跨星级样本权重倍数
STAR_TRANSITION_WEIGHT = 2.0


# ==================== 滑动窗口预测配置 ====================

SLIDING_WINDOW_BASE = 0.3
SLIDING_WINDOW_RANGE = 0.7


# ==================== 模型结构配置 ====================

EMBED_DIM = 16
HIDDEN_DIM = 64
NUM_LAYERS = 2
DROPOUT = 0.2
NUM_CLASSES = 10


# ==================== 训练超参数配置 ====================

EPOCHS = 100
LEARNING_RATE = 0.001
PATIENCE = 10
BATCH_SIZE = 32


# ==================== 置信度计算配置 ====================

CONFIDENCE_STD_FACTOR = 10

# 统计模式阈值（查表分布集中）
CONFIDENCE_HIGH_STATS = 40
CONFIDENCE_MEDIUM_STATS = 25

# 深度学习模式阈值（softmax分布平滑，阈值更低）
CONFIDENCE_HIGH_DL = 20
CONFIDENCE_MEDIUM_DL = 15


# ==================== 其他配置 ====================

MIN_RECORDS_FOR_TRAINING = 10
TEST_RATIO = 0.2
'''

                with open('config.py', 'w', encoding='utf-8') as f:
                    f.write(default_config)

                self.load_config()
                QMessageBox.information(self, "恢复成功", "已恢复默认配置")

            except Exception as e:
                QMessageBox.critical(self, "恢复失败", f"无法恢复配置: {e}")


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置应用样式
    app.setStyle('Fusion')

    window = ConfigEditor()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
