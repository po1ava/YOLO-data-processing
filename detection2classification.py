import os
import shutil
import glob


def move_images_based_on_txt(source_dir, target_dir):
    """
    根据txt文件内容移动同名图片
    参数:
        source_dir: 源目录（包含txt和图片）
        target_dir: 目标目录（存放符合条件的图片）
    """
    # 创建目标目录（如果不存在）
    os.makedirs(target_dir, exist_ok=True)

    # 获取所有txt文件
    txt_files = glob.glob(os.path.join(source_dir, '*.txt'))

    for txt_file in txt_files:
        # 检查txt内容是否包含以"3"开头的行
        has_target_line = False
        with open(txt_file, 'r', encoding='utf-8') as f:
            for line in f:
                # 检查行是否以"3"开头（忽略行首空白）
                if line.lstrip().startswith('3'):
                    has_target_line = True
                    break

        # 如果存在符合条件的行，移动同名图片
        if has_target_line:
            # 获取不带扩展名的文件名
            base_name = os.path.splitext(os.path.basename(txt_file))[0]

            # 查找匹配的图片文件
            for ext in ['jpg', 'png', 'jpeg']:
                image_path = os.path.join(source_dir, f"{base_name}.{ext}").replace("/labels","/images")

                if os.path.exists(image_path):
                    # 移动图片到目标目录
                    shutil.move(image_path, os.path.join(target_dir, os.path.basename(image_path)))
                    print(f"已移动: {image_path} → {target_dir}")
                    break


if __name__ == "__main__":
    # 配置路径（根据实际情况修改）
    SOURCE_DIR = "E:/desktop/文物病害研究/0702四牌楼全部仅有变色分类/val/labels"  # 包含txt和图片的源目录
    TARGET_DIR = "E:/desktop/文物病害研究/0702四牌楼全部仅有变色分类/val/DD"  # 存放符合条件图片的目标目录

    # 执行处理
    move_images_based_on_txt(SOURCE_DIR, TARGET_DIR)