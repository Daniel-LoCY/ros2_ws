FROM ros:foxy

RUN apt update -y

# 複製yolov4範例

RUN git clone https://github.com/AlexeyAB/darknet.git

# 安裝缺少套件

RUN apt install -y nvidia-cuda-toolkit libopencv-dev wget

WORKDIR /darknet

# 修改Makefile, 不包含CUDNN

RUN sed -i 's/GPU=0/GPU=1/g' Makefile

RUN sed -i 's/OPENCV=0/OPENCV=1/g' Makefile

RUN sed -i 's/LIBSO=0/LIBSO=1/g' Makefile

RUN make

# RUN wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights

CMD '/bin/bash'