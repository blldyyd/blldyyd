# coding=utf-8
import wx
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
        参数

        方法体
        ①start_button()#开始定时关机按钮绑定的函数
        ②shut_down()执行关机的函数
        '''
        self.g=Thread(target=self.shut_down)#创建循环判断是否关机的线程
        self.g.start()#启动关机的线程
        '''
        添加成员区域
        '''
        super(chuangkou,self).__init__(None,-1,title='Windows定时关机软件',size=(600,600))#调用父类创建窗口

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
        self.h=wx.Button(self.a,label ='开始定时关机')#开始按钮
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

    def start_button(self,can):#开始定时关机按钮绑定的函数
        '''
        本函数的作用就是当点击定时关机按钮时 改变按钮的名称和颜色
        '''
        if self.h.GetLabel()=="开始定时关机":#如果按钮名字是"开始定时关机"则执行
            print("开始了定时")
            self.h.SetLabel("关闭定时关机")#按钮名改成"关闭定时关机"
            self.h.SetBackgroundColour("#00FF00")#按钮变成绿色

        elif self.h.GetLabel()=="关闭定时关机":#如果按钮名字是"关闭定时关机"则执行
            print("关闭了定时")
            self.h.SetLabel("开始定时关机")#按钮名改成"开始定时关机"
            self.h.SetBackgroundColour(None)#按钮变成灰色

    def shut_down(self):
        '''
        循环的判断当前时间是否是输入的关机时间
        是则执行关机操作
        否则不执行
        '''
        __judge=0#用于判断是否关机，如果是0就开启定时关机并且加1 不重复执行关机操作，如果是1就取消定时关机
        while True:
            sleep(1)#休眠1秒，避免cpu负荷过高
            __time=localtime()#获取现在的时间

            if self.h.GetLabel()=="关闭定时关机":#如果按钮的名称变成了关闭定时关机就执行
                #如果当前时间等于选择框中选中的时间则执行定时关机操作
                if str(__time.tm_year)+str(__time.tm_mon)+str(__time.tm_mday)+str(__time.tm_hour)+str(__time.tm_min)==\
                   self.i.GetValue()+self.j.GetValue()+self.k.GetValue()+self.d.GetValue()+self.e.GetValue():
                    if __judge==0:#如果没开启关机操作就执行1分钟后关机
                        print('开始定时关机')
                        system('shutdown -s -f')#执行1分钟后关机
                        __judge+=1#加1的目的是避免重复执行
                    else:
                        continue

            else:#如果按钮的名称不是关闭定时关机就执行
                if __judge==1:#如果开启关机操作就取消
                    print('取消定时关机')
                    system('shutdown -a')#执行取消1分钟后关机
                    __judge-=1#减1的目的是让__judge变回0
                else:
                    continue
                
                    
if __name__=="__main__":#主代码
    app=wx.App()#窗口初始化
    shili=chuangkou()#实例化一个窗口的类
    shili.Show()#显示窗口
    app.MainLoop()#主循环函数
