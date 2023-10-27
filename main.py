import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep
import numpy as np
import re

# 全局变量(当前坐标)
current_actual = None
algorithm_queue = None
enableStatus_robot = None
robot_state = False
robotErrorState = False
globalLockValue = threading.Lock()
globalLockState = threading.Lock()

def ConnectRobot():
    try:
        ip = "192.168.5.1"
        dashboardPort = 29999
        movePort = 30003
        feedPort = 30004
        print("正在建立连接...")
        dashboard = DobotApiDashboard(ip, dashboardPort)
        move = DobotApiMove(ip, movePort)
        feed = DobotApi(ip, feedPort)
        print(">.<连接成功>!<")
        return dashboard, move, feed
    except Exception as e:
        print(":(连接失败:(")
        raise e

def RunPoint(move: DobotApiMove, point_list: list):
    move.MovL(point_list[0], point_list[1], point_list[2], point_list[3], point_list[4], point_list[5])

def GetFeed(feed: DobotApi):
    global current_actual
    global algorithm_queue
    global enableStatus_robot
    global robotErrorState
    hasRead = 0
    while True:
        data = bytes()
        while hasRead < 1440:
            temp = feed.socket_dobot.recv(1440 - hasRead)
            if len(temp) > 0:
                hasRead += len(temp)
                data += temp
        hasRead = 0
        feedInfo = np.frombuffer(data, dtype=MyType)
        if hex((feedInfo['test_value'][0])) == '0x123456789abcdef':
            globalLockValue.acquire()
            # Refresh Properties
            current_actual = feedInfo["tool_vector_actual"][0]
            algorithm_queue = feedInfo['isRunQueuedCmd'][0]
            enableStatus_robot=feedInfo['EnableStatus'][0]
            robotErrorState= feedInfo['ErrorStatus'][0]
            globalLockValue.release()
        sleep(0.001)

def WaitArrive(point_list):
    global robot_state
    while True:
        is_arrive = True
        globalLockValue.acquire()
        if current_actual is not None:
            for index in range(6):
                if (abs(current_actual[index] - point_list[index]) > 1):
                    is_arrive = False
            globalLockState.acquire()
            if is_arrive or robot_state:
                robot_state=False
                globalLockState.release()
                globalLockValue.release()
                return
            globalLockState.release()
        globalLockValue.release()  
        sleep(0.001)

def ClearRobotError(dashboard: DobotApiDashboard):
    global robot_state
    global robotErrorState
    while True:
      globalLockValue.acquire()
      if robotErrorState:
                numbers = re.findall(r'-?\d+', dashboard.GetErrorID())
                numbers= [int(num) for num in numbers]
                if (numbers[0] == 0):
                  if (len(numbers)>1):
                    for i in numbers[1:]:
                      print("errorid",i)   
                    while True:
                            globalLockState.acquire()
                            dashboard.ClearError()
                            numberss = re.findall(r'-?\d+', dashboard.Continue())
                            if int(numberss[0])==0 :
                                robot_state=True
                                globalLockState.release()
                                break
                            globalLockState.release()
      else:  
         if  int(enableStatus_robot[0])==1 and int(algorithm_queue[0])==0:
                 while True: 
                    globalLockState.acquire()
                    numberss = re.findall(r'-?\d+', dashboard.Continue())
                    if int(numberss[0])==0 :
                        robot_state=True
                
                        globalLockState.release()
                        break
                    globalLockState.release()
      globalLockValue.release()
      sleep(5)
       
if __name__ == '__main__':
    dashboard, move, feed = ConnectRobot()
    print("开始使能...")
    dashboard.EnableRobot()
    print("完成使能:)")
    feed_thread = threading.Thread(target=GetFeed, args=(feed,))
    feed_thread.daemon = True
    feed_thread.start()
    feed_thread1 = threading.Thread(target=ClearRobotError, args=(dashboard,))
    feed_thread.daemon = True
    feed_thread1.start()
    print("循环执行...")
    point_a = [20, 280, -60, 200,10,10]
    point_b = [160, 260, -30, 170,10,10]
    while True:   
        RunPoint(move, point_a)
        WaitArrive(point_a)
        RunPoint(move, point_b)
        WaitArrive(point_b)
