#不同屏幕分辨率需要手动调整参数
#别骂了别骂了我知道我写的就是一坨(┬┬﹏┬┬)

import pyautogui
import time
import os
from plyer import notification
import easyocr
import cv2


reader=easyocr.Reader(['ch_sim','en'],gpu=False)
path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))     #获取相对位置
time_sleep=float(input('根据网络及硬件情况，请输入点击搜索和报定后的延迟时间（单位：秒；请留出足够多的时间！至少7秒!）'
                       '\n请输入一个整数，输入后点击enter继续：'))

wether_caipei=input('是否要在当“采配库存”为0的时候添加书籍？'
                    '\n输入‘y’表示是，输入其他字符表示否（别带空格！）：')  #输入变量

pyautogui.PAUSE=1.25
line='未识别到网页标签'
dic={'书号':'结果'}
dic_unexpected={'书号':'意料外情况'} #变量初始化
net_lable = os.path.join(path,'source/net_lable.png')
image_path_shuhao = os.path.join(path,'source/shuhao.png')
image_path_search_button = os.path.join(path,'source/search_button.png')
search_failed = os.path.join(path,'source/search_failed.png')
bad_gateway= os.path.join(path,'source/502_bad_gateway.png')
fahuobubu = os.path.join(path,'source/fahuobubu.png')
baoding = os.path.join(path,'source/baoding.png')
no_return=os.path.join(path,'source/no_return.png')  #并没有全部使用，但留着总归没错

def extract_list(nested_list, element):  #从嵌套列表中提取包含某一项的列表的函数
    for sublist in nested_list:
        if element in sublist:
            return sublist
    return None

def refresh(time):   #刷新网页端方法
    pyautogui.press('f5')
    time.sleep(2)
    try:
        if os.path.exists(os.path.join(path, 'source/screenshot_refresh.png')):
                os.remove(os.path.join(path, 'source/screenshot_refresh.png'))
        screenshot_refresh = pyautogui.screenshot(region=(0,0, 1920, 500))
        screenshot_refresh.save(os.path.join(path, 'source/screenshot_refresh.png'))
        result = reader.readtext(os.path.join(path, 'source/screenshot_refresh.png'))
        target_list=extract_list(result,'确定')
        pyautogui.click(target_list[0][0][0]+5,target_list[0][0][1]+5)
        time.sleep(time)
        return None
    except Exception:
        pyautogui.press('enter')
        time.sleep(time)
        return None

with open (os.path.join(path,'source/shuhao.txt'), 'r', encoding='utf-8') as file:
    lines = file.read().splitlines()   #读取书号并转化为数组
while True:
    try:
        location_weblink = pyautogui.locateOnScreen(net_lable, confidence=0.25, region=(0, 0, 1920, 150),
                                                    grayscale=True)
        pyautogui.click(location_weblink[0], location_weblink[1])
        break
    except pyautogui.ImageNotFoundException:
        print('错误！未找到网页标签！')
        dic_unexpected.update({line:'未找到网页标签'})
        lines=[]
        break             #找到网页标签；这都找不到也该洗洗睡了

for line in lines:
    butui=True      #初始化变量
    pyautogui.click(605, 425)
    pyautogui.hotkey('ctrl','a')
    pyautogui.typewrite(line)
    pyautogui.click(1530, 425)
    time.sleep(time_sleep)      #识别书号、输入并搜索

    try:
        if os.path.exists(os.path.join(path,'soource/screenshot_shibie.png')):
            os.remove(os.path.join(path,'soource/screenshot_shibie.png'))
        screenshot_shibie=pyautogui.screenshot(region=(820,675,270,60))
        screenshot_shibie.save(os.path.join(path, 'source/screenshot_shibie.png'))
        pretreated_shibie = cv2.imread(os.path.join(path, 'source/screenshot_shibie.png'))
        pretreated_shibie = cv2.resize(pretreated_shibie, (540, 120))
        cv2.imwrite(os.path.join(path, 'source/pretreated_shibie.png'), pretreated_shibie)   #预处理图片
        result_shibie=reader.readtext(os.path.join(path,'source/pretreated_shibie.png'),detail=0)
        shibie= result_shibie[0]
    except IndexError:
        shibie = ''
    if shibie == '没有您想查看的书籍':
        print('错误！未找到书籍：', line)
        dic_unexpected.update({line: '未找到书籍'})
        continue  #识别该书是否存在

    try:
        pyautogui.locateOnScreen(os.path.join(path,'source/no_return.png'),confidence=0.65,region=(1660,680,85,215),grayscale=True)
    except pyautogui.ImageNotFoundException:
        butui=False
    if butui==True:
        print('图书不可退：', line)
        dic_unexpected.update({line: '图书不可退，请核实'})
        continue  #识别图书是否可退

    try:
        if os.path.exists(os.path.join(path,'source/screenshot_kucun.png')):
            os.remove(os.path.join(path,'source/screenshot_kucun.png'))
        screenshot_kucun=pyautogui.screenshot(region=(1310,680,100,155))
        screenshot_kucun.save(os.path.join(path, 'source/screenshot_kucun.png'))
        pretreated_kucun = cv2.imread(os.path.join(path, 'source/screenshot_kucun.png'))
        pretreated_kucun = cv2.resize(pretreated_kucun, (400, 620))
        cv2.imwrite(os.path.join(path, 'source/pretreated_kucun.png'), pretreated_kucun)   #预处理截图
        result_kucun=reader.readtext(os.path.join(path,'source/pretreated_kucun.png'),detail=0,allowlist='1234567890')
        kucun= result_kucun[0]  #识别在店库存
    except IndexError:
        kucun='0'
    if kucun!= '0':
        print(line,'在店库存不为零，为',kucun)
        dic.update({line:f'在店库存不为零，为{kucun}'})
        try:
            del dic_unexpected[line]
        except KeyError:
            pass
        continue
    try:
        if os.path.exists(os.path.join(path, 'source/screenshot_caipei.png')):
            os.remove (os.path.join(path, 'source/screenshot_caipei.png'))
        screenshot_caipei = pyautogui.screenshot(region=(1220, 680, 100, 155))
        screenshot_caipei.save(os.path.join(path, 'source/screenshot_caipei.png'))
        pretreated_caipei=cv2.imread(os.path.join(path, 'source/screenshot_caipei.png'))
        pretreated_caipei=cv2.resize(pretreated_caipei,(400,620))
        cv2.imwrite(os.path.join(path, 'source/pretreated_caipei.png'),pretreated_caipei)   #预处理截图
        result_caipei = reader.readtext(os.path.join(path, 'source/pretreated_caipei.png'), detail=0,allowlist='1234567890')
        caipei = result_caipei[0] #识别采配库存
        print('采配库存识别结果为',result_caipei)
        if len(result_caipei)==2 and [result_caipei[-1]=='60' or result_caipei[-1]=='6']:  #检测结果是否唯一&识别纠错
            pass
        elif len(result_caipei)==1 and [caipei=='60' or caipei=='6']:
            print('此处识别可能出错，已缩小识别区域：',line)
            dic_unexpected.update({f'{line}**':'此处识别可能出错，已缩小识别区域'})   #缩小区域再次识别
            try:
                if os.path.exists(os.path.join(path, 'source/screenshot_caipei.png')):
                    os.remove(os.path.join(path, 'source/screenshot_caipei.png'))
                screenshot_caipei = pyautogui.screenshot(region=(1220, 680, 100, 95))
                screenshot_caipei.save(os.path.join(path, 'source/screenshot_caipei.png'))
                pretreated_caipei = cv2.imread(os.path.join(path, 'source/screenshot_caipei.png'))
                pretreated_caipei = cv2.resize(pretreated_caipei, (400, 285))
                cv2.imwrite(os.path.join(path, 'source/pretreated_caipei.png'), pretreated_caipei)  # 预处理截图
                result_caipei = reader.readtext(os.path.join(path, 'source/pretreated_caipei.png'), detail=0, allowlist='1234567890')
                caipei=result_caipei[0]
                if len(result_caipei)>1:
                    print('搜索结果不唯一，请核实')
                    dic_unexpected.update({line: '搜索结果不唯一，请核实'})
                    dic_unexpected.update({f'{line}**': '核实完成'})
                    continue
            except IndexError:
                print('采配库存识别结果为空值,已使用默认值0，请核实：', line)
                dic_unexpected.update({f'{line}*': '采配库存识别结果为空值，已使用默认值0，请核实'})
                caipei = '0'
                dic_unexpected.update({f'{line}**': '核实完成'})
        else:
            print('搜索结果不唯一，请核实')
            dic_unexpected.update({line: '搜索结果不唯一，请核实'})
            continue
    except IndexError:
        print('采配库存识别结果为空值,已使用默认值0，请核实：', line)
        dic_unexpected.update({f'{line}*':'采配库存识别结果为空值，已使用默认值0，请核实'})
        caipei='0'

    if caipei=='0':
        if wether_caipei=='y':
            try:
                location_fahuo = pyautogui.locateOnScreen(fahuobubu, confidence=0.55, region=(1500,680,190,170), grayscale=True)
                pyautogui.click(location_fahuo[0]+55, location_fahuo[1]+20)
                pyautogui.click(location_fahuo[0]+55, location_fahuo[1]+100)
                pyautogui.click(location_fahuo[0]-75, location_fahuo[1]+20)
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.typewrite('1')
                time.sleep(2)
                location_baoding = pyautogui.locateOnScreen(baoding,region=(1585,680,170,315), confidence=0.75, grayscale=True)
                pyautogui.click(location_baoding[0]+55, location_baoding[1]+20)
                dic.update({line:'添加成功！采配库存为0'})
                try:
                    del dic_unexpected[line]
                except KeyError:
                    pass
                time.sleep(time_sleep)
            except pyautogui.ImageNotFoundException:
                print('发货按钮识别失败或网络中断！于',line,'处中断')
                dic_unexpected.update({line:'发货按钮识别失败或网络中断，将在最后重试'})
                notification.notify(title='发货按钮识别失败或网络中断，将在最后重试',message=line, timeout=5)
                lines.append(line)
                refresh(time_sleep)
                continue
        else:
            print('采配库存识别为0，跳过', line)
            dic.update({line: '采配库存识别为0，跳过'})
            try:
                del dic_unexpected[line]
            except KeyError:
                pass
            continue
    elif caipei!='0':
        try:
            location_fahuo = pyautogui.locateOnScreen(fahuobubu, confidence=0.55, region=(1500,680,190,170), grayscale=True)
            pyautogui.click(location_fahuo[0] - 75, location_fahuo[1] + 20)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite('1')
            time.sleep(2)
            location_baoding = pyautogui.locateOnScreen(baoding,region=(1585,680,170,315), confidence=0.75, grayscale=True)
            pyautogui.click(location_baoding[0] + 55, location_baoding[1] + 20)
            dic.update({line: '添加成功！采配库存不为0'})
            try:
                del dic_unexpected[line]
            except KeyError:
                pass
            time.sleep(time_sleep)
        except pyautogui.ImageNotFoundException:
            print('发货按钮识别失败或网络中断！于',line,'处中断')
            dic_unexpected.update({line: '发货按钮识别失败或网络中断，将在最后重试'})
            notification.notify(title='发货按钮识别失败或网络中断，将在最后重试', message=line, timeout=5)
            lines.append(line)
            refresh(time_sleep)
            continue
    else:
        print(line,'发生甚么事了,添加失败，程序极可能会在下一次循环中断我都不知道怎么搞的')
        dic_unexpected.update({line:'发生甚么事了？添加失败，我都不知道怎么搞的,程序极可能在下一次循环中断'})

with open(os.path.join(path, f'result/output{time.strftime('%Y-%m-%d %H：%M',time.localtime())}.txt'), 'w', encoding='utf-8') as file:
    for key,value in dic.items():
        file.write(f'{key}:{value}\n')
    file.write(f'\n\n以下为意料外情况收录：\n')
    for key,value in dic_unexpected.items():
        file.write(f'{key}:{value}\n')
print('程序结束')
notification.notify(title='程序结束', timeout=5)
