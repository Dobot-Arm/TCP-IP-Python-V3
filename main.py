import threading
from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType, alarmAlarmJsonFile
from time import sleep
import numpy as np
import re

# 全局变量(当前坐标)
current_actual = [-1]
algorithm_queue = -1
enableStatus_robot = -1
robotErrorState = False
globalLockValue = threading.Lock()


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
    move.MovL(point_list[0], point_list[1], point_list[2],
              point_list[3], point_list[4], point_list[5])


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
            algorithm_queue = feedInfo['run_queued_cmd'][0]
            enableStatus_robot = feedInfo['enable_status'][0]
            robotErrorState = feedInfo['error_status'][0]
            globalLockValue.release()
        sleep(0.001)


def WaitArrive(point_list):
    while True:
        is_arrive = True
        globalLockValue.acquire()
        if current_actual is not None:
            for index in range(4):
                if (abs(current_actual[index] - point_list[index]) > 1):
                    is_arrive = False
            if is_arrive:
                globalLockValue.release()
                return
        globalLockValue.release()
        sleep(0.001)


def ClearRobotError(dashboard: DobotApiDashboard):
    global robotErrorState
    dataController, dataServo = alarmAlarmJsonFile()    # 读取控制器和伺服告警码
    while True:
        globalLockValue.acquire()
        if robotErrorState:
            numbers = re.findall(r'-?\d+', dashboard.GetErrorID())
            numbers = [int(num) for num in numbers]
            if (numbers[0] == 0):
                if (len(numbers) > 1):
                    for i in numbers[1:]:
                        alarmState = False
                        if i == -2:
                            print("机器告警 机器碰撞 ", i)
                            alarmState = True
                        if alarmState:
                            continue
                        for item in dataController:
                            if i == item["id"]:
                                print("机器告警 Controller errorid", i,
                                      item["zh_CN"]["description"])
                                alarmState = True
                                break
                        if alarmState:
                            continue
                        for item in dataServo:
                            if i == item["id"]:
                                print("机器告警 Servo errorid", i,
                                      item["zh_CN"]["description"])
                                break

                    choose = input("输入1, 将清除错误, 机器继续运行: ")
                    if int(choose) == 1:
                        dashboard.ClearError()
                        sleep(0.01)
                        dashboard.Continue()

        else:
            if int(enableStatus_robot) == 1 and int(algorithm_queue) == 0:
                dashboard.Continue()
        globalLockValue.release()
        sleep(5)


if __name__ == '__main__':
    dashboard, move, feed = ConnectRobot()
    feed_thread = threading.Thread(target=GetFeed, args=(feed,))
    feed_thread.daemon = True
    feed_thread.start()
    feed_thread1 = threading.Thread(target=ClearRobotError, args=(dashboard,))
    feed_thread1.daemon = True
    feed_thread1.start()
    print("开始使能...")
    dashboard.EnableRobot()
    print("完成使能:)")
    print("循环执行...")
    point_a = [148.021667, -325.570190, 1461.586304, -
               87.462433, 23.257524, -114.395256]
    point_b = [46.395420, -345.765656, 1463.996338, -
               87.583336, 22.516230, -133.578445]
    while True:
        RunPoint(move, point_a)
        WaitArrive(point_a)
        RunPoint(move, point_b)
        WaitArrive(point_b)
