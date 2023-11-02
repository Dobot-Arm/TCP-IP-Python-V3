from dobot_api import DobotApiDashboard, DobotApi, DobotApiMove, MyType
from time import sleep

PARAMS=0
def connect_robot():
    try:
        ip = "192.168.5.1"
        dashboard_p = 29999
        move_p = 30003
        feed_p = 30004
        print("正在建立连接...")
        dashboard = DobotApiDashboard(ip, dashboard_p)
        move = DobotApiMove(ip, move_p)
        feed = DobotApi(ip, feed_p)
        print(">.<连接成功>!<")
        return dashboard, move, feed
    except Exception as e:
        print(":(连接失败:(")
        raise e

if __name__ == '__main__':
    dashboard, move, feed = connect_robot()
   
    """
    ************************************
    ************************************
        if PARAMS  条件编译 指令是否有参数
            0  指令不含参数
            1   指令含参数
            
        包括以下指令的例子：
            EnableRobot
            DisableRobot
            DO
            AccJ
            SetArmOrientation
            RunScript
            GetTraceStartPose
            PositiveSolution
            InverseSolution
            GetPose
            ModbusCreate
            GetHoldRegs
            DOGroup
            SetCollideDrag
            SetTerminal485
            MovL
            MovLIO
            MoveJog
            StartTrace
            RelMovJUser
            Circle3
    """
    
    """
    ************************************
    ************************************
     * 指令：EnableRobot
     * 功能：使能机器人
    """
    if PARAMS:
      dashboard.EnableRobot()    #无参数
    else:
       load=0.1
       centerX=0.1
       centerY=0.1
       centerZ=0.1
       dashboard.EnableRobot(load)    #一个参数
       
       dashboard.EnableRobot(load, centerX, centerY, centerZ)    #四个参数
  
    """
    ************************************
    ************************************
     * 指令：DisableRobotexit
     * 功能：下使能机器人
    """
    dashboard.DisableRobot()    #无参数
     
     
    """
    ************************************
    ************************************
     * 指令： DO
     * 功能：设置数字输出端口状态（队列指令）
    """
    index=1
    status=1
    dashboard.DO(index,status)  
     
     
    """
     *******************************
     *******************************
     * 指令： AccJ
     * 功能：设置关节加速度比例。该指令仅对MovJ、MovJIO、MovJR、 JointMovJ指令有效
    """
    index=1
    dashboard.AccJ(index)  
     
     
    """
     ******************************
     ******************************
     * 指令： SetArmOrientation
     * 功能：设置手系指令。
    """
    if PARAMS:
        LorR=1
        dashboard.SetArmOrientation(LorR)    #1个参数
    else:
        LorR=1
        UorD=1
        ForN=1
        Config=1
        dashboard.SetArmOrientation(LorR, UorD, ForN, Config)    #4个参数
    
    
    """
    ************************************
    ************************************
     * 指令： RunScript
     * 功能：运行lua脚本。
    """
    name="luaname"
    dashboard.RunScript(name)  
     
     
    """
    ************************************
    ************************************
     * 指令：GetTraceStartPose
     * 功能：获取轨迹拟合中首个点位。
    """
    traceName="name"
    dashboard.GetTraceStartPose(traceName)  
     
     
     
    """
    ************************************
    ************************************
     * 指令： PositiveSolution
     * 功能：正解。（给定机器人各关节的角度，计算出机器人末端的空间位置）
    """
    J1=0.1
    J2=0.1
    J3=0.1
    J4=0.1
    J5=0.1
    J6=0.1
    User=1
    Tool=1
    dashboard.PositiveSolution(J1, J2, J3, J4,J5,J6,User, Tool)    

     
    """
    ************************************
    ************************************
     * 指令： InverseSolution
     * 功能：逆解。（已知机器人末端的位置和姿态，计算机器人各关节的角度值）
    """  
    if PARAMS:
        J1=0.1
        J2=0.1
        J3=0.1
        J4=0.1
        J5=0.1
        J6=0.1
        User=1
        Tool=1
        dashboard.InverseSolution(J1, J2, J3, J4,J5,J6,User, Tool)    #1个参数
    else:
        J1=0.1
        J2=0.1
        J3=0.1
        J4=0.1
        J5=0.1
        J6=0.1        
        User=1
        Tool=1
        isJointNear=1
        JointNear="JointNear"
        dashboard.InverseSolution(J1, J2, J3, J4,J5,J6,User, Tool,isJointNear, JointNear)  
    
  
    """
    ************************************
    ************************************
     * 指令： GetPose
     * 功能：获取笛卡尔坐标系下机械臂的实时位姿
    """  
    if PARAMS:
        dashboard.GetPose()    
    else:
        User=1
        Tool=1
        dashboard.GetPose(User, Tool)  
    
    
    """
    ************************************
    ************************************
     * 指令： ModbusCreate
     * 功能：创建modbus主站
    """
    if PARAMS:
        ip="192.168.1.6"
        port=29999
        slave_id=1
        dashboard.ModbusCreate(ip, port, slave_id)    #3个参数
    else:
        ip="192.168.1.6"
        port=29999
        slave_id=1
        isRTU=1
        dashboard.ModbusCreate(ip, port, slave_id, isRTU)    #4个参数
     
     
    """
    ************************************
    ************************************
     * 指令： GetHoldRegs
     * 功能：读保持寄存器。
       """
    if PARAMS:
        index=1
        addr=1
        count=1
        dashboard.GetHoldRegs(index, addr, count)    #3个参数
    else:
        index=1
        addr=1
        count=1
        valType="valType"
        dashboard.GetHoldRegs(index, addr, count, valType)    #4个参数    
     
    """
    ************************************
    ************************************
     * 指令： DOGroup
     * 功能：设置输出组端口状态  (最大支持64个参数)
    """
    if PARAMS:
        index=1
        value=1
        dashboard.DOGroup(index, value)    #2个参数
    else:
        index=1
        value=1
        index2=1
        value2=1
        index32=1
        value32=1
        dashboard.DOGroup(index, value, index2, value2, index32, value32)    # 64个参数  (参数省略)
     
     
    """
    ************************************
    ************************************
     * 指令： SetCollideDrag
     * 功能：设置是否强制进入拖拽（报错状态下也能进入拖拽）
    """
    status=1
    dashboard.SetCollideDrag(status)

    """
    ************************************
    ************************************
     * 指令： SetTerminal485
     * 功能：设置末端485参数
    """
    baudRate=1
    dataLen=1
    parityBit="parityBit"
    stopBit=1
    dashboard.SetTerminal485(baudRate, dataLen, parityBit, stopBit)
 
     
    """
    ************************************
    ************************************
     * 指令： MovL
     * 功能：功能：点到点运动，目标点位为笛卡尔点位
    """
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        rx=1.0
        ry=1.0
        rz=1.0
        move.MovL(x, y, z, rx, ry, rz)    #无可选参数
    else:
        x=1.0
        y=1.0
        z=1.0
        rx=1.0
        ry=1.0
        rz=1.0
        userparam="User=1"
        toolparam="Tool=1"
        speedlparam="SpeedL=1"
        acclparam="AccL=1"
        cpparam="CP=1" 
        move.MovL(x, y, z, rx, ry, rz,userparam)    #设置user      可选参数顺序可换
        move.MovL(x, y, z, rx, ry, rz,userparam, toolparam)    #设置user tool
        move.MovL(x, y, z, rx, ry, rz,userparam, toolparam, speedlparam,)    #设置 user  tool  speedl 
        move.MovL(x, y, z, rx, ry, rz,userparam, toolparam, speedlparam, acclparam)    #设置user  user  tool  speedl accl
        move.MovL(x, y, z, rx, ry, rz,userparam, toolparam, speedlparam, acclparam, cpparam)    #设置 user  tool  speedl accl cp
     
     
    """
    ************************************
    ************************************
    * 指令： Arc
    * 功能：：从当前位置以圆弧插补方式移动至笛卡尔坐标系下的目标位置。
 	该指令需结合其他运动指令确定圆弧起始点。
    """
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        rx=1.0
        ry=1.0
        rz=1.0
        x2=1.0
        y2=1.0
        z2=1.0
        rx2=1.0
        ry2=1.0
        rz2=1.0
        move.Arc(x, y, z, rx, ry, rz,x2, y2, z2,rx2, ry2, rz2)    #无可选参数
    else:
        x=1.0
        y=1.0
        z=1.0
        rx=1.0
        ry=1.0
        rz=1.0
        x2=1.0
        y2=1.0
        z2=1.0
        rx2=1.0
        ry2=1.0
        rz2=1.0
        userparam="User=1"
        toolparam="Tool=1"
        speedlparam="SpeedL=1"
        acclparam="AccL=1"
        cpparam="CP=1" 
        move.Arc(x, y, z, rx, ry, rz,x2, y2, z2,rx2, ry2, rz2,cpparam,userparam,speedlparam, toolparam, speedlparam, acclparam)    # user tool 顺序不固定可换
 
 
    """
    ************************************
    ************************************
     * 指令： MovLIO
     * 功能：在直线运动时并行设置数字输出端口状态，目标点位为笛卡尔点位。
    """
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        rx=1.0
        ry=1.0
        rz=1.0
        Mode=1
        Distance=1
        Index=1
        Status=1
        move.MovLIO(x, y, z, rx,ry,rz, Mode, Distance, Index, Status)    #无可选参数
    else:
        x=1.0
        y=1.0
        z=1.0
        rx=1.0
        ry=1.0
        rz=1.0
        Mode=1
        Distance=1
        Index=1
        Status=1
        userparam="User=1"
        toolparam="Tool=1"
        speedlparam="SpeedL=1"
        acclparam="AccL=1"
        cpparam="CP=1" 
        move.MovLIO(x, y, z, rx,ry,rz,Mode, Distance, Index, Status,cpparam,userparam,speedlparam, toolparam, speedlparam, acclparam)    # user tool 顺序不固定可换    
     
    """
    ************************************
    ************************************
     * 指令： MoveJog
     * 功能：点动运动，不固定距离运动
    """
    if PARAMS:
        axisID=""
        move.MoveJog(axisID)           
    else:
        axisID="J1+"
        CoordType="CoordType=1"
        userparam="User=0"
        toolparam="Tool=0"
        move.MoveJog(axisID, CoordType, userparam, toolparam)    

    ##    发MoveJog()停止命令控制机器人停止运动
    move.MoveJog()
    
    
    """
    ************************************
    ************************************
     * 指令： StartTrace
     * 功能： 轨迹拟合。(轨迹文件笛卡尔点)
    """
    traceName="traceName"
    move.StartTrace(traceName)           
 
 
    """
    ************************************
    ************************************
     * 指令： RelMovJUser
     * 功能：沿用户坐标系进行相对运动指令，末端运动方式为关节运动。
    """
    x=1.0
    y=1.0
    z=1.0
    rx=1.0
    ry=1.0
    rz=1.0
    User=1
    move.RelMovJUser(x,y,z,rx,ry,rz,traceName)      
    

    """
    ************************************
    ************************************
     * 指令： Circle3
     * 功能：整圆运动，仅对笛卡尔点位生效。
    """   
    if PARAMS:
        x=1.0
        y=1.0
        z=1.0
        rx=1.0
        ry=1.0
        rz=1.0
        count=1
        move.Circle3(x, y, z, rx,ry,rz,count)           
    else:
        x=1.0
        y=1.0
        z=1.0
        r=1.0
        count=1
        userparam="User=0"
        toolparam="Tool=0"
        speedlparam="SpeedL=R"
        acclparam="AccL=R"
        move.Circle3(x, y, z, rx,ry,rz,count, userparam, toolparam, speedlparam, acclparam)       