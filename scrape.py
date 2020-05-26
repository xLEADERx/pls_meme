from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import subprocess
import sys
import pyautogui
import io
from PIL import Image
import base64
from io import BytesIO
import win32clipboard
from PIL import Image
import pyautogui
import random

CHAT_NAME = '' # Group Name

ZOOM_FULL_PATH = r''

Meme_Search_list = ['dank memes', 'memes', 'most upvoted memes', 'new memes', 'cid memes']

WAIT_FOR_DOM_TO_LOAD = 9 # Secs to wait for DOM to load content

DAY = 'TODAY' # Fetch data from YESTERDAY or TODAY

first_time = True

options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=C:\Users\Arshad\Desktop\token")

navegador = webdriver.Chrome(options=options) # Can Add Drivers Path executable_path="path/to/diver"

window_before, window_after  = '',''

def SidePanel():
    """
    Search the side panel and click the Chat Name if success return True
    """
    navegador.get("https://web.whatsapp.com/")

    window_before = navegador.window_handles[0]

    time.sleep(WAIT_FOR_DOM_TO_LOAD) 

    container = navegador.find_elements_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div')# panel-side 

    try:
        for item in container:
            name1 = item.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[1]')
            name2 = item.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[15]')
            name3 = item.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[14]')
            name4 = item.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[10]')

        for arg in [name1 , name2 , name3 , name4]:
            if CHAT_NAME in arg.text:
                arg.click()
                return True
        sys.exit(0)
    except SystemExit:
        navegador.close()
        sys.exit("Unable To Find CHAT_NAME in List")
    except Exception: 
        return False


def extractor(raw_msg):
    """
    extract metting id, password and open zoom from DAY specified 
    """
    def send_to_clipboard(clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()
        
    msg_check = False

    regex = DAY + r'\b'
    
    cords = re.search(regex, raw_msg).span(0)

    raw_msg = raw_msg[cords[0] + len(DAY) + 1:]


    raw_msg = re.split('[0-9][0-9]:[0-9][0-9]', raw_msg)

    text = raw_msg[-2].strip()

    if text == 'Pls meme':
        txtinput = navegador.find_elements_by_xpath("/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]")
        #txtinput[0].send_keys('meme test')
        img_data = str.encode(get_meme())
        #print(img_data)
        im = Image.open(io.BytesIO(base64.b64decode(img_data))).save('meme.jpg')
        filepath = 'meme.jpg'
        image = Image.open(filepath)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        send_to_clipboard(win32clipboard.CF_DIB, data)
        navegador.switch_to.window(window_before)
        txtinput[0].send_keys(Keys.CONTROL + 'v')
        time.sleep(2)
        pyautogui.click(x=925, y=524)
        pyautogui.press('enter')


    return raw_msg


def get_meme():
    first_time = True
    if True:
        navegador.execute_script("window.open('https://www.google.co.in/imghp?hl=en');")
        window_after = navegador.window_handles[1]
        navegador.switch_to.window(window_after)
        txtinput = navegador.find_elements_by_xpath("/html/body/div/div[3]/div[2]/form/div[2]/div[1]/div[1]/div/div[2]/input")
        txtinput[0].send_keys(random.choice(Meme_Search_list))
        txtinput[0].send_keys(Keys.ENTER)
        images = navegador.find_elements_by_tag_name('img')
        rand = random.randrange(0,30)
        pyautogui.press('down')
        pyautogui.press('down')
        pyautogui.press('down')
        time.sleep(3)

        while True:
            for i,img in enumerate(images[:30]):
                if i == rand:
                    print(rand)
                    src = img.get_attribute('src')
                    if src != None and src[-1] == '=':
                        src = src[str(src).find('/9'):]
                        navegador.close()
                        first_time = False
                        break
                    rand = random.randrange(0,30)
            if first_time == False:
                break
        return src
                    
      

#main block
if __name__ == '__main__':

    while True:
        if SidePanel():
            break
        print('Error could not read the DOM content Retrying in 3 Secs...')
        time.sleep(3)

    messages = navegador.find_elements_by_xpath('/html/body/div[1]/div/div/div[4]/div/div[3]/div/div/div[3]') # Path for messages section Scrape messages inside the sender section
      
      
    while True:
        for msg in messages:
            raw_msg = msg.text
            parsed_msg = extractor(raw_msg)
        time.sleep(1)

