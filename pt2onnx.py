from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolo11l.pt")
    model.export(
        format="onnx",  # 指定导出格式
        imgsz=(640, 640),  # 输入图像尺寸（与训练一致）
        simplify=True,  # 简化模型结构（推荐）
        dynamic=False,  # 是否允许动态输入尺寸（部署灵活时设为 True）
    )
