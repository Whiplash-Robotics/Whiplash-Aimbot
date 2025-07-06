from ultralytics import YOLO
import torch

if __name__ == '__main__':
    model = YOLO("C:/Users/Ryan Zhu/Documents/GitHub/Whiplash/yolo-benchmarking/runs/detect/train11/weights/last.pt")
    model.train(resume=True, epochs=100) 
