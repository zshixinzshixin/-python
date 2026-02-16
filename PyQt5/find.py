import os
import subprocess
import tempfile

def test_pyuic():
    """测试 pyuic5 是否工作"""
    
    # 创建临时的 .ui 文件
    ui_content = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
 </widget>
 <resources/>
 <connections/>
</ui>'''
    
    with tempfile.NamedTemporaryFile(suffix='.ui', delete=False, mode='w') as f:
        f.write(ui_content)
        ui_file = f.name
    
    try:
        # 尝试不同的命令
        commands = [
            ['pyuic5', '-x', ui_file, '-o', 'test_output.py'],
            ['python', '-m', 'PyQt5.uic.pyuic', '-x', ui_file, '-o', 'test_output2.py'],
            ['D:\\MiniConda\\python.exe', '-m', 'PyQt5.uic.pyuic', '-x', ui_file, '-o', 'test_output3.py']
        ]
        
        for i, cmd in enumerate(commands):
            print(f"\n尝试命令: {' '.join(cmd)}")
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ 命令 {i+1} 成功")
                    # 检查输出文件
                    output_file = cmd[-1]
                    if os.path.exists(output_file):
                        print(f"   生成文件: {output_file}")
                        with open(output_file, 'r') as f:
                            content = f.read(100)
                            print(f"   文件开头: {content[:50]}...")
                else:
                    print(f"❌ 命令 {i+1} 失败")
                    print(f"   错误: {result.stderr}")
            except Exception as e:
                print(f"❌ 命令 {i+1} 异常: {e}")
    
    finally:
        # 清理临时文件
        os.unlink(ui_file)
        for f in ['test_output.py', 'test_output2.py', 'test_output3.py']:
            if os.path.exists(f):
                os.unlink(f)

if __name__ == "__main__":
    test_pyuic()