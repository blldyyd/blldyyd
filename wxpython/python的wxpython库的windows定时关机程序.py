# coding=utf-8
import wx#wx是gui界面库
from threading import Thread
from os import system
from time import sleep,localtime


#年列表
year=[str(i) for i in range(localtime().tm_year,localtime().tm_year+101)]
#月列表
month=[str(i) for i in range(1,13)]
#日列表
day=[str(i) for i in range(1,32)]
#小时列表
hour=[str(i) for i in range(0,24)]
#分钟列表
minute=[str(i) for i in range(0,60)]

    
class chuangkou(wx.Frame):#窗口的类
    def __init__(self):
        '''
        添加成员区域
        '''
        super(chuangkou,self).__init__(None,-1,title='Windows定时关机软件',size=(600,600))#调用父类创建窗口
        self.g=Thread(target=self.shut_down)#创建一个关机的线程
        self.a=wx.Panel(self)#创建画板
        self.b=wx.StaticText(self.a,label="请选择关机的时间")#文字提示

        self.f=wx.StaticText(self.a,label="绿色=开启，灰色=关闭")#文字提示

        self.i=wx.ComboBox(self.a,value=str(localtime().tm_year),choices=year)#选择年份框
        self.j=wx.ComboBox(self.a,value=str(localtime().tm_mon),choices=month)#选择月份框
        self.k=wx.ComboBox(self.a,value=str(localtime().tm_mday),choices=day)#选择天框
        self.d=wx.ComboBox(self.a,value=str(localtime().tm_hour),choices=hour)#选择小时框
        self.e=wx.ComboBox(self.a,value=str(localtime().tm_min),choices=minute)#选择分钟框
        '''
        成员的绑定函数区域
        '''
        self.h=wx.Button(self.a,label ='开始定时关机')#开始按钮h
        self.h.Bind(wx.EVT_BUTTON,self.start_button)#开始按钮绑定的函数
        '''
        成员的布局区域
        '''
        box=wx.BoxSizer(wx.HORIZONTAL)#创建一个垂直布局
        box1= wx.BoxSizer(wx.VERTICAL)#创建一个平行布局
        box1.Add(self.b, proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=10)#文字提示b的布局，平行占据一行在最上面
        box.Add(self.i,proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=100)#输入框i的布局，垂直
        box.Add(self.j,proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=100)#输入框j的布局，垂直
        box.Add(self.k,proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=100)#输入框k的布局，垂直
        box.Add(self.d,proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=100)#输入框d的布局，垂直
        box.Add(self.e,proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=100)#输入框e的布局，垂直
        box1.Add(box,proportion=0,flag=wx.ALIGN_CENTER)#垂直布局的，平行居中
        box1.Add(self.h, proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=50)#按钮h的布局，平行居中
        box1.Add(self.f, proportion=0, flag=wx.ALIGN_CENTER|wx.TOP,border=50)#文字f的布局，平行居中

        self.a.SetSizer(box1)#在a画板上

    def start_button(self,can):#按钮绑定函数
        if self.h.GetLabel()=="开始定时关机":#如果按钮名字是"开始定时"则执行
            print("开始了定时")
            self.h.SetLabel("关闭定时关机")#按钮名改成"关闭定时"
            self.h.SetBackgroundColour("#00FF00")#按钮变成绿色
            try:
                self.g.start()#启动关机的线程
            except:
                print("开启线程失败，已经开启了关机线程！")
        elif self.h.GetLabel()=="关闭定时关机":#如果按钮名字是"关闭定时"则执行
            print("关闭了定时")
            self.h.SetLabel("开始定时关机")#按钮名改成"开始定时"
            self.h.SetBackgroundColour(None)#按钮变成灰色

    def shut_down(self):
        __panduan=0
        while True:
            sleep(1)
            __time=localtime()
            if self.h.GetLabel()=="关闭定时关机":
                if str(__time.tm_year)+str(__time.tm_mon)+str(__time.tm_mday)+str(__time.tm_hour)+str(__time.tm_min)==\
                   self.i.GetValue()+self.j.GetValue()+self.k.GetValue()+self.d.GetValue()+self.e.GetValue():
                    if __panduan==0:
                        print('开始定时关机')
                        system('shutdown -s -f')
                        __panduan+=1
                    else:
                        continue
            else:
                if __panduan==1:
                    print('取消定时关机')
                    system('shutdown -a')
                    __panduan-=1
                else:
                    continue
                
                    
if __name__=="__main__":#主代码
    app=wx.App()#窗口初始化
    shili=chuangkou()#实例化一个窗口的类
    shili.Show()#显示窗口
    app.MainLoop()#主循环函数
