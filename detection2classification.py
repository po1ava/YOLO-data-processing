import glob
import os
import shutil

source_dir = "example_0/labels"  # 原数据集标签所在目录
target_dir = "example_0/new_class"  # 存放符合条件图片的目标目录
class_tuple = ('3',)

if __name__ == "__main__":
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)

    # 获取所有txt文件
    txt_files = glob.glob(os.path.join(source_dir, '*.txt'))

    for txt_file in txt_files:
        has_target_line = False
        with open(txt_file, 'r', encoding='utf-8') as f:
            for line in f:
                # 检查是否具有符合条件的标签
                if line.lstrip().startswith(class_tuple):
                    has_target_line = True
                    break

        # 如果存在符合条件的行，移动同名图片
        if has_target_line:
            # 获取不带扩展名的文件名
            base_name = os.path.splitext(os.path.basename(txt_file))[0]

            # 查找匹配的图片文件
            for ext in ['jpg', 'png', 'jpeg']:
                image_path = os.path.join(source_dir, f"{base_name}.{ext}").replace("/labels", "/images")

                if os.path.exists(image_path):
                    # 移动图片到目标目录
                    shutil.move(image_path, os.path.join(target_dir, os.path.basename(image_path)))
                    print(f"已移动: {image_path} → {target_dir}")
                    break
