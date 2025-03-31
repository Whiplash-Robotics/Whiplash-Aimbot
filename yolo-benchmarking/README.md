# YOLO Benchmarking

## Getting Started

### Dataset

Import the dataset from Roboflow by following the instructions in [data/README.md](data/README.md). Documentation will be made on this whole process in the future.

### Virtual Environment

To create a virtual environment, run the following commands:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Libraries

Make sure to activate the virtual environment before installing the required libraries, unless you're like that.

To install the required libraries, run the following command:

```bash
# Install required python packages
pip3 install -r requirements.txt
```

### GPU Support

If you have a CUDA-supported GPU (check [here](https://developer.nvidia.com/cuda-gpus)), then you can use your GPU instead of your CPU to train the models. Follow the steps at [this link](https://www.digitalocean.com/community/tutorials/install-cuda-cudnn-for-gpu) to install all of the required dependencies for your operating system.

Run `nvidia-smi` in your command line interface to check if it detects your GPU.

`torch.cuda.is_available()` will return `True` if your GPU is being utilized. Otherwise, it will default to using your CPU.

If pytorch still doesn't detect your GPU, run the following:

```bash
# Reinstall the following packages
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```

### Run Loader

To run the data loader and verify the dataset is being loaded correctly, use the following command:

```bash
cd src
python3 data_loader.py
```

## Sources

- v11: https://github.com/ultralytics/ultralytics
- v10: https://docs.ultralytics.com/models/yolov10/#performance
- v8: https://docs.ultralytics.com/models/yolov8/#performance-metrics
- v6: https://github.com/meituan/YOLOv6/releases
- v5: https://github.com/ultralytics/yolov5?tab=readme-ov-file
- DAMO: https://github.com/tinyvision/damo-yolo
