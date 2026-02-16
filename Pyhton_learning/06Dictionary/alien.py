alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color'])
print(alien_0['points'])

new_points = alien_0['points']
print(f"You just earned {new_points} points!")

print(f"\n{alien_0}")
alien_0['x_position'] = 0
alien_0['y_position'] = 25
print(alien_0)
# 添加键对

alien_0 = {}
alien_0['color'] = 'green'
alien_0['points'] = 5
print(f'\n{alien_0}')
# 定义空字典

alien_0['color'] = 'yellow'
print(f"The alinen is now {alien_0['color'].title()}")