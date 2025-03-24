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
roboflow download -f <format> -l ./raw https://universe.roboflow.com/nanjing-university-eotbh/valorantyolov8/dataset/2
```

3. Profit

- Hopefully you get a data yaml (haven't downloaded yet)
