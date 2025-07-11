from ultralytics import YOLO
import torch

if __name__ == '__main__':
    # Load a model
    model = YOLO("/models/YOLO11s/yolo11s.pt")

    print("Available devices:")
    if torch.cuda.is_available():
        print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
    else:
        print("CPU only")

    train_results = model.train(
        data="C:/Users/Ryan Zhu/Documents/GitHub/Whiplash/yolo-benchmarking/data/data.yaml",  # path to dataset YAML, replace with your absolute dataset path
        epochs=100,  # number of training epochs
        imgsz=640,  # training image size
        workers=12,
        batch=32,
        device="0" if torch.cuda.is_available() else "cpu",  # automatically select GPU if available, otherwise use CPU
    )

    metrics = model.val()
    # results = model("../data/test/images/astraenemy00061_jpg.rf.e92c798ccdc8afea3cca195a9267f5d8.jpg")
    # results[0].show()
    path = model.export(format="onnx")