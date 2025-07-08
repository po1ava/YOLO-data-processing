import os
import random

target_dir = "example"  # 数据集所在根目录，支持嵌套
delete_ratio = 0  # 删除背景图片比例（0-1）

if __name__ == '__main__':

    empty_txt_files = []

    # 遍历文件夹及子文件夹
    for root, _, files in os.walk(target_dir):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                    empty_txt_files.append(file_path)

    # 输出背景图片总数
    total_empty = len(empty_txt_files)
    print(f"发现背景图片总数: {total_empty}")

    # 计算需要删除的数量
    num_to_delete = round(total_empty * delete_ratio)

    # 随机选择要删除的文件
    files_to_delete = random.sample(empty_txt_files, num_to_delete) if num_to_delete > 0 else []

    # 执行删除操作
    deleted_txt_count = 0
    deleted_img_count = 0

    for txt_file in files_to_delete:
        try:
            # 删除文本文件
            os.remove(txt_file)
            deleted_txt_count += 1

            # 查找并删除同名图片
            base_name = txt_file.replace('.txt', '').replace('\\labels\\', '\\images\\')
            print(txt_file)
            print(base_name)

            for ext in ['.png', '.jpg', '.jpeg']:
                img_file = base_name + ext
                if os.path.exists(img_file):
                    try:
                        os.remove(img_file)
                        deleted_img_count += 1
                        # print(f"已删除: {os.path.basename(txt_file)} 和相应图片")
                        break  # 删除一个匹配的图片后跳出循环
                    except Exception as e:
                        print(f"删除图片失败: {img_file}, 错误: {e}")
        except Exception as e:
            print(f"删除标签文件失败: {txt_file}, 错误: {e}")

    # 输出结果
    print(f"成功删除背景图片标签文件: {deleted_txt_count}/{num_to_delete}")
    print(f"成功删除背景图片: {deleted_img_count}")
