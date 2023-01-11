# ros2

### 執行步驟

1. `cd ros2_ws`

2. `colcon build`

3. `. install/local_setup.bash`

4. `ros2 run <package_name> <node_name>`

### Dockerfile包含yolov4 darknet環境

> 可直接執行`docker pull game48875/ros_yolo:latest`

> 建立container請加入`--gpus all`

> yolov4.weights[下載連結](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights)
