with open('C:\\Users\\Administrator\\Desktop\\工作\\sort\\ansible_sort_data.txt', 'r') as file:
    lines = file.readlines()

# 提取偶数行，保留数字并加 'C'
result = [line.split()[-1] + 'C\n' for i, line in enumerate(lines, 1) if i % 2 == 0]

# 保存到新的文件
with open('C:\\Users\\Administrator\\Desktop\\工作\\sort\\ansible_result.txt', 'w') as file:
    file.writelines(result)