# Dataset

## Source

- [Benchmarking test dataset](https://universe.roboflow.com/nanjing-university-eotbh/valorantyolov8/dataset/2)

## Getting Started

1. Download the Roboflow CLI using npm

```zsh
npm i -g roboflow-cli
```

2. Download the dataset from the source URL above using the Roboflow CLI

- Format is one of the supported dataset formats (like voc, yolov9, darknet, etc). See `roboflow download --help` for the full list of supported formats.

```zsh
cd ./yolo-benchmarking/data
curl -L "https://universe.roboflow.com/ds/1XZHl0LGJg?key=YuXNBlp1M4" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
```

3. Profit

The data should have been successfully imported into the data folder.

Structure:
data/
├── train/
│   ├── images/
│   │   └── *.jpg
│   └── labels/
│       └── *.txt
├── valid/
│   ├── images/
│   │   └── *.jpg
│   └── labels/
│       └── *.txt
└── test/
│   ├── images/
│   │   └── *.jpg
│   └── labels/
│       └── *.txt
├── data.yaml
├── README.dataset.txt
└── README.roboflow.txt
