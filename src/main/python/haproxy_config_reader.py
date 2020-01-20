import socket


class BackendServer:
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.be_name = kwargs["be_name"]
        self.srv_id = kwargs["srv_id"]
        self.srv_name = kwargs["srv_name"]
        self.srv_addr = kwargs["srv_addr"]
        self.srv_port = kwargs["srv_port"]

    def __str__(self) -> str:
        return "BackendServer(" \
               "be_name=" + self.be_name + \
               ", srv_id=" + self.srv_id + \
               ", srv_name=" + self.srv_name + \
               ", srv_addr=" + self.srv_addr + \
               ", srv_port=" + self.srv_port + ")"


class BackendConfigurationService:
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.host = kwargs["host"]
        self.port = kwargs["port"]

    @staticmethod
    def recvall(sock):
        BUFF_SIZE = 4096 # 4 KiB
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

    def find_servers(self, be_name):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(b'show servers state api_backend\n')
            data = self.recvall(s)
        backend_servers = []
        for line in data.decode("utf-8").splitlines():
            data = line.split(" ")
            if len(data) < 2:
                continue
            # print(data)
            if not be_name == data[1]:
                continue
            srv_id = data[2]
            srv_name = data[3]
            srv_addr = data[4]
            srv_port = data[18]
            backend_server = BackendServer(be_name=be_name, srv_id=srv_id, srv_name=srv_name, srv_addr=srv_addr, srv_port=srv_port)
            backend_servers.append(backend_server)
        return backend_servers

    def set_fake_server(self, be_name, srv_id):
        updated = self.update_server(be_name, srv_id, "127.1.1.1", 444)
        for s_id in range(srv_id, srv_id + updated):
            self.disable_server(be_name, s_id)
        return updated

    def set_real_server(self, be_name, srv_id, srv_addr, srv_port):
        updated = self.update_server(be_name, srv_id, srv_addr, srv_port)
        for s_id in range(srv_id, srv_id + updated):
            self.enable_server(be_name, s_id)
        return updated

    def update_server(self, be_name, srv_id, srv_addr, srv_port):
        updated = 0
        ip_list = list({addr[-1][0] for addr in socket.getaddrinfo(srv_addr, 0, 0, 0, 0)})
        #Enable server (similar to add feature): set server be_template/websrv1 state ready
        #Disable server (similar to remove feature): set server be_template/websrv1 state maint
        #Address and port can be changed using Runtime API as usual: set server be_template/websrv1 addr 192.168.50.112 port 8000
        for ip in ip_list:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(('set server ' + be_name + '/api_srv' + str(srv_id) + ' addr ' + ip + ' port ' + str(srv_port) + '\n').encode("utf-8"))
                srv_id = srv_id + 1
                updated = updated + 1
        return updated

    def enable_server(self, be_name, srv_id):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(('set server ' + be_name + '/api_srv' + str(srv_id) + ' state ready\n').encode("utf-8"))

    def disable_server(self, be_name, srv_id):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(('set server ' + be_name + '/api_srv' + str(srv_id) + ' state maint\n').encode("utf-8"))

