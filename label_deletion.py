import os

target_dir = "example"  # 数据集所在根目录，支持嵌套
delete_label = ['3']  # 需要删除的标签序号列表

if __name__ == "__main__":

    num = 0
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                filtered_lines = []
                for line in lines:
                    stripped = line.strip()
                    # 跳过空行和需要清除的行
                    if not stripped:
                        continue
                    if stripped.split()[0] in delete_label:
                        num += 1
                        continue
                    filtered_lines.append(line)

                # 重新写回文件
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    f.writelines(filtered_lines)

    print(f"共删除{num}条标签数据")
    print(f"已清理 {target_dir} 及其子目录下所有标签文件")
