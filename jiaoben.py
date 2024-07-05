#别骂了别骂了我知道我写的就是一坨(┬┬﹏┬┬)I know my code sucks.
#考虑到我的同事们都没有Python环境，此程序会在打包成.exe文件后再使用。我会分享一些程序打包的经验。
#Considering that none of my colleagues have a Python environment, this program will be used after it is packaged into an .exe file.
#I will share some experiences of packaging the programme.

#除了程序以外还有一个操作指南，里面有详细的使用方法。我会删除其中包含新华传媒数字资产的部分后上传。
#In addition to the programme there is an operating guide with detailed instructions on how to use it.
#I will upload it after removing the part of it that contains the digital assets of Xinhua Media.

#因为本脚本工作方法是识别图像相对位置并点击，同时为了提升识别正确率我划分了很多识别区域，因此必须用统一的分辨率本脚本才能正常运行。
#信息搜集后我选择了1920x1440这个很奇怪但每个同事的显示器都支持的分辨率。
#Because this script works by identifying the relative positions of images and clicking on them,
#and because I have divided the recognition area into many regions in order to improve the recognition rate,
#it is necessary to use a uniform resolution in order for this script to work properly.
#After information gathering I chose the strange but supported by every colleague's monitor's resolution of 1920x1440.

import pyautogui
import time
import os
from plyer import notification
#plyer在打包的时候会出问题。使用pyinstaller打包的时候请添加'--hidden-import plyer.platforms.win.notification  pythonfilename.py'
#plyer seems to have some problems with the packaged version.Please add
#'--hidden-import plyer.platforms.win.notification pythonfilename.py' when packaging with pyinstaller.
import easyocr
import cv2


reader=easyocr.Reader(['ch_sim','en'],gpu=False)
path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
#获取程序（.py或打包后的.exe）的绝对位置。将其与素材的相对位置结合以使程序在打包后仍能正确调用位置。
#Getting the absolute location of the program (.py or packed .exe).
#Combine this with the relative location of the materials so that the program can still call the correct location after it has been packaged.
time_sleep=float(input('根据网络及硬件情况，请输入点击搜索和报定后的延迟时间（单位：秒；请留出足够多的时间！至少7秒!）'
                       '\n请输入一个整数，输入后点击enter继续：'))
#’Depending on the network and hardware,
#please enter the delay time after clicking Search and Report Settings (in seconds; please allow enough time!At least 7 seconds!)'
#（At least 7 seconds!) Please enter an integer and click enter to continue:‘

#公司的平台响应速度很感人，因此不得不设置一个缓冲时间。我不知道为什么一开始测试时输入浮点数time.sleep会报错，后来也没管了。
#The b2b platform's response time sucks, so I had to set a buffer time.
#I don't know why entering a float number for time.sleep will cause an error, and idk about it later.

wether_caipei=input('是否要在当“采配库存”为0的时候添加书籍？'
                    '\n输入‘y’表示是，输入其他字符表示否（别带空格！）：')
#’Do you still want to add the book when its distributional storage is 0? Enter 'y' for yes, and any other character for no (no spaces!):‘

pyautogui.PAUSE=1.25
#记得设置按键间隔，慢点不要紧重要的是稳定。
#Remember to set the interval between keyboard inputs, it doesn't matter if it's relatively slow, what matters is its stability.

line='未识别到网页标签'
dic={'书号':'结果'}
dic_unexpected={'书号':'意料外情况'}

#这两个字典会记录每一本书的操作结果，最后会输出在result这个文件夹里。文件夹里的那些txt文件就是输出结果示例。
#These two dictionaries will record the result of each book operation and finally output in the results folder.
#The txt files in the folder are examples of the output results.

net_lable = os.path.join(path,'source/net_lable.png') #读取识别素材。Read the materia for recognition。
image_path_shuhao = os.path.join(path,'source/shuhao.png')
image_path_search_button = os.path.join(path,'source/search_button.png')
search_failed = os.path.join(path,'source/search_failed.png')
bad_gateway= os.path.join(path,'source/502_bad_gateway.png')
fahuobubu = os.path.join(path,'source/fahuobubu.png')
baoding = os.path.join(path,'source/baoding.png')
no_return=os.path.join(path,'source/no_return.png')  #并没有全部使用，但留着总归没错。Not everything is used, but I kept them just in case.

def extract_list(nested_list, element):
    for sublist in nested_list:
        if element in sublist:
            return sublist
    return None
#从嵌套列表中提取包含某一项的列表的函数，用来处理easyocr的识别结果。
#A function to extract a list containing an item from a nested list, to process the result of easyocr.
#thx 天宫AI

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
#其实，公司的平台不止响应速度感人，稳定性更加感人，会天天爆502 bad gateway的错误。这段函数能在按钮识别失败后刷新页面并为“是否重新提交表单”的对话框点“是”。
#In fact, if the response time of the b2b platform sucks, then its stability is sucker.
#This function can refresh the webpage and click'yes' for the coming dialog。


with open (os.path.join(path,'source/shuhao.txt'), 'r', encoding='utf-8') as file:
    lines = file.read().splitlines()
#读取书号并转化为数组。Read the ISBN and convert to array
#向txt中输入书号这一步我并没有写程序：直接在txt中输入内容更简单直观。打包后我会创建一个指向这个txt的快捷方式（当然，用的相对位置）。
#I didn't write a programme to enter the book number into the txt: it's easier and more intuitive to enter the content directly into the txt.
#I will create a shortcut to this txt after packaging it (in a relative position, of course).
#example：explorer.exe ISBN-book-adder-for-Xinhua-Media\_internal\source\shuhao.txt

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
        break
#在程序开始前最大化网页标签，然后点击网页标签就可以让目标界面出现在整个屏幕上，是个笨办法但有用又稳定。
#Maximising the web tab before the program starts and then clicking on the web tab
#will make the target interface appear on the whole screen, a dumb but useful and stable solution.

#旧版本pyautogui识别失败返回值是none，不是报错
#If older versions of pyautogui failed to recognise, it returns none, not an error.
for line in lines:
    butui=True
    pyautogui.click(605, 425)
    pyautogui.hotkey('ctrl','a')
    pyautogui.typewrite(line)
    pyautogui.click(1530, 425)
    time.sleep(time_sleep)
    #由于识别输入框和搜索按钮过于不稳定，最后采用了点击固定坐标的解决方案。
    #The solution of clicking on fixed coordinates was finally used because recognising given input boxes and search buttons was too unstable.

    try:
        if os.path.exists(os.path.join(path,'source/screenshot_shibie.png')):
            os.remove(os.path.join(path,'source/screenshot_shibie.png'))
        screenshot_shibie=pyautogui.screenshot(region=(820,675,270,60))
        screenshot_shibie.save(os.path.join(path, 'source/screenshot_shibie.png'))
        pretreated_shibie = cv2.imread(os.path.join(path, 'source/screenshot_shibie.png'))
        pretreated_shibie = cv2.resize(pretreated_shibie, (540, 120))
        cv2.imwrite(os.path.join(path, 'source/pretreated_shibie.png'), pretreated_shibie)   #预处理图片
        result_shibie=reader.readtext(os.path.join(path,'source/pretreated_shibie.png'),detail=0)
        shibie= result_shibie[0]
        #如果此书不存在，这个区域会显示“没有您想查看的书籍”
        #If the book doesn't exist, "没有您想查看的书籍" will present at this area
    except IndexError:
        shibie = ''
    if shibie == '没有您想查看的书籍':
        print('错误！未找到书籍：', line) #BookNotFound
        dic_unexpected.update({line: '未找到书籍'})
        continue
        #识别该书是否存在。Identify whether the ISBN exists.
        #如果不存在，程序会添加下一本。If it does not exist, the programme proceeds and adds the next book.

    try:
        pyautogui.locateOnScreen(os.path.join(path,'source/no_return.png'),confidence=0.65,region=(1660,680,85,215),grayscale=True)
    except pyautogui.ImageNotFoundException:
        butui=False
    if butui==True:
        print('图书不可退：', line)
        dic_unexpected.update({line: '图书不可退，请核实'}) #The book is not returnable. Please check.
        continue
        #识别图书是否可退货。Identify if the book is returnable.

    try:
        if os.path.exists(os.path.join(path,'source/screenshot_kucun.png')):
            os.remove(os.path.join(path,'source/screenshot_kucun.png'))
        screenshot_kucun=pyautogui.screenshot(region=(1310,680,100,155))
        screenshot_kucun.save(os.path.join(path, 'source/screenshot_kucun.png'))
        pretreated_kucun = cv2.imread(os.path.join(path, 'source/screenshot_kucun.png'))
        pretreated_kucun = cv2.resize(pretreated_kucun, (400, 620))
        cv2.imwrite(os.path.join(path, 'source/pretreated_kucun.png'), pretreated_kucun)   #预处理截图
        result_kucun=reader.readtext(os.path.join(path,'source/pretreated_kucun.png'),detail=0,allowlist='1234567890')
        kucun= result_kucun[0]  #识别在店库存。Identify in-store storage.
    except IndexError:
        kucun='0'
        #在店库存为0在平台上表现为不显示任何数字。
        #An in-store storage of 0 is represented on the platform by not displaying any numbers.

    if kucun!= '0':
        print(line,'在店库存不为零，为',kucun)
        dic.update({line:f'在店库存不为零，为{kucun}'}) #如果库存不为零则不用添加，领导说的。If the inventory is not zero then you don't have to add more, my superior says so.
        try:
            del dic_unexpected[line] #重试后删除报错信息。后面也一样。Delete the error message after retry.It's the same later.
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
        cv2.imwrite(os.path.join(path, 'source/pretreated_caipei.png'),pretreated_caipei)   #预处理截图。Preprocessing Screenshot.
        #这样处理截图方便我查看在哪一步的截图出了问题。
        #Handling the screenshots this way makes it easy for me to see at which step of the screenshot something went wrong.
        result_caipei = reader.readtext(os.path.join(path, 'source/pretreated_caipei.png'), detail=0,allowlist='1234567890')
        caipei = result_caipei[0] #识别采配库存。Identify distributional storage.
        print('采配库存识别结果为',result_caipei)
        if len(result_caipei)==2 and [result_caipei[-1]=='60' or result_caipei[-1]=='6']:  #检测结果是否唯一&识别纠错。Detect whether the result is unique & identify error correction
            pass
        #为什么出现’60‘或者’6‘需要重新识别的原因在user_guide里有说；若出现一个书号对应多本书则必须由人工核实。
        #The reason why '60' or '6' means error is mentioned in the user_guide.
        #In the event that an ISBN corresponds to two or more books, it must be verified manually.
        elif len(result_caipei)==1 and [caipei=='60' or caipei=='6']:
            print('此处识别可能出错，已缩小识别区域：',line)
            dic_unexpected.update({f'{line}**':'此处识别可能出错，已缩小识别区域'})   #缩小截图区域再次识别。Zoom in on the screenshot area to identify it again.
            try:
                if os.path.exists(os.path.join(path, 'source/screenshot_caipei.png')):
                    os.remove(os.path.join(path, 'source/screenshot_caipei.png'))
                screenshot_caipei = pyautogui.screenshot(region=(1220, 680, 100, 95))
                screenshot_caipei.save(os.path.join(path, 'source/screenshot_caipei.png'))
                pretreated_caipei = cv2.imread(os.path.join(path, 'source/screenshot_caipei.png'))
                pretreated_caipei = cv2.resize(pretreated_caipei, (400, 285))
                cv2.imwrite(os.path.join(path, 'source/pretreated_caipei.png'), pretreated_caipei)
                result_caipei = reader.readtext(os.path.join(path, 'source/pretreated_caipei.png'), detail=0, allowlist='1234567890')
                caipei=result_caipei[0]
                #没写成函数的原因是因为变量太多。The reason it wasn't written as a function was because there were too many variables.
                if len(result_caipei)>1:
                    print('搜索结果不唯一，请核实')
                    dic_unexpected.update({line: '搜索结果不唯一，请核实'})
                    dic_unexpected.update({f'{line}**': '核实完成'})
                    continue
            except IndexError:
                print('采配库存识别结果为空值,已使用默认值0，请核实：', line)#Distributional storage is identified as null, default value of 0 has been used, please verify
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
                #采配库存为0需要多操作几步。It requires a few more actions if distributional storage is 0 to add a book.
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.typewrite('1') #暂时没有一次性添加多本书的需求。There is no need to add more than one book at a time at this time.
                time.sleep(2)
                location_baoding = pyautogui.locateOnScreen(baoding,region=(1585,680,170,315), confidence=0.75, grayscale=True)
                pyautogui.click(location_baoding[0]+55, location_baoding[1]+20)
                dic.update({line:'添加成功！采配库存为0'})#Added successfully! Distributional storage is 0.
                #此处识别的两个按钮是浮动的，无法使用固定坐标。
                #The two buttons identified here are not fixed, so fixed coordinates cannot be used.
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
                #若识别失败则把此条书号重新添加在lines的末尾，最后重试。
                #If the recognition fails then re-add this ISBN to the end of the lines and retry in the end.
        else:
            print('采配库存识别为0，跳过', line)#跳过添书。skip adding process.
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
            dic.update({line: '添加成功！采配库存不为0'})#Added successfully! Distributional storage is not 0.
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
        #Just in case I wrote an 'else'

with open(os.path.join(path, f'result/output{time.strftime('%Y-%m-%d %H：%M',time.localtime())}.txt'), 'w', encoding='utf-8') as file:
    for key,value in dic.items():
        file.write(f'{key}:{value}\n')
    file.write(f'\n\n以下为意料外情况收录：\n')
    for key,value in dic_unexpected.items():
        file.write(f'{key}:{value}\n')
        #将结果写入txt文件。Write the result into the txt file.
print('程序结束')
notification.notify(title='程序结束', timeout=5)
