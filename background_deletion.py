import os
import random

if __name__ == '__main__':
    target_dir = 'E:/desktop/文物病害研究/0626南京银行仅有变色'  # 替换为你的目标文件夹路径

    # 收集所有空文本文件路径
    empty_txt_files = []

    # 遍历文件夹及子文件夹
    for root, _, files in os.walk(target_dir):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                # 检查是否为空文件
                if os.path.isfile(file_path) and os.path.getsize(file_path) == 0:
                    empty_txt_files.append(file_path)

    # 输出空文本文件总数
    total_empty = len(empty_txt_files)
    print(f"发现空文本文件总数: {total_empty}")

    # 计算需要删除的数量（90%）
    num_to_delete = round(total_empty * 0.8)
    print(f"计划删除 {num_to_delete} 个空文本文件 (90%)")

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

            for ext in ['.png', '.jpg', '.jpeg']:  # 支持的图片格式
                img_file = base_name + ext
                if os.path.exists(img_file):
                    try:
                        os.remove(img_file)
                        deleted_img_count += 1
                        print(f"已删除: {os.path.basename(txt_file)} 和同名图片")
                        break  # 删除一个匹配的图片后跳出循环
                    except Exception as e:
                        print(f"删除图片失败: {img_file}, 错误: {e}")
        except Exception as e:
            print(f"删除文本文件失败: {txt_file}, 错误: {e}")

    # 输出结果
    print(f"\n操作完成:")
    print(f"成功删除文本文件: {deleted_txt_count}/{num_to_delete}")
    print(f"成功删除同名图片: {deleted_img_count}")
    print(f"剩余空文本文件: {total_empty - deleted_txt_count}")
