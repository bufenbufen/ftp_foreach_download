# coding: utf-8
from ftplib import FTP
import os,platform

client_path = os.getcwd()
# 判断客户端windows、linux
system = platform.system()

def ftp_connect():
    host, port, username, password = '192.168.1.1', 21, 'username', 'password'
    ftp = FTP()
    ftp.encoding = "utf-8"
    ftp.connect(host=host, port=port)
    ftp.login(user=username, passwd=password)
    ftp.set_pasv(False)
    print(ftp.getwelcome())
    return ftp


def is_dir(ftp,file_path):
    """
    获取ftp当前目录下文件夹列表，判断目标文件是否归属其中，在返回True，否则返回False
    :param ftp:
    :param file_path:
    :return:is dir-->True,not is dir -->False
    """
    dir_allinfo_list = []
    dir_list = []
    file = file_path.split(r'/')[-1]
    ftp.dir(dir_allinfo_list.append)
    # ftp.dir()
    folder_names = [line[4:] for line in dir_allinfo_list if line.startswith('d')]
    for name in folder_names:
        dir_list.append(name.split()[-1])
    if file in dir_list: return True
    return False


def is_file(ftp,file):
    pass


def get_file_path(ftp, server_path,file_list=[]):
    """
    递归爬取文件路径列表，ftp.cwd切换ftp目录，用于遍历子目录
    :param ftp:
    :param server_path:
    :param file_list:
    :return:
    """
    for file in ftp.nlst(server_path):
        if is_dir(ftp, file):
            # print('dir:{}'.format(file))
            ftp.cwd(file)
            get_file_path(ftp, os.path.join(server_path, file+'/'), file_list)
            ftp.cwd(server_path)
        else:
            # print('file:{}'.format(file))
            file_list.append(os.path.join(server_path, file))

    return file_list


def download_file(ftp, remotepath, localpath):
    """
    客户端文件夹不存在时，创建服务端同名文件夹后再下载
    :param ftp:
    :param remotepath:
    :param localpath:
    :return:
    """
    if system == "Windows":
        localdir = '\\'.join(localpath.split('\\')[:-1])
    else:
        localdir = '/'.join(localpath.split('/')[:-1])
    if not os.path.exists(localdir):
        os.mkdir(localdir)
    bufsize = 1024
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


if __name__ == '__main__':
    ftp = ftp_connect()
    server_path = ftp.pwd() + '/'
    file_path_list = get_file_path(ftp,server_path)
    # print(file_path_list)
    if not file_path_list:
        print("FTP NULL")

    for file_path in file_path_list:
        server_file_path = file_path
        # print(client_path+'\\'+server_file_path.split(server_path)[-1].replace('/','\\'))
        if system == "Windows":
            client_file_path = os.path.join(client_path+'\\', server_file_path.split(server_path)[-1].replace('/','\\'))
        else:
            client_file_path = os.path.join(client_path,server_file_path.split(server_path)[-1])
        print(server_file_path+"  ==>to==>  "+client_file_path,end="")
        try:
            download_file(ftp,server_file_path,client_file_path)
        except Exception as e:
            print("\033[0;31;40m", "\tdownload error{}".format(e), "\033[0m")
        print("\033[1;32m", "\tdownload success", "\033[0m")

    ftp.quit()
    print("爬取完成")