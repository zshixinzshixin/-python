alien_0 = {'color': 'green', 'points': 5}
alien_1 = {'color': 'yellow', 'points': 10}
alien_2 = {'color': 'red', 'points': 15}

aliens = [alien_0, alien_1, alien_2]

for alien in aliens:
    print(alien)
# 把三个外星人的字典嵌套进入列表里

print("\n")
aliens = []
# 先定义空列表
for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5,'speed': 'slow'}
    aliens.append(new_alien)

for alien in aliens[:5]:
    print(alien)
print("...")

print(f"Total number of aliens: {len(aliens)}")
# 自动加入

print("\n")
aliens = []

for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)

for alien in aliens[:3]:
    # 这里要用alien，这个是单独列表可以通过键来查询值
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['speed'] = 'medium'
        alien['points'] = 10
    elif alien['color'] == 'yellow':
        alien['color'] = 'red'
        alien['speed'] = fast
        alien['points'] = 15
    
for alien in aliens[:5]:
    print(alien)
print("...")