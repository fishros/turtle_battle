
from time import time
from rclpy.node import Node
from functools import partial

from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from turtlesim.srv import Kill
import random,math,time


class TurtleSpawner(Node):
    def __init__(self) -> None:
        super().__init__("turtle_spawner")
        self.declare_parameter("object_name","sex_girl")
        self.turtle_name = self.get_parameter("object_name").value
        # 自己的位置
        self.pose_ = None
        self.turtle_counter_ = 0
        self.object_name = "艳娘"
        self.pose_subscriber_ = self.create_subscription(
            Pose, "turtle1/pose", self.callback_turtle_pose, 10)
        self.spawn_new_turtle()
        self.object_pose = {"x":0, "y":0, "theta":0}
        self.control_loop_timer_ = self.create_timer(0.1, self.control_loop)
        #计时器
        self.tick = 0
        #grade
        self.grade = 0


    def callback_turtle_pose(self, msg):
        self.pose_ = msg

        
    def control_loop(self):
        if self.pose_ == None :
            return
        dist_x = self.object_pose["x"] - self.pose_.x
        dist_y = self.object_pose["y"] - self.pose_.y
        distance = math.sqrt(dist_x*dist_x + dist_y*dist_y)
        # self.get_logger().info("DISTANCE"+str(distance))

        if distance < 0.5:
            # position
            self.call_kill_server(self.turtle_name)
            self.grade += 10
            self.get_logger().info("恭喜你成功捕获到了"+self.object_name+"一次芳心，目前艳娘对你的心动值为："+str(self.grade))
            if self.grade >= 100:
                self.get_logger().info("经过你的努力，你成功获得了来自"+str(self.object_name)+"的奖励，奖励将在3秒后发放~")
                time.sleep(3)
                self.success_ward()


    def success_ward(self):
        import webbrowser
        webbrowser.open("https://www.bilibili.com/video/bv19U4y1n7CQ")


    def callback_call_spawn(self, future, turtle_name, x, y, theta):
        try:
            response = future.result()
            if response.name != "":
                self.get_logger().info(self.object_name+"已出现，快开始你的追逐吧~")
            self.object_pose["x"] = x
            self.object_pose["y"] = y
            self.object_pose["theta"] = theta
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))



    def spawn_new_turtle(self):
        name = self.turtle_name
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        self.call_spawn_server(name, x, y, theta)



    def call_spawn_server(self, turtle_name, x, y, theta):
        client = self.create_client(Spawn, "spawn")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server...")
        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_spawn, turtle_name=turtle_name, x=x, y=y, theta=theta))



    def call_kill_server(self, turtle_name):
        client = self.create_client(Kill, "kill")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server...")

        request = Kill.Request()
        request.name = turtle_name

        future = client.call_async(request)
        future.add_done_callback(
            partial(self.callback_call_kill, turtle_name=turtle_name))



    def callback_call_kill(self, future, turtle_name):
        try:
            future.result()
            self.spawn_new_turtle()
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))