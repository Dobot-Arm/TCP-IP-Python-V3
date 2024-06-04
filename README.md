---

typora-root-url: ./images
---

English version of the README -> please [click here](./README-EN.md)

Dobot   TCP-IP-Python-V3   二次开发api接口 （ [TCP-IP-Python-V3 Public English README](https://github.com/Dobot-Arm/TCP-IP-Python-V3.git) ）



# 1. 简介

 TCP-IP-Python-V3  是为 dobot 公司旗下基于TCP/IP协议的Python的封装设计的软件开发套件。它基于 Python 语言开发，遵循dobot-TCP-IP控制通信协议，通过socket与机器终端进行Tcp连接，  并为用户提供了易用的api接口。通过 TCP-IP-Python-V3，用户可以快速地连接dobot机器并进行二次开发对机器的控制与使用。



## 前置依赖

* 电脑可用网线连接控制器的网口，然后设置固定 IP，与控制器 IP 在同一网段下。也可无线连接控制器。

  有线连接时连接LAN1：ip为192.168.5.1, 有线连接时连接LAN2：ip为192.168100.1,  无线连接：ip为192.168.1.6

* 尝试 ping 通控制器 IP，确保在同一网段下。

* 安装Python环境，Python环境安装请参考  [Python安装指南](https://docs.python.org/zh-cn/3/using/index.html)  

  python环境配置numpy： pip install numpy 

* 此API接口与Demo适用于V3系列的3.5.5.0及以上控制器版本

  


##  版本和发布记录

###  当前版本 v1.0.0.0

|   版本   |  修改日期  |
| :------: | :--------: |
| v1.0.0.0 | 2023-10-20 |



# 2. 技术支持



# 3. TCP-IP-Python-V3 控制协议

由于基于TCP/IP的通讯具有成本低、可靠性高、实用性强、性能高等特点；许多工业自动化项目对支持TCP/IP协议控制机器人需求广泛，因此 CR-V3 机器人将设计在TCP/IP协议的基础上，提供了丰富的接口用于与外部设备的交互；有关协议更详细的信息请查阅**《[越疆TCPIP控制协议文档6AXis](https://github.com/Dobot-Arm/TCP-IP-Protocol-6AXis.git)》**



# 4. 获取 TCP-IP-Python-V3

1. 从GitHub 下载或者克隆Dobot  TCP-IP-Python-V3 二次开发api程序

   ```bash
   `git clone https://github.com/Dobot-Arm/TCP-IP-Python-V3.git
   ```

2. 参考对应的 README.md 文档使用；

   

# 5. 文件类的说明以及使用方法

1. main.py: 主程序运行入口。  

2. dobot_api.py：封装机器人接口，具体Api指令用法根据[机器人TCP/IP远程控制方案](https://github.com/Dobot-Arm/TCP-IP-Protocol-6AXis.git)自行参考和使用。

3. files：存放报警ID相关信息 , `alarm_controller.json`警告报警配置文件,`alarm_servo.json`伺服报警配置文件

4. PythonExample.py :   包含一些api接口指令的用法和代码示例来参考

dobot_api目录中的类说明：

| Class             | Define                                        |
| ----------------- | --------------------------------------------- |
| DobotApi          | 基于tcp通信的接口类，封装了通信的基础业务     |
| DobotApiDashboard | 继承于DobotClient，实现了具体的机器人基本功能 |
| DobotApiMove      | 继承于DobotClient，实现了具体的机器人运动功能 |
| MyType            | 数据类型对象，反馈机器人的状态列表            |
| alarm_controller  | 警告报警配置信息                              |
| alarm_servo       | 伺服报警配置信息                              |

**DobotApi**  

 基于tcp通信的接口类，提供对机器的tcp连接，关闭，获取ip，端口等功能， 封装了通信的基础业务。

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

   继承于DobotClient，  能发送一些设置相关的控制指令给机器人。实现了具体的机器人基本功能。  

```c++
class DobotApiDashboard(DobotApi):
    """
    Define class dobot_api_dashboard to establish a connection to Dobot
    """
    def EnableRobot(self,*dynParams):
      """
```

**DobotApiMove**  

继承于DobotClient， 能发送一些运动相关的运动指令给机器人，实现了具体的机器人运动功能。  

```python
class DobotApiMove(DobotApi):
    """
    Define class dobot_api_move to establish a connection to Dobot
    """
    def MovJ(self, x, y, z, r,*dynParams):

```

**MyType**

数据类型对象，能反馈机器人的状态信息。

```c++
MyType=np.dtype([('len', np.int16, ), 
                ('Reserve', np.int16, (3,) ),
```



分别创建控制类端口对象 ，运动类端口对象，反馈类端口对象，进行Tcp连接

```python
    ip = "192.168.5.1"
    dashboardPort = 29999
    movePort = 30003
    feedPort = 30004
    print("正在建立连接...")
    dashboard = DobotApiDashboard(ip, dashboardPort)
    move = DobotApiMove(ip, movePort)
    feed = DobotApi(ip, feedPort)
    
```

使用控制端口下发控制指令信息，进行使能，下使能操作

```python
     dashboard.EnableRobot()
     dashboard.DisableRobot()
```

使用运动端口下发运行指令信息，控制机器运动

```python
    x=10
    y=10
    z=10
    r=10
    move.MovL(x,y,z,r)
    move.MovJ(x,y,z,r)
```

通过反馈端口获取机器状态

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
        print(feedInfo['EnableStatus'][0])   #输出机器使能状态
```

   **具体使用详情请查看代码示例PythonExample.py和Demo示例**



# 7. 常见问题

问题一：  Tcp连接  29999/30003端口无法连接或者连接后无法下发指令

 解决方法：  如控制器版本是3.5.6.0版本以下，可尝试升级控制器为3.5.6.1版本及以上版本。 如机器已经是3.5.6.1版本及以上，可将问题现象和操作反馈给技术支持



问题二： Tcp连接过程中  29999控制端口能发送指令，30003运动端口发送不了指令

 解决方法：  运动队列被堵塞，尝试用29999端口下发clearerror()和 continue()指令来重新开启队列



问题三：怎么判断机器运动指令是否到位

解决方法：  可通过下发sync指令来判断机器运动指令是否到位

​                     可通过对比目标点位笛卡尔坐标值和机器实际笛卡尔坐标值来判断是否到位



# 8. 示例

* Dobot-Demo 实现Tcp对机器的控制等交互，分别对控制端口，运动端口，反馈端口进行tcp连接，通过机器运动指令完成状态来进行下发指令，且对机器异常状态进行处理等功能。

  

1.  主线程：分别对机器控制端口，运动端口，反馈端口进行连接。给机器使能，MovL移动指令等动作

![](/main.png)

2.  反馈状态线程：实时反馈机器的状态信息

![](/feed.png)

3. 机器运动线程： 给机器下发运动指令

![](/move.png)

4.  异常处理线程：对机器异常状态进行判断和处理动作

![](/excetion.png)

**Demo运行的操作步骤时序如下图所示 ：**

1. 从GitHub 获取越疆dobot  TCP-IP-Python-V3  二次开发Api程序

   ```bash
   `git clone https://github.com/Dobot-Arm/TCP-IP-Python-V3.git
   ```

2. 通过LAN1网口-连接机器端，设置本机机器IP地址为192.168.5.X  网段

   控制面板>>网络>> Internet>>网络连接  

   ![](netConnect.png)

   

   选择连接的以太网  >>  点击右键  >> 属性  >>   Internet协议版本(TCP/IPV4)

   修改ip地址为192.168.5.X网段IP

   <img src="/updateIP.png" style="zoom:80%;" />

   

3. 连接上位机DobotStudio Pro，连接机器，把机器模式切换至TCP/IP模式

   ![](/checkTcpMode.png)

   

4. 运行程序，需要检测搜索到动态库，在VsCode/PyCharm中打开整个目录，直接运行 main.py。  

   ![](/runpy.png)

   

  **常见问题：**

​     **问题一： ModuleNotFoundError :  Nomode name 'numpy'**

​    解决方法： 未安装numpy环境，  安装numpy      pip install numpy。



​    **问题二： Demo中 不同机型（CR/Nova）对应的笛卡尔坐标**

​     解决方法： 确认机型对应的笛卡尔坐标，修改Demo 坐标值。



**运行示例前请确保机器处于安全位置，防止机器发生不必要的碰撞**

