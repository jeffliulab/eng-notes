# ROS2 System Integration

## Overview

ROS2 (Robot Operating System 2) is the de facto standard middleware for robot software integration. It is not an operating system, but rather a framework that provides communication, toolchains, and an ecosystem enabling software from various subsystems to work together.

---

## Node Architecture

### One Node Per Subsystem

The core idea of ROS2: decompose the robot system into independent nodes, each responsible for one subsystem.

**Typical Robot Node Graph**:

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
  <text x="110" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">camera_node Image</text>
  <text x="110" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Capture</text>
  <rect x="210" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="280" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">lidar_node Point</text>
  <text x="280" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Cloud Capture</text>
  <rect x="380" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="450" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">imu_node</text>
  <text x="450" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Orientation Data</text>
  <rect x="210" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="210" width="3" height="50" fill="var(--dia-green)"/>
  <text x="280" y="232" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">detection_node</text>
  <text x="280" y="246" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Object Detection</text>
  <rect x="295" y="490" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="295" y="490" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="365" y="512" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">controller_node</text>
  <text x="365" y="526" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Motion Control</text>
  <rect x="295" y="350" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="295" y="350" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="365" y="372" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">planner_node Path</text>
  <text x="365" y="386" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Planning</text>
  <rect x="380" y="210" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="210" width="3" height="50" fill="var(--dia-green)"/>
  <text x="450" y="232" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">localization_node</text>
  <text x="450" y="246" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Localization</text>
  <rect x="210" y="630" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="210" y="630" width="3" height="50" fill="var(--dia-green)"/>
  <text x="280" y="652" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">motor_driver_node</text>
  <text x="280" y="666" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Motor Driver</text>
  <rect x="380" y="630" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="380" y="630" width="3" height="50" fill="var(--dia-green)"/>
  <text x="450" y="652" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">gripper_node</text>
  <text x="450" y="666" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Gripper Control</text>
  <rect x="295" y="770" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="295" y="770" width="3" height="50" fill="var(--dia-blue)"/>
  <text x="365" y="792" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">monitor_node</text>
  <text x="365" y="806" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">System Monitor</text>
  <rect x="550" y="70" width="140" height="50" rx="4" fill="var(--dia-bg-card)" stroke="var(--dia-stroke)" stroke-width="1.6"/>
  <rect x="550" y="70" width="3" height="50" fill="var(--dia-accent)"/>
  <text x="620" y="92" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">logger_node Data</text>
  <text x="620" y="106" text-anchor="middle" font-family="Fraunces, Georgia, serif" font-size="12" fill="var(--dia-stroke)">Logging</text>
</svg>
</div>


### Inter-Node Communication Patterns

| Pattern | Use | Features |
|------|------|------|
| **Topic** | Continuous data streams | Publish-Subscribe, asynchronous |
| **Service** | Request-Response | Synchronous call |
| **Action** | Long-duration tasks | With feedback and cancellable |
| **Parameter** | Configuration | Modifiable at runtime |

### Topic Example

```python
# camera_node: Publish images
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

## Launch Files

Launch files are used to start multiple nodes, set parameters, and configure remappings.

### Python Launch File

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
        # Camera node
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
        
        # LiDAR node
        Node(
            package='rplidar_ros',
            executable='rplidar_node',
            name='lidar_node',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'frame_id': 'lidar_link',
            }],
        ),
        
        # IMU node
        Node(
            package='imu_driver',
            executable='imu_node',
            name='imu_node',
            parameters=[os.path.join(pkg_dir, 'config', 'imu.yaml')],
        ),
        
        # Motor driver node
        Node(
            package='motor_driver',
            executable='motor_node',
            name='motor_driver_node',
            parameters=[os.path.join(pkg_dir, 'config', 'motors.yaml')],
        ),
        
        # Controller node
        Node(
            package='my_robot_control',
            executable='controller_node',
            name='controller_node',
            parameters=[os.path.join(pkg_dir, 'config', 'controller.yaml')],
        ),
    ])
```

### XML Launch File

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

## Parameter Management

### YAML Parameter File

```yaml
# config/controller.yaml
controller_node:
  ros__parameters:
    # Control frequency
    control_rate: 200.0  # Hz
    
    # PID parameters
    pid:
      kp: [10.0, 10.0, 10.0, 5.0, 5.0, 5.0]
      ki: [0.1, 0.1, 0.1, 0.05, 0.05, 0.05]
      kd: [1.0, 1.0, 1.0, 0.5, 0.5, 0.5]
    
    # Safety limits
    safety:
      max_velocity: 1.5      # m/s
      max_acceleration: 3.0   # m/s^2
      max_torque: 50.0        # N·m
      collision_threshold: 10.0  # N
```

### Modifying Parameters at Runtime

```bash
# View parameters
ros2 param list /controller_node
ros2 param get /controller_node pid.kp

# Dynamically modify parameters (no node restart needed)
ros2 param set /controller_node safety.max_velocity 2.0
```

---

## tf2 Coordinate Transforms

### Transform Tree

Each part of the robot has its own coordinate frame; tf2 manages the transform relationships between them.

**Typical tf Tree**:

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

### Publishing Static Transforms

Sensor positions relative to base_link (invariant transforms):

```python
# Static transform broadcaster
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped

def publish_static_transforms(self):
    t = TransformStamped()
    t.header.stamp = self.get_clock().now().to_msg()
    t.header.frame_id = 'base_link'
    t.child_frame_id = 'lidar_link'
    t.transform.translation.x = 0.1   # 10cm forward
    t.transform.translation.y = 0.0
    t.transform.translation.z = 0.15  # 15cm high
    t.transform.rotation.w = 1.0      # No rotation
    
    self.static_broadcaster.sendTransform(t)
```

### Static Transforms in Launch File

```python
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=['0.1', '0', '0.15', '0', '0', '0',
               'base_link', 'lidar_link'],
),
```

---

## URDF Robot Model

### URDF Basics

URDF (Unified Robot Description Format) describes the kinematic structure of a robot:

```xml
<?xml version="1.0"?>
<robot name="my_quadruped" xmlns:xacro="http://www.ros.org/wiki/xacro">
    
    <!-- Base -->
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
    
    <!-- Left front hip joint -->
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
    
    <!-- More joints and links... -->
</robot>
```

### Xacro Macros

Avoid repetition -- define parameterized legs with macros:

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

<!-- Instantiate four legs -->
<xacro:leg prefix="lf" x_offset="0.15" y_offset="0.1"/>
<xacro:leg prefix="rf" x_offset="0.15" y_offset="-0.1"/>
<xacro:leg prefix="lr" x_offset="-0.15" y_offset="0.1"/>
<xacro:leg prefix="rr" x_offset="-0.15" y_offset="-0.1"/>
```

### robot_state_publisher

Converts URDF + joint states into published tf transforms:

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

## Common ROS2 Packages

### Perception

| Package | Function |
|---|------|
| `usb_cam` | USB camera driver |
| `realsense2_camera` | Intel RealSense driver |
| `rplidar_ros` | RPLiDAR driver |
| `velodyne` | Velodyne LiDAR driver |
| `imu_tools` | IMU filtering/visualization |

### Control

| Package | Function |
|---|------|
| `ros2_control` | Hardware abstraction layer + controller framework |
| `ros2_controllers` | PID/Joint trajectory/Differential drive controllers |
| `moveit2` | Motion planning (manipulators) |
| `nav2` | Autonomous navigation stack |

### Tools

| Package | Function |
|---|------|
| `rviz2` | 3D visualization |
| `rqt` | GUI tool suite |
| `rosbag2` | Data recording and playback |
| `foxglove_bridge` | Web visualization |

---

## QoS Configuration

### Common QoS Policies

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# Sensor data (allow drops, want latest)
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    depth=1
)

# Control commands (must be reliably delivered)
control_qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)
```

### Real-Time Considerations

ROS2 uses DDS middleware by default. For real-time control:

- **Control loop frequency**: 200-1000 Hz typical
- **DDS latency**: Usually < 1 ms (within same machine)
- **Avoid in control loops**: Dynamic memory allocation, file I/O, network waits

```python
# Control node timer callback
def control_callback(self):
    # 1. Read sensor data (from cache, non-blocking)
    imu_data = self.latest_imu
    joint_states = self.latest_joints
    
    # 2. Compute control (pure computation, no I/O)
    torques = self.compute_control(imu_data, joint_states)
    
    # 3. Send control commands
    self.publish_torques(torques)
    
    # Total time should be < 1/control_rate
```

---

## Multi-Robot Collaboration

### Namespace Isolation

Use namespaces when running multiple identical robots:

```bash
ros2 launch my_robot bringup.launch.py namespace:=robot1
ros2 launch my_robot bringup.launch.py namespace:=robot2
```

Topics automatically become `/robot1/cmd_vel`, `/robot2/cmd_vel`, etc.

### DDS Discovery

ROS2 nodes on the same network automatically discover each other. Isolation method:

```bash
# Nodes with different domain IDs are invisible to each other
export ROS_DOMAIN_ID=42
```

---

## Related Content

- [ROS2 In-Depth Tutorial](https://jeffliulab.github.io/ai-notes/08_Embodied_Intelligence/06_Software/ROS2.md) -- Deep dive into ROS2
- [System Integration Overview](系统集成综述.md) -- Integration overview
- [Debugging and Testing](调试与测试.md) -- ROS2 debugging methods

---

## References

- ROS2 Official Documentation: [docs.ros.org](https://docs.ros.org/)
- ROS2 Design Documents: [design.ros2.org](https://design.ros2.org/)
- The Robotics Back-End: [roboticsbackend.com](https://roboticsbackend.com/)
- Macenski, S. et al., "Robot Operating System 2: Design, Architecture, and Uses In the Wild," Science Robotics, 2022
