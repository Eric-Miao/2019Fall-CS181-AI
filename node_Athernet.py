import sys
import time
import logging
import aip_packet
from access_level import utils
from access_level import mac_frame
from access_level import mac_layer
from access_level import mac_phy_config
from access_level import macfile
import nat_gateway

logger = logging.getLogger(__name__)


def print_usage():
    print('{} <-s> <filename> <protocol> <IP> <Port>\n \
        PROTOCOL_TCP=1 \
        PROTOCOL_UDP=2 \
        PROTOCOL_ICMP=3')

    print('{} <-r> <filename> <protocol>\n \
        PROTOCOL_TCP=1 \
        PROTOCOL_UDP=2 \
        PROTOCOL_ICMP=3')

    exit(-1)


class Audio_Sender:

    def __init__(self, ip, port, filename, interface, config, protocol):
        self.src = 1
        self.dest = 2
        self.buffer = utils.DataBuffer()
        self.interface = mac_layer.BaseMACLayerInterface(
            self.src, self.dest)
        self.buffer.read_from_file(filename)
        self.buffer.flush()
        self.ptl = protocol
        self.TCP_dest = (ip, int(port))
        self.TCP_src = (0, 0)

    def send(self):
        self.start_time = time.time()
        self.send_size = self.buffer.length
        self.sent_size = 0
        while True:
            try:
                raw_data, read_size = self.buffer.read(mac_frame.MAX_LENGTH)
                if read_size == 0:
                    self.end_time = time.time()
                    print('send finished')
                    break
                data = self._gen_TCP_frame(raw_data, aip_packet.TYPE_DATA)
                # assert isinstance(data, bytes)
                self.interface.send(
                    data, read_size, mac_frame.TYPE_UPPER_LAYER)
                self.sent_size += read_size
            except BaseException as e:
                print("Send failed: {}".format(e))
                self.end_time = time.time()
                break
        self._print_stat()

    def send_ICMP(self):
        self.start_time = time.time()
        self.send_size = self.buffer.length
        self.sent_size = 0
        mid_time = self.start_time
        recv_buffer = mac_frame.MACBuffer(name="File")
        while True:
            try:
              while True:
                raw_data = 'this is a ICMP ICMP Echo Request.'
                read_size = len(raw_data)
                data = self._gen_TCP_frame(raw_data, aip_packet.TYPE_DATA)
                # assert isinstance(data, bytes)
                self.interface.send(
                    data, read_size, mac_frame.TYPE_UPPER_LAYER)
                print("Awaiting ICMP Echo...")
                self.interface.receive(recv_buffer)
                ack_frame = recv_buffer.read_frame()
                if ack_frame.type == mac_frame.TYPE_MAC_ACK:
                    tcp_frame = aip_packet.AIPPacket(ack_frame.data)
                    if tcp_frame.type == aip_packet.PROTOCOL_ICMP:
                      print('received echo from %s, latency = %d' %
                            (self.TCP_dest[0], time.time() - mid_time))
                      print(tcp_frame.payload)
                elif time.time() - mid_time > 10:
                  print("Resending ICMP Request...")
                  continue

            except BaseException as e:
                print("Send failed: {}".format(e))
                self.end_time = time.time()
                break
        self._print_stat()

    def _gen_TCP_frame(self, data, type):
        frame = {'type': type, 'payload': data, 'protocol': self.ptl,
                 'src': self.TCP_src, 'dest': self.TCP_dest}
        tcp_frame = aip_packet.AIPPacket(**frame)
        return tcp_frame.to_binary()

    def _print_stat(self):
        time_spent = - self.start_time + self.end_time
        speed = self.sent_size / time_spent
        print("Macfile: Transferred {}/{} bytes in {}s, avg speed: {} bytes/s.".format(
            self.sent_size, self.send_size, time_spent, speed))


class Audio_Listener:

    def __init__(self, filename, interface, config, protocol):
        self.addr = 2
        self.ptop_addr = 1
        self.filename = filename
        self.interface = mac_layer.BaseMACLayerInterface(
            self.addr, self.ptop_addr)
        # self.interface = mac_layer.MACLayerInterface(
        #     self.addr, self.ptop_addr, False)
        self.buffer = utils.DataBuffer()

    def recv(self):
        recv_buffer = mac_frame.MACBuffer(name="File")
        self.start_time = time.time()
        while True:
            try:
                self.interface.receive(recv_buffer)
                frame = recv_buffer.read_frame()
                if frame.type == mac_frame.TYPE_MAC_END_SESSION:
                    break
                else:
                    tcp_frame = aip_packet.AIPPacket(frame.data)
                    self.buffer.write(tcp_frame.to_binary())
                    print('package from', tcp_frame.src, 'recived')
            except BaseException as e:
                print("Recv error: {}".format(e))
                self.buffer.write_to_file(self.filename)
                break
        self.end_time = time.time()
        self.buffer.write(recv_buffer.read())
        self.buffer.flush()
        self.recv_size = self.buffer.length
        self._print_stat()
        self.buffer.write_to_file(self.filename)

    def _print_stat(self):
        time_spent = self.end_time - self.start_time
        speed = self.recv_size / time_spent
        print("MACFile: Transferred {} bytes in {}s, avg speed: {} bytes/s.".format(
            self.recv_size, time_spent, speed))


def get_protocol(type):
    if (type == 1):
        return aip_packet.PROTOCOL_TCP
    if (type == 2):
        return aip_packet.PROTOCOL_UDP
    if (type == 3):
        return aip_packet.PROTOCOL_ICMP


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        print_usage()
    else:
        config = mac_phy_config.default_phy_config
        interface = mac_phy_config.default_audio_interface
        filename = sys.argv[2]
        protocol = get_protocol(int(sys.argv[3]))
        if sys.argv[1] == '-r':
            Audio_Listener(filename, interface, config, protocol).recv()
        elif sys.argv[1] == '-s':
            ip = sys.argv[4]
            port = sys.argv[5]
            Audio_Sender(ip, port, filename, interface,
                         config, protocol).send()
        else:
            print_usage()
