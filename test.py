from ultralytics import YOLO

if __name__ == '__main__':

    model = YOLO('yolo11l.pt')

    # 使用测试集评估
    results = model.val(
        data='yolo.yaml',          # 数据集配置文件
        split='test',              # 指定测试集
        batch=16,                  # 批处理大小
        plots=True,                # 生成评估图表
        conf=0.5,                  # 置信度阈值
        iou=0.5,                   # IoU阈值
        device='0',                # 使用GPU序号
        workers=0,                 # 多线程情况
    )

    # 输出模型指标
    print(f"精确率: {results.box.p}")
    print(f"召回率: {results.box.r}")
    print(f"mAP@0.5: {results.box.map50}")
    print(f"mAP@0.5-0.95: {results.box.map}")