# coding=utf-8
import wx,socket,sqlite3
from threading import Thread
from time import sleep,localtime
from datetime import datetime


host_name=socket.gethostname()#获取主机名
host_ip=socket.gethostbyname(host_name)#获取主机ip地址
socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#创建一个udp套接字
socket.bind((host_ip,8080))#绑定本机ip地址和8080端口号接收消息
conn=sqlite3.connect("liaotian.db",check_same_thread=False)#打开或者创建一个db数据文件
#创建一张存聊天记录的表
sujuku=conn.cursor()
try:
    sujuku.execute("create table ltjlu(name char(100),time char(100),neirong char(100))")
except:
    print("已经创建过表")
sujuku.close()


class chuangkou(wx.Frame):
    def __init__(self):
        '''
        方法体
        ①send_out()需要发送内容输入框的绑定函数
        ②chat_box()接收对方发送内容的函数
        ③view_records()查看聊天记录的绑定函数
        '''
        self.liaotian=0#判断是否取过消息记录
        self.c=Thread(target=self.chat_box)#创建一个线程用于接收upd数据包
        self.c.start()#开始该线程
        '''
        添加成员区域
        '''
        super(chuangkou,self).__init__(None,-1,title="对等聊天程序",size=(600,600))#继承父类创建一个窗口
        self.a=wx.Panel(self)#创建一个画板
        self.e=wx.TextCtrl(self.a,value="请输入要发送的ip地址")#创建一个输出对方ip地址的输入框
        self.f = wx.Button( self.a,wx.ID_ANY,"查看消息记录")#创建一个可以查看聊天记录的按钮
        #创建一个聊天创建的输入框
        self.d=wx.TextCtrl(self.a,style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH2|wx.BORDER_SIMPLE|wx.HSCROLL)
        self.d.SetBackgroundColour('#d1d1d1')#颜色改变为灰
        self.b = wx.TextCtrl(self.a, style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE,value="请输入要发送的内容按 回车发送")  # 创建一个输入发送聊天内容的输入框

        '''
        成员的绑定函数区域
        '''
        self.b.Bind(wx.EVT_TEXT_ENTER,self.send_out)#把该输入框绑定send_out函数
        self.f.Bind(wx.EVT_BUTTON,self.view_records)#把该按钮绑定view_resords函数
        '''
        成员的布局区域
        '''
        box=wx.BoxSizer(wx.HORIZONTAL)#创建一个垂直布局
        box1= wx.BoxSizer(wx.VERTICAL)#创建一个平行布局
        box1.Add(self.e,proportion=3, flag=wx.EXPAND|wx.TOP,border=0)#输入ip地址的输入框的布局
        box1.Add(self.f,proportion=1, flag=wx.EXPAND|wx.TOP,border=0)#查看聊天记录按钮的布局
        box1.Add(self.d,proportion=30, flag=wx.EXPAND|wx.TOP,border=0)#接收输入框的布局
        box1.Add(self.b,proportion=20, flag=wx.EXPAND|wx.TOP,border=0)#发送的输入框的布局
        
        self.a.SetSizer(box1)#布局设置在a画板上
        
    def send_out(self,can):#发送消息的函数
        '''
        该函数的作用是发送内容到指定的ip地址并且保存到聊天数据库中
        '''
        #将我发送的内容存储到数据表中
        sujuku = conn.cursor()
        try:
            sujuku.execute("insert into ltjlu(name,time,neirong) values (?,?,?)",("我发送",
                                                                                  datetime.now(),
                                                                                  self.b.GetValue()))
        except:
            print("保存数据到数据库失败")
        sujuku.close()
        conn.commit()

        try:
            # 获取输入框的内容发送到指定ip的地址上
            socket.sendto(self.b.GetValue().encode(),(self.e.GetValue(),8080))
            # 将我发送的内容输入到聊天框中
            self.d.AppendText("我发送\n"+self.b.GetValue()+"\n\n")
        except:
            print('发送字数超过上限或者没输入ip地址')

        self.b.Clear()#最后清空输入框的内容
        
    def chat_box(self):#接收对方发送消息的函数
        '''
        该函数的作用是循环不断的监听对方发送的内容
        '''
        while True:
            sleep(0.3)
            try:
                #监听对方发送的内容
                self.chuang2_1,self.chuang2_2=socket.recvfrom(1024)

                #将对方发送的内容输入到聊天框中
                self.d.AppendText(self.chuang2_2[0] + "发送\n" + self.chuang2_1.decode() + "\n\n")

                #将对方发送的内容存储到数据表中
                sujuku = conn.cursor()
                try:
                    sujuku.execute("insert into ltjlu(name,time,neirong) values (?,?,?)", (self.chuang2_2[0] + "发送", \
                                                                                           datetime.now(), \
                                                                                           self.chuang2_1))
                except:
                    pass
                sujuku.close()
                conn.commit()
            except:
                print("接收超过聊天字数\n")

    def view_records(self,can):#查看聊天记录的函数
        '''
        该函数的作用是当点击查看聊天记录按钮时从数据库中循环的读取内容并添加到聊天框中
        '''
        #如果没点击过查看聊天记录就执行
        if self.liaotian==0:
            sujuku=conn.cursor()
            ltjl=sujuku.execute("select name,time,neirong from ltjlu")
            for i in ltjl:#循环取出每一条消息并添加到聊天框
                self.d.AppendText('\n'+i[0])
                self.d.AppendText("\t\t"+i[1]+'\n')
                self.d.AppendText(i[2])
                self.d.AppendText('\n\n')
            sujuku.close()
            self.liaotian+=1#加1后再次点击查看消息记录无效

            
if __name__=="__main__":#主代码
    app=wx.App()#初始化
    shili=chuangkou()#创建实例
    shili.Show()#显示窗口
    app.MainLoop()#窗口主循环
