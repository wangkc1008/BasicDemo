# -*- encoding=utf8 -*-
import socket
import json
from threadPool.Pool import ThreadPool
from threadPool.Task import AsyncTask
from network.processor.net.parser import IPParser
from network.processor.trans.parser import UDPParser, TCPParser


class ServerProcessTask(AsyncTask):

    def __init__(self, packet, *args, **kwargs):
        """
        定义异步处理任务
        :param packet:
        :param args:
        :param kwargs:
        """
        super(ServerProcessTask, self).__init__(func=self.process, *args, **kwargs)
        self.packet = packet

    def process(self):
        headers = {
            'network_header': None,
            'transport_header': None
        }

        ip_header = IPParser.parse(self.packet)
        if ip_header['protocol'] == 17:  # UDP协议
            headers['transport_header'] = UDPParser.parser(self.packet)
        elif ip_header['protocol'] == 6:
            headers['transport_header'] = TCPParser.parser(self.packet)
        headers['network_header'] = ip_header
        return headers


class Server:

    def __init__(self):
        # 创建socket 指明工作协议类型(IPv4) 套接字类型 工作具体的协议(IP协议)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

        # 设置自己的主机ip和端口
        self.ip = '192.168.31.47'
        self.port = 8888
        self.sock.bind((self.ip, self.port))

        # 设置混杂模式 接受所有经过网卡设备的数据
        self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # 初始化线程池
        self.pool = ThreadPool(10)
        self.pool.start()

    def loop_server(self):
        """
        循环读取网络数据
        :return:
        """
        while True:
            packet, addr = self.sock.recvfrom(65535)
            task = ServerProcessTask(packet)
            self.pool.put(task)
            result = task.get_result()
            result = json.dumps(result, indent=4)
            print(result)


if __name__ == '__main__':
    server = Server()
    server.loop_server()