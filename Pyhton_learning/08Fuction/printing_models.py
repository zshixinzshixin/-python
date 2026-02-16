# 首先创建一个列表，其中包含一些要打印的设计
unprinted_desigins = ['phone case', 'robot pendant', 'dodecahedron']
conmpleted_models = []

# 模拟打印每个设计，直到没有未打印的设计为止
# 打印每个设计后，都将其移到列表 completed_models中

while unprinted_desigins:
    current_design = unprinted_desigins.pop()
    print(f"Printing model: {current_design}")
    conmpleted_models.append(current_design)

# 显示打印的所有模型
print("\nThe following models have been printed:")
for completed_model in conmpleted_models:
    print(conmpleted_models)


# 下面是重新编写的函数
print("\n--------------")
def print_models(unprinted_desigins, completed_models):
    """"
    模拟打印每个设计，直到没有未打印的设计为止
    打印每个设计后，都将其移到列表 completed_models中
    """
    while unprinted_desigins:
        current_design = unprinted_desigins.pop()
        print(f"Printing model: {current_design}")
        completed_models.append(current_design)

def show_completed_models(completed_models):
    """"显示打印好的所有模型"""
    print("\nThe following models have been printed:")
    for completed_model in completed_models:
        print(completed_model)
    
unprinted_desigins = ['phone case', 'robot pendant', 'dodecahedron']
completed_models = []

print_models(unprinted_desigins[:], completed_models)
show_completed_models(conmpleted_models)
print(f"\n{unprinted_desigins}")
# 这切片表示法 [:] 创建列表的副本。