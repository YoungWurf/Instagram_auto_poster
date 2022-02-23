import warnings
warnings.filterwarnings('ignore')
import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from os import system
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import shutil
from random import randint
import config

def open_chrome():
    chrome_options = Options()
    chrome_options.add_argument("/home/"+str(os.getlogin())+"/.config/google-chrome/Default")
    driver=webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    return driver

def log_in(driver,my_username,my_password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div[4]/div/div/button[1]").click()
    time.sleep(1)
    driver.find_element_by_name("username").send_keys(my_username)
    time.sleep(1)
    driver.find_element_by_name("password").send_keys(my_password)
    time.sleep(1)
    driver.find_element_by_name("password").send_keys("\ue007")
    time.sleep(5)
    now=datetime.datetime.now()
    return driver

def drag_and_drop_file(drop_target, path):
    JS_DROP_FILE = """
    var target = arguments[0],
        offsetX = arguments[1],
        offsetY = arguments[2],
        document = target.ownerDocument || document,
        window = document.defaultView || window;

    var input = document.createElement('INPUT');
    input.type = 'file';
    input.onchange = function () {
      var rect = target.getBoundingClientRect(),
          x = rect.left + (offsetX || (rect.width >> 1)),
          y = rect.top + (offsetY || (rect.height >> 1)),
          dataTransfer = { files: this.files };

      ['dragenter', 'dragover', 'drop'].forEach(function (name) {
        var evt = document.createEvent('MouseEvent');
        evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
        evt.dataTransfer = dataTransfer;
        target.dispatchEvent(evt);
      });

      setTimeout(function () { document.body.removeChild(input); }, 25);
    };
    document.body.appendChild(input);
    return input;
"""
    driver = drop_target.parent
    file_input = driver.execute_script(JS_DROP_FILE, drop_target, 0, 0)
    file_input.send_keys(path)

def make_a_post(driver,post,caption):
    driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[3]/div/button").click()
    time.sleep(randint(1,10))
    drop_link=driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div/div/div[2]/div[1]/div/div")
    drag_and_drop_file(drop_link,post)
    time.sleep(randint(1,10))
    driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button").click()
    time.sleep(randint(1,10))
    driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button").click()
    time.sleep(randint(1,10))
    driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea").send_keys(caption)
    time.sleep(randint(1,10))
    driver.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button").click()
    time.sleep(randint(1,10))
    return 0

def check_Gdrive():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    folder=config.google_folder
    file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
    counter=0
    for index, file in enumerate(file_list):
        counter+= 1
    if counter>0:
        return 0
    else:
        return 1

def download_Gdrive_photos():
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    folder=config.google_folder
    file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()
    path=os.getcwd()
    path=os.path.join(path,"instagram-photos-to-post")
    try:
        os.mkdir(path)
    except:
        print("Directory:instagram-photos-to-post already exists")
    os.chdir(path)
    for index, file in enumerate(file_list):
        file.GetContentFile(file['title'])
        file.Trash()
  
def auto_post():
    main_folder=os.getcwd()
    count_of_attempts=0
    caption="#vaptisi#gamos#stolismosvaftisis#mpomponiera"
    while True: 
        try:
            download_Gdrive_photos()
        except:
            os.chdir(main_folder) 
            print("\nNo initial photos in google drive\n")
            flag=1
            day=0
            while flag==1:
                day+= 1
                print("Waiting for new photos in Google drive , days waiting:"+str(day)+"\n")
                t = datetime.datetime.today()
                future = datetime.datetime(t.year,t.month,t.day,9,0)
                if t.hour >= 9:
                    future += datetime.timedelta(days=1)
                time.sleep((future-t).total_seconds())
                flag=check_Gdrive()
            download_Gdrive_photos(  
        os.chdir(main_folder) 
        path=os.getcwd()
        path=os.path.join(path,"instagram-photos-used")
        try:
            os.mkdir(path)
        except:
            print("Directory:instagram-photos-used already exists")
        source_dir=main_folder+'/instagram-photos-to-post'
        target_dir=main_folder+"/instagram-photos-used"
        file_names=os.listdir(source_dir)
        os.chdir(source_dir)
        for file_name in file_names:
            t = datetime.datetime.today()
            future = datetime.datetime(t.year,t.month,t.day,10,0)
            if t.hour >= 10:
                future += datetime.timedelta(days=1)
            print("\nNext post is planned for :"+str(future))
            time.sleep((future-t).total_seconds())
            count_of_attempts+= 1
            if os.path.exists(target_dir+"/"+file_name) == False:
                driver=log_in(open_chrome(),config.username,config.password) 
                time.sleep(2)
                make_a_post(driver,str(source_dir+"/"+file_name),caption)
                driver.close()
                shutil.move(os.path.join(source_dir, file_name), target_dir)
                print("\nNew instagram post!\n")
            else:
                print("\nThis photo is already posted\n")
                os.remove(source_dir+"/"+file_name)
                
def main():
    auto_post()

main()
