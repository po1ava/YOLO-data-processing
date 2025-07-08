import os
import shutil
import uuid
from glob import glob

import albumentations as A
import cv2

img_dir = "example_0/images"  # 图片所在路径
augmentation_factor = 4  # 数据增强后相对于原数据集的倍数，填写>=2的整数

horizontalFlip = 0.5  # 水平翻转图像概率
verticalFlip = 0.3  # 垂直翻转图像概率
randomRotate90 = 0.4  # 图像随机旋转90°的倍数概率
randomBrightnessContrast = 0.5  # 随机调整亮度和对比度概率
hueSaturationValue = 0.2  # 调整色调、饱和度和明度概率
gaussianBlur = 0.2  # 应用高斯模糊概率
clahe = 0.1  # 增强局部对比度概率


class YOLOv8AlbumentationsAugmenter:
    def __init__(self, output_img_dir, output_label_dir, target_size=(640, 640)):

        # 初始化路径参数
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.output_img_dir = output_img_dir
        self.output_label_dir = output_label_dir
        os.makedirs(output_img_dir, exist_ok=True)
        os.makedirs(output_label_dir, exist_ok=True)

        # 定义增强管道（包含空间变换+像素变换）
        self.transform = A.Compose([
            A.Resize(*target_size),  # 统一尺寸
            A.HorizontalFlip(p=horizontalFlip),
            A.VerticalFlip(p=verticalFlip),
            A.RandomRotate90(p=randomRotate90),
            A.RandomBrightnessContrast(p=randomBrightnessContrast),
            A.HueSaturationValue(p=hueSaturationValue),
            A.GaussianBlur(blur_limit=(3, 7), p=gaussianBlur),
            A.CLAHE(p=clahe),
        ], bbox_params=A.BboxParams(format='yolo',
                                    label_fields=['class_labels']))

    def process_single_image(self, img_path, label_path):
        # 读取图像和标签
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 解析YOLO标签
        with open(label_path, 'r') as f:
            lines = f.readlines()
        bboxes = []
        class_labels = []
        for line in lines:
            cls, xc, yc, w, h = map(float, line.strip().split())
            bboxes.append([xc, yc, w, h])
            class_labels.append(cls)

        # 应用增强
        transformed = self.transform(
            image=image,
            bboxes=bboxes,
            class_labels=class_labels
        )

        # 生成唯一文件名
        unique_id = str(uuid.uuid4())[:8]
        new_img_name = f"{unique_id}.jpg"
        new_label_name = f"{unique_id}.txt"

        # 保存增强后的图像
        cv2.imwrite(os.path.join(self.output_img_dir, new_img_name),
                    cv2.cvtColor(transformed['image'], cv2.COLOR_RGB2BGR))

        # 保存增强后的标签
        with open(os.path.join(self.output_label_dir, new_label_name), 'w') as f:
            for bbox, cls in zip(transformed['bboxes'], transformed['class_labels']):
                f.write(f"{int(cls)} {' '.join(map(str, bbox))}\n")

    def batch_augment(self):
        img_paths = glob(os.path.join(self.img_dir, "*.jpg"))
        for img_path in img_paths:
            print(img_path)

            base_name = os.path.basename(img_path).replace(".jpg", "")
            label_path = os.path.join(self.label_dir, f"{base_name}.txt")
            print(label_path)
            try:
                if os.path.exists(label_path):
                    self.process_single_image(img_path, label_path)
            except:
                pass


def move_and_delete_folder(src_dir, dst_dir):
    # 创建目标目录（若不存在）
    os.makedirs(dst_dir, exist_ok=True)

    # 移动所有内容
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        shutil.move(src_path, dst_path)

    # 删除源目录
    shutil.rmtree(src_dir)


if __name__ == "__main__":

    label_dir = img_dir.replace("images", "labels")
    temp_img_dir = img_dir.replace("images", "images2")
    temp_label_dir = label_dir.replace("labels", "labels2")

    for i in range(int(augmentation_factor - 1)):
        augmenter = YOLOv8AlbumentationsAugmenter(
            output_img_dir=temp_img_dir,
            output_label_dir=temp_label_dir
        )
        augmenter.batch_augment()

    move_and_delete_folder(temp_img_dir, img_dir)
    move_and_delete_folder(temp_label_dir, label_dir)

    print("数据增强完成")
