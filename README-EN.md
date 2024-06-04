---

typora-root-url: ./images
---

Chinese version of the README -> please [click here](./README.md)

Dobot   TCP-IP-Python-V3   secondary development API interface ([TCP-IP-Python-V3 Public Chinese README](https://github.com/Dobot-Arm/TCP-IP-Python-V3.git))

# 1\. Introduction

**TCP-IP-Python-V3** is a software development kit designed by Dobot based on Python of TCP/IP protocol. It is developed based on Python language, follows the Dobot-TCP-IP control communication protocol, connects to the device terminal via Socket, and provides users with an easy-to-use API interface. Through TCP-IP-Python-V3, users can quickly connect to the Dobot device and carry out secondary development to control and use the device.

## Pre-dependency

* You can connect your computer to the network interface of the controller with a network cable, and then set the fixed IP to be in the same network segment as the controller IP. You can also connect your computer to the controller via wireless connection.
  
  When connected to LAN1 via wired connection: IP: 192.168.5.1; <br/>When connected to LAN2 via wired connection: IP: 192.168100.1; <br/>Wireless connection: IP: 192.168.1.6

* Try pinging the controller IP to make sure it is under the same network segment.

* Setup the Python environment. For details, please refer to [Python Setup and Usage](https://docs.python.org/3/using/index.html).
  
  Python configuration: pip install numpy

* This API interface and Demo are applicable to V3 series controller V3.5.5.0 and above.

## Version and Release

### Current version V1.0.0.0

| Version| Date|
|:----------:|:----------:|
| V1.0.0.0| 2023-03-07 |

# 2\. Technical support


# 3\. TCP-IP-Python-V3 control protocol

As the communication based on TCP/IP has high reliability, strong practicability and high performance with low cost, many industrial automation projects have a wide demand for controlling robots based on TCP/IP protocol. Therefore, the CR-V3 robot is designed to provide rich interfaces for interaction with external devices based on the TCP/IP protocol. For more details, see [Dobot TCP_IP Remote Control Interface Guide](https://github.com/Dobot-Arm/TCP-IP-Protocol-6AXis.git).

# 4\. Obtaining TCP-IP-Python-V3

1. Obtain the secondary development API program of Dobot  TCP-IP-Python-V3 from GitHub.
  
   ```bash
   `git clone https://github.com/Dobot-Arm/TCP-IP-Python-V3.git
   ```

2. Refer to the corresponding README.md file for use.

# 5\. File and class descriptions

1. main.py: The running entrance of the main program.

2. dobot_api.py: encapsulate the robot interface. For details, refer to the [TCP_IP Remote Control Interface Guide](https://github.com/Dobot-Arm/TCP-IP-Protocol-6AXis.git).

3. files: Files related to the alarm ID, `alarm_controller.json`: Warning alarm profile, `alarm_servo.json`: Servo alarm profile

4. PythonExample.py: Contains usage and code examples of some API interface commands

Class descriptions in the dobot_api directory:

| Class| Define|
|----------|----------|
| DobotApi| Interface class based on TCP communication, encapsulates the basic business of communication|
| DobotApiDashboard| Inherited from DobotClient, it implements the specific basic functions of the robot|
| DobotApiMove| Inherited from DobotClient, it implements the specific motion functions of the robot|
| MyType| Data type, it feeds back the robot status list|
| alarm_controller| Warning alarm configuration information|
| alarm_servo| Servo alarm configuration information|

**DobotApi**

Interface class based on TCP communication, encapsulates the basic business of communication.

```python
class DobotApi:
    def __init__(self, ip, port, *args):
    ""
    if self.port == 29999 or self.port == 30003 or self.port == 30004:
            try:
                self.socket_dobot = socket.socket()
                self.socket_dobot.connect((self.ip, self.port))
    ""        
```

**DobotApiDashboard**

Inherited from DobotClient, it can deliver some settings-related commands to the robot. It implements the specific basic functions of the robot.

```c++
class DobotApiDashboard(DobotApi):
    """
    Define class dobot_api_dashboard to establish a connection to Dobot
    """
    def EnableRobot(self,*dynParams):
      """
```

**DobotApiMove**

Inherited from DobotClient, it can deliver some motion-related commands to the robot. It implements the specific motion functions of the robot.

```python
class DobotApiMove(DobotApi):
    """
    Define class dobot_api_move to establish a connection to Dobot
    """
    def MovJ(self, x, y, z, r,*dynParams):

```

**MyType**

Data type, it feeds back the robot status.

```c++
MyType=np.dtype([('len', np.int16, ), 
                ('Reserve', np.int16, (3,) ),
```

Create control port, motion port, and feedback port respectively for TCP connection.

```python
    ip = "192.168.5.1"
    dashboardPort = 29999
    movePort = 30003
    feedPort = 30004
    print("Connecting...")
    dashboard = DobotApiDashboard(ip, dashboardPort)
    move = DobotApiMove(ip, movePort)
    feed = DobotApi(ip, feedPort)
    
```

Deliver control commands via control port to enable or disable the robot.

```python
     dashboard.EnableRobot()
     dashboard.DisableRobot()
```

Deliver motion commands via motion port to control the motion of the robot.

```python
    x=10
    y=10
    z=10
    r=10
    move.MovL(x,y,z,r)
    move.MovJ(x,y,z,r)
```

Get the robot status via the feedback port

```python
    data = bytes()
    while hasRead < 1440:
        temp = feed.socket_dobot.recv(1440 - hasRead)
        if len(temp) > 0:
            hasRead += len(temp)
            data += temp
    hasRead = 0
    feedInfo = np.frombuffer(data, dtype=MyType)
    if hex((feedInfo['test_value'][0])) == '0x123456789abcdef':
        print(feedInfo['EnableStatus'][0])   #Output device enabling status
```

**For details, see the PythonExample.py and the Demo example.**

# 7\. Common problem

**Problem 1:**  TCP connection. Port 29999/30003 cannot be connected or cannot deliver commands after connecting.

**Solution:**  If the controller version is below V3.5.6.0, you can try to upgrade the controller to V3.5.6.1 or above. If the controller version is already V3.5.6.1 or above, you can feedback the problem to technical support.

**Problem 2:** During TCP connection, the 29999 control port can send commands, but the 30003 motion port cannot send commands.

**Solution:**  If motion queue is blocked, you can try to reopen the queue by delivering **clearerror()** and **continue()** commands via port 29999.

**Problem 3:** How to judge whether the Robot motion command is in place or not

**Solution:**  It can be judged by delivering a sync command.

It can be judged by comparing the Cartesian coordinates of the target point with the actual Cartesian coordinates of the robot.

# 8\. Example

* Dobot-Demo realizes TCP control of the robot and other interactions. It connects to the control port, motion port, and feedback port of the robot respectively. It delivers motion commands to robot, and handles the abnormal status of the robot, etc.

1. Main thread: Connect to the control port, motion port, and feedback port of the robot respectively. Enable the robot.

![](/main_en.png)

2. Feedback status thread: Real-time feedback of robot status information.

![](/feed_en.png)

3. Robot motion thread: Deliver motion commands to robot.

![](/move_en.png)

4. Exception handling thread: Judge and handle the abnormal status of the robot.

![](/excetion_en.png)

**Steps to run the Demo:**

1. Obtain the secondary development API program of Dobot IP-CR-Python-V3 from GitHub.
  
   ```bash
   `git clone https://github.com/Dobot-Arm/TCP-IP-Python-V3.git
   ```

2. Connect to the robot via LAN1 interface, and set the local IP address to 192.168.5.X.
  
   Control Panel >> Network and Internet >> Network Connections.
   
   ![](netConnect_en.png)
   
   Select the connected Ethernet >> Right click >> Properties >> Internet Protocol Version (TCP/IPV4).
   
   Modify the IP address to 192.168.5.X.
   
   <img src="/updateIP_en.png" style="zoom:80%;" />

3. Open the DobotStudio Pro, connect to the robot, and set the robot mode to **TCP/IP secondary development**.
  
   ![](/checkTcpMode_en.png)

4. To run the program, you need to detect the dynamic library, open the whole directory in VsCode/PyCharm and run main.py directly.
  
   ![](/runpy.png)

**Common problem**

**Problem 1: ModuleNotFoundError :  Nomode name 'numpy'**

**Solution:** If the numpy environment is not installed, install numpy      pip install numpy.

**Problem 2: Confirm the Cartesian coordinates of the different models (CR/Nova) in Demo**

**Solution:** Confirm the Cartesian coordinates of the model and modify the coordinates in Demo.

**Make sure the robot is in a safe position before running the Demo to prevent unnecessary collisions.**
