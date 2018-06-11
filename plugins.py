from selenium.webdriver import PhantomJS
import os

import configparser
config = configparser.ConfigParser()
config.read('conf.ini')


class plugin:
    def __init__(self):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        print(APP_ROOT)
        self.req = 0
        self.driver = PhantomJS(APP_ROOT+"/phantomjs.exe",service_log_path=os.path.devnull)
        self.driver.implicitly_wait(3)
    def restart(self):
        self.__init__()
    def frame_search(self,path):
        framedict = {}
        for child_frame in self.driver.find_elements_by_tag_name('frame'):
            child_frame_name = child_frame.get_attribute('name')
            framedict[child_frame_name] = {'framepath': path, 'children': {}}
            xpath = '//frame[@name="{}"]'.format(child_frame_name)
            self.driver.switch_to.frame(self.driver.find_element_by_xpath(xpath))
            framedict[child_frame_name]['children'] = self.frame_search(
                framedict[child_frame_name]['framepath'] + [child_frame_name])

            self.driver.switch_to.default_content()
            if len(framedict[child_frame_name]['framepath']) > 0:
                for parent in framedict[child_frame_name]['framepath']:
                    parent_xpath = '//frame[@name="{}"]'.format(parent)
                    self.driver.switch_to.frame(self.driver.find_element_by_xpath(parent_xpath))
        return framedict
    def tmon(self):
        self.driver.get("https://login.ticketmonster.co.kr/user/loginform?return_url=")
        self.driver.find_element_by_name('userid').send_keys(config['ACCOUNT']['tmon_id'])
        self.driver.find_element_by_name('password').send_keys(config['ACCOUNT']['tmon_pw'])
        self.driver.find_element_by_xpath('//*[@id="loginFrm"]/a[2]').click()
        self.driver.get('http://m.benefit.ticketmonster.co.kr/promotions/page/attendance?view_mode=app')
        self.driver.find_element_by_xpath('//*[@id="attn_wrap"]/div/div/div[3]/div[2]/div[1]/button').click()

        print(self.driver.find_element_by_class_name('content').text)
        self.tmon_ret = self.driver.find_element_by_class_name('content').text
    def ondisk(self):
        self.driver.get("http://ondisk.co.kr/index.php")
        self.driver.find_element_by_xpath('//*[@id="mb_id"]').send_keys(config['ACCOUNT']['ondisk_id'])
        self.driver.find_element_by_xpath('//*[@id="page-login"]/form/div[2]/p[2]/input').send_keys(config['ACCOUNT']['ondisk_pw'])
        self.driver.find_element_by_xpath('//*[@id="page-login"]/form/div[2]/p[3]/input').click()
        self.driver.get("http://ondisk.co.kr/index.php?mode=eventMarge&sm=event&action=view&idx=746&event_page=1")
        self.driver.switch_to_frame(1)
        self.driver.execute_script("window.alert = function(msg){ window.msg = msg; };")
        self.driver.find_element_by_class_name('button').click()

        alert_text = self.driver.execute_script("return window.msg;")
        print(alert_text)
        self.ondisk_ret = alert_text



