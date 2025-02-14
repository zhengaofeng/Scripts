# 读取数据文件并按两行一组排序
with open('C:\\Users\\Administrator\\Desktop\\工作\\sort\\ansible_free.txt', 'r') as file:
    lines = file.readlines()

# 将两行一组组合起来
grouped_lines = [lines[i:i + 2] for i in range(0, len(lines), 2)]
print(grouped_lines)

# 对每组的第1行（IP地址行）进行排序
grouped_lines.sort(key=lambda x: list(map(int, x[0].split(' | ')[0].split('.'))))
print(grouped_lines)

# 将排序后的内容写回文件
with open('C:\\Users\\Administrator\\Desktop\\工作\\sort\\ansible_sort_free.txt', 'w') as file:
    for group in grouped_lines:
        file.writelines(group)


