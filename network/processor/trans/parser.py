# -*- encoding=utf8 -*-
import struct


class TransParser:

    IP_HEADER_LENGTH = 20  # IP报文头部的长度
    UDP_HEADER_LENGTH = 8  # UDP头部的长度
    TCP_HEADER_LENGTH = 20  # TCP头部的长度


def data2str(data):
    data = struct.unpack(len(data) * 'B', data)
    str = ''
    for ch in data:
        if ch > 127 or ch < 32:
            str += '.'
        else:
            str += chr(ch)
    return str


class UDPParser(TransParser):

    @classmethod
    def parse_udp_header(cls, udp_header):
        """
        UDP报文格式
        1. 16位源端口 16位目的端口
        2. 16位UDP长度 16位UDP报文校验和
        :param udp_header:
        :return:
        """
        udp_header = struct.unpack('>HHHH', udp_header)

        # 返回结果
        # src_port 源端口
        # dst_port 目的端口
        # udp_length UDP报文长度
        # udp_checksum UDP报文校验和
        return {
            'src_port': udp_header[0],
            'dst_port': udp_header[1],
            'udp_length': udp_header[2],
            'udp_checksum': udp_header[3]
        }

    @classmethod
    def parser(cls, packet):

        return cls.parse_udp_header(packet[cls.IP_HEADER_LENGTH:cls.IP_HEADER_LENGTH + cls.UDP_HEADER_LENGTH])

        # result = cls.parse_udp_header(packet[cls.IP_HEADER_LENGTH:cls.IP_HEADER_LENGTH + cls.UDP_HEADER_LENGTH])
        # result['data'] = data2str(packet[cls.IP_HEADER_LENGTH + cls.UDP_HEADER_LENGTH:])


class TCPParser(TransParser):

    @classmethod
    def parse_tcp_header(cls, tcp_header):
        """
        TCP报文格式
        1. 16位源端口号 16位目的端口号
        2. 32位序列号
        3. 32位确认号
        4. 4位数据偏移 6位保留字段 6位TCP标记 16位窗口
        5. 16位校验和 16位紧急指针
        :param tcp_header:
        :return:
        """
        line1 = struct.unpack('>HH', tcp_header[:4])
        src_port = line1[0]
        dst_port = line1[1]
        line2 = struct.unpack('>L', tcp_header[4:8])
        seq_num = line2[0]
        line3 = struct.unpack('>L', tcp_header[8:12])
        ack_num = line3[0]
        line4 = struct.unpack('>BBH', tcp_header[12:16])  # 先按照8位、8位、16位解析
        data_offset = line4[0] >> 4  # 第一个8位右移四位获取高四位
        flags = line4[1] & int(b'00111111', 2)  # 第二个八位与00111111进行与运算获取低六位
        FIN = flags & 1
        SYN = (flags >> 1) & 1
        RST = (flags >> 2) & 1
        PSH = (flags >> 3) & 1
        ACK = (flags >> 4) & 1
        URG = (flags >> 5) & 1
        win_size = line4[2]
        line5 = struct.unpack('>HH', tcp_header[16:20])
        tcp_checksum = line5[0]
        urg_pointer = line5[1]

        # 返回结果
        # src_port 源端口
        # dst_port 目的端口
        # seq_num 序列号
        # ack_num 确认号
        # data_offset 数据偏移量
        # flags 标志位
        #     FIN 结束位
        #     SYN 同步位
        #     RST 重启位
        #     PSH 推送位
        #     ACK 确认位
        #     URG 紧急位
        # win_size 窗口大小
        # tcp_checksum TCP校验和
        # urg_pointer 紧急指针
        return {
            'src_port': src_port,
            'dst_port': dst_port,
            'seq_num': seq_num,
            'ack_num': ack_num,
            'data_offset': data_offset,
            'flags': {
                'FIN': FIN,
                'SYN': SYN,
                'RST': RST,
                'PSH': PSH,
                'ACK': ACK,
                'URG': URG
            },
            'win_size': win_size,
            'tcp_checksum': tcp_checksum,
            'urg_pointer': urg_pointer
        }

    @classmethod
    def parser(cls, packet):

        return cls.parse_tcp_header(packet[cls.IP_HEADER_LENGTH:cls.IP_HEADER_LENGTH + cls.TCP_HEADER_LENGTH])

        # result = cls.parse_tcp_header(packet[cls.IP_HEADER_LENGTH:cls.IP_HEADER_LENGTH + cls.TCP_HEADER_LENGTH])
        # result['data'] = data2str(packet[cls.IP_HEADER_LENGTH + cls.TCP_HEADER_LENGTH:])

