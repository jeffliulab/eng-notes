# ROS2 系统集成

## 概述

ROS2（Robot Operating System 2）是机器人软件集成的事实标准中间件。它不是操作系统，而是提供通信、工具链和生态系统的框架，让各子系统的软件能够协同工作。

---

## 节点（Node）架构

### 每个子系统一个节点

ROS2 的核心思想：将机器人系统分解为独立的节点（Node），每个节点负责一个子系统。

**典型机器人的节点图**：

<div class="diagram">
<svg viewBox="0 0 730 860" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="arr-m0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="var(--dia-stroke)"/></marker></defs>
  
  <line x1="110" y1="120" x2="280" y2="210" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="280" y1="120" x2="450" y2="210" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="450" y1="120" x2="450" y2="210" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="280" y1="260" x2="365" y2="350" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="450" y1="260" x2="365" y2="350" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="365" y1="400" x2="365" y2="490" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="365" y1="540" x2="280" y2="630" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="365" y1="540" x2="450" y2="630" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <line x1="280" y1="680" x2="365" y2="770" stroke="var(--dia-stroke)" stroke-width="1.5" marker-end="url(#arr-m0)"/>
  <rect x="40" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="40" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="110" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">camera_node 图像采集</text>
  <rect x="210" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">lidar_node 点云采集</text>
  <rect x="380" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">imu_node 姿态数据</text>
  <rect x="210" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="210" width="3" height="50" fill="var(--dia-green)"/>
  <text x="280" y="232" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">detection_node</text>
  <text x="280" y="246" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">目标检测</text>
  <rect x="295" y="490" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="295" y="490" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="365" y="512" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">controller_node</text>
  <text x="365" y="526" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">运动控制</text>
  <rect x="295" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="295" y="350" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="365" y="379" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">planner_node 路径规划</text>
  <rect x="380" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="210" width="3" height="50" fill="var(--dia-green)"/>
  <text x="450" y="232" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">localization_node</text>
  <text x="450" y="246" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">定位</text>
  <rect x="210" y="630" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="630" width="3" height="50" fill="var(--dia-green)"/>
  <text x="280" y="652" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">motor_driver_node</text>
  <text x="280" y="666" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">电机驱动</text>
  <rect x="380" y="630" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="630" width="3" height="50" fill="var(--dia-green)"/>
  <text x="450" y="659" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">gripper_node 夹爪控制</text>
  <rect x="295" y="770" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="295" y="770" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="365" y="799" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">monitor_node 系统监控</text>
  <rect x="550" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="550" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="620" y="99" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">logger_node 数据记录</text>
</svg>
</div>


### 节点间通信模式

| 模式 | 用途 | 特点 |
|------|------|------|
| **Topic（话题）** | 持续数据流 | 发布-订阅，异步 |
| **Service（服务）** | 请求-响应 | 同步调用 |
| **Action（动作）** | 长时间任务 | 带反馈和可取消 |
| **Parameter（参数）** | 配置 | 运行时可修改 |

### 话题示例

```python
# camera_node: 发布图像
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(0.033, self.timer_callback)  # 30Hz
        self.cap = cv2.VideoCapture(0)
        self.bridge = CvBridge()
    
    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, 'bgr8')
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = 'camera_link'
            self.publisher.publish(msg)
```

---

## Launch 文件

Launch 文件用于启动多个节点、设置参数、配置重映射。

### Python Launch 文件

```python
# launch/robot_bringup.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_robot')
    
    return LaunchDescription([
        # 相机节点
        Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name='camera_node',
            parameters=[{
                'video_device': '/dev/video0',
                'image_width': 640,
                'image_height': 480,
                'framerate': 30.0,
            }],
            remappings=[
                ('/image_raw', '/camera/image_raw'),
            ],
        ),
        
        # LiDAR 节点
        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='lidar_node',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'frame_id': 'lidar_link',
            }],
        ),
        
        # IMU 节点
        Node(
            package='imu_driver',
            executable='imu_node',
            name='imu_node',
            parameters=[os.path.join(pkg_dir, 'config', 'imu.yaml')],
        ),
        
        # 电机驱动节点
        Node(
            package='motor_driver',
            executable='motor_node',
            name='motor_driver_node',
            parameters=[os.path.join(pkg_dir, 'config', 'motors.yaml')],
        ),
        
        # 控制器节点
        Node(
            package='my_robot_control',
            executable='controller_node',
            name='controller_node',
            parameters=[os.path.join(pkg_dir, 'config', 'controller.yaml')],
        ),
    ])
```

### XML Launch 文件

```xml
<!-- launch/robot_bringup.launch.xml -->
<launch>
    <node pkg="usb_cam" exec="usb_cam_node_exe" name="camera_node">
        <param name="video_device" value="/dev/video0"/>
        <param name="framerate" value="30.0"/>
    </node>
    
    <node pkg="rplidar_ros" exec="rplidar_node" name="lidar_node">
        <param name="serial_port" value="/dev/ttyUSB0"/>
    </node>
    
    <include file="$(find-pkg-share my_robot)/launch/sensors.launch.py"/>
</launch>
```

---

## 参数管理

### YAML 参数文件

```yaml
# config/controller.yaml
controller_node:
  ros__parameters:
    # 控制频率
    control_rate: 200.0  # Hz
    
    # PID 参数
    pid:
      kp: [10.0, 10.0, 10.0, 5.0, 5.0, 5.0]
      ki: [0.1, 0.1, 0.1, 0.05, 0.05, 0.05]
      kd: [1.0, 1.0, 1.0, 0.5, 0.5, 0.5]
    
    # 安全限制
    safety:
      max_velocity: 1.5      # m/s
      max_acceleration: 3.0   # m/s^2
      max_torque: 50.0        # N·m
      collision_threshold: 10.0  # N
```

### 运行时修改参数

```bash
# 查看参数
ros2 param list /controller_node
ros2 param get /controller_node pid.kp

# 动态修改参数（无需重启节点）
ros2 param set /controller_node safety.max_velocity 2.0
```

---

## tf2 坐标变换

### 坐标变换树

机器人的每个部件都有自己的坐标系，tf2 管理它们之间的变换关系。

**典型的 tf 树**：

```
world
  └── odom
        └── base_link
              ├── imu_link
              ├── lidar_link
              ├── camera_link
              │     └── camera_optical_link
              ├── left_front_hip
              │     └── left_front_thigh
              │           └── left_front_calf
              │                 └── left_front_foot
              ├── right_front_hip
              │     └── ...
              └── ...
```

### 发布静态变换

传感器相对于 base_link 的位置（不变的变换）：

```python
# 静态变换发布器
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped

def publish_static_transforms(self):
    t = TransformStamped()
    t.header.stamp = self.get_clock().now().to_msg()
    t.header.frame_id = 'base_link'
    t.child_frame_id = 'lidar_link'
    t.transform.translation.x = 0.1   # 前方 10cm
    t.transform.translation.y = 0.0
    t.transform.translation.z = 0.15  # 高 15cm
    t.transform.rotation.w = 1.0      # 无旋转
    
    self.static_broadcaster.sendTransform(t)
```

### Launch 文件中的静态变换

```python
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=['0.1', '0', '0.15', '0', '0', '0',
               'base_link', 'lidar_link'],
),
```

---

## URDF 机器人模型

### URDF 基础

URDF（Unified Robot Description Format）描述机器人的运动学结构：

```xml
<?xml version="1.0"?>
<robot name="my_quadruped" xmlns:xacro="http://www.ros.org/wiki/xacro">
    
    <!-- 基座 -->
    <link name="base_link">
        <visual>
            <geometry>
                <box size="0.4 0.2 0.1"/>
            </geometry>
            <material name="gray">
                <color rgba="0.5 0.5 0.5 1"/>
            </material>
        </visual>
        <collision>
            <geometry>
                <box size="0.4 0.2 0.1"/>
            </geometry>
        </collision>
        <inertial>
            <mass value="5.0"/>
            <inertia ixx="0.01" ixy="0" ixz="0"
                     iyy="0.02" iyz="0" izz="0.02"/>
        </inertial>
    </link>
    
    <!-- 左前髋关节 -->
    <joint name="lf_hip_joint" type="revolute">
        <parent link="base_link"/>
        <child link="lf_hip_link"/>
        <origin xyz="0.15 0.1 0" rpy="0 0 0"/>
        <axis xyz="1 0 0"/>
        <limit lower="-0.8" upper="0.8"
               velocity="10" effort="50"/>
    </joint>
    
    <link name="lf_hip_link">
        <visual>
            <geometry>
                <cylinder radius="0.02" length="0.08"/>
            </geometry>
        </visual>
        <inertial>
            <mass value="0.5"/>
            <inertia ixx="0.001" ixy="0" ixz="0"
                     iyy="0.001" iyz="0" izz="0.001"/>
        </inertial>
    </link>
    
    <!-- 更多关节和连杆... -->
</robot>
```

### Xacro 宏

避免重复——用宏定义参数化的腿：

```xml
<xacro:macro name="leg" params="prefix x_offset y_offset">
    <joint name="${prefix}_hip_joint" type="revolute">
        <parent link="base_link"/>
        <child link="${prefix}_hip_link"/>
        <origin xyz="${x_offset} ${y_offset} 0"/>
        <axis xyz="1 0 0"/>
        <limit lower="-0.8" upper="0.8" velocity="10" effort="50"/>
    </joint>
    <!-- ... -->
</xacro:macro>

<!-- 实例化四条腿 -->
<xacro:leg prefix="lf" x_offset="0.15" y_offset="0.1"/>
<xacro:leg prefix="rf" x_offset="0.15" y_offset="-0.1"/>
<xacro:leg prefix="lr" x_offset="-0.15" y_offset="0.1"/>
<xacro:leg prefix="rr" x_offset="-0.15" y_offset="-0.1"/>
```

### robot_state_publisher

将 URDF + 关节状态 → 发布 tf 变换：

```python
Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    parameters=[{
        'robot_description': open('urdf/robot.urdf').read()
    }],
),
```

---

## 常用 ROS2 包

### 感知相关

| 包 | 功能 |
|---|------|
| `usb_cam` | USB 摄像头驱动 |
| `realsense2_camera` | Intel RealSense 驱动 |
| `rplidar_ros` | RPLiDAR 驱动 |
| `velodyne` | Velodyne LiDAR 驱动 |
| `imu_tools` | IMU 滤波/可视化 |

### 控制相关

| 包 | 功能 |
|---|------|
| `ros2_control` | 硬件抽象层 + 控制器框架 |
| `ros2_controllers` | PID/关节轨迹/差速控制器 |
| `moveit2` | 运动规划（机械臂） |
| `nav2` | 自主导航栈 |

### 工具

| 包 | 功能 |
|---|------|
| `rviz2` | 3D 可视化 |
| `rqt` | GUI 工具集 |
| `rosbag2` | 数据录制回放 |
| `foxglove_bridge` | Web 可视化 |

---

## QoS 配置

### 常用 QoS 策略

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# 传感器数据（允许丢包，要最新的）
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=1
)

# 控制命令（必须可靠送达）
control_qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)
```

### 实时性考虑

ROS2 默认使用 DDS 中间件。对于实时控制：

- **控制回路频率**：200-1000 Hz 典型
- **DDS 延迟**：通常 < 1 ms（同一机器内）
- **避免在控制回路中**：动态内存分配、文件IO、网络等待

```python
# 控制节点的定时器回调
def control_callback(self):
    # 1. 读取传感器数据（从缓存，非阻塞）
    imu_data = self.latest_imu
    joint_states = self.latest_joints
    
    # 2. 计算控制（纯计算，无IO）
    torques = self.compute_control(imu_data, joint_states)
    
    # 3. 发送控制命令
    self.publish_torques(torques)
    
    # 总耗时应 < 1/control_rate
```

---

## 多机协作

### Namespace 隔离

多个相同机器人时使用 namespace：

```bash
ros2 launch my_robot bringup.launch.py namespace:=robot1
ros2 launch my_robot bringup.launch.py namespace:=robot2
```

话题自动变为 `/robot1/cmd_vel`, `/robot2/cmd_vel` 等。

### DDS Discovery

同一网络内的 ROS2 节点自动发现。隔离方法：

```bash
# 不同域 ID 的节点互不可见
export ROS_DOMAIN_ID=42
```

---

## 相关内容

- [ROS2 详细教程](https://jeffliulab.github.io/ai-notes/08_Embodied_Intelligence/06_Software/ROS2.md) — ROS2 深入学习
- [系统集成综述](系统集成综述.md) — 集成全局视图
- [调试与测试](调试与测试.md) — ROS2 调试方法

---

## 参考资源

- ROS2 官方文档: [docs.ros.org](https://docs.ros.org/)
- ROS2 设计文档: [design.ros2.org](https://design.ros2.org/)
- The Robotics Back-End: [roboticsbackend.com](https://roboticsbackend.com/)
- Macenski, S. et al., "Robot Operating System 2: Design, Architecture, and Uses In the Wild," Science Robotics, 2022
