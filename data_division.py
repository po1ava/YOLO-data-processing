import os
import random
import shutil


dataset_dir = 'example'  # 数据集images与labels文件夹所在目录
training_set_ratio = 0.8  # 训练集比例（0-1）
validation_set_ratio = 0.1  # 测试集比例（0-1）
seed = 0  # 划分随机数

if __name__ == '__main__':
    random.seed(seed)

    train_images_dir = os.path.join(dataset_dir, 'train/images')
    train_labels_dir = os.path.join(dataset_dir, 'train/labels')
    val_images_dir = os.path.join(dataset_dir, 'val/images')
    val_labels_dir = os.path.join(dataset_dir, 'val/labels')
    test_images_dir = os.path.join(dataset_dir, 'test/images')
    test_labels_dir = os.path.join(dataset_dir, 'test/labels')

    # 创建训练和验证目录
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(train_labels_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
    os.makedirs(val_labels_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_labels_dir, exist_ok=True)

    # 图片和标签文件夹
    images_dir = os.path.join(dataset_dir, 'images')
    labels_dir = os.path.join(dataset_dir, 'labels')

    # 图片和标签列表
    images = [os.path.join(images_dir, f) for f in os.listdir(images_dir)]
    labels = [os.path.join(labels_dir, f) for f in os.listdir(labels_dir)]

    # 创建文件列表
    train_images = []
    train_labels = []
    val_images = []
    val_labels = []
    test_images = []
    test_labels = []

    # 随机分配数据到训练集和验证集
    for image, label in zip(images, labels):
        x = random.random()
        if x < training_set_ratio:
            train_images.append(image)
            train_labels.append(label)
        elif x < training_set_ratio + validation_set_ratio:
            val_images.append(image)
            val_labels.append(label)
        else:
            test_images.append(image)
            test_labels.append(label)

    # 移动文件到对应的目录
    for image in train_images:
        shutil.move(image, train_images_dir)
    for label in train_labels:
        shutil.move(label, train_labels_dir)

    for image in val_images:
        shutil.move(image, val_images_dir)
    for label in val_labels:
        shutil.move(label, val_labels_dir)

    for image in test_images:
        shutil.move(image, test_images_dir)
    for label in test_labels:
        shutil.move(label, test_labels_dir)

    print(f"已完成训练集、验证集、测试集数据划分")
