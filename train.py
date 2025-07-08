import warnings

from ultralytics import YOLO

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    model = YOLO('yolo11l.pt')  # 加载预训练模型权重文件
    model.train(data='yolo.yaml',  # 指定训练数据集的配置文件路径
                cache=False,  # 是否缓存数据集以加快后续训练速度
                imgsz=640,  # 指定训练时使用的图像尺寸
                epochs=200,  # 设置训练的总轮次数
                batch=16,  # 设置每个训练批次的大小
                workers=16,  # 设置用于数据加载的线程数
                patience=50,  # 设置早停机制的耐心值
                device='0',  # 指定使用的GPU设备序号
                optimizer='SGD',  # 设置模型优化器
                )
