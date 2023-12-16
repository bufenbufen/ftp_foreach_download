#### ftp_foreach_download

自动遍历下载FTP服务器的所有文件，测试的FTP服务器操作系统：linux



#### ftp_connect方法中FTP服务器ip、port、username、password

```
def ftp_connect():
    host, port, username, password = '192.168.1.1', 21, 'username', 'password'
    ftp = FTP()
    ftp.encoding = "utf-8"
    ftp.connect(host=host, port=port)
    ftp.login(user=username, passwd=password)
    ftp.set_pasv(False)
    print(ftp.getwelcome())
    return ftp
```



#### 注意

```
使用脚本报连接错误时，可关闭本地（客户端）防火墙
```



#### windows

![](https://raw.githubusercontent.com/bufenbufen/ftp_foreach_download/main/images/windows.png)





#### linux

![](https://github.com/bufenbufen/ftp_foreach_download/blob/main/images/linux.png?raw=true)