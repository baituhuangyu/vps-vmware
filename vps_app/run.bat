# netsh interface ip set address "连接名称" static 新IP地址 子网掩码 网关 1
# netsh interface ip set address "本地连接" static 192.168.1.108 255.255.255.0 192.168.0.1 1
netsh interface ip set address %1 static %2 %3 %4 1
