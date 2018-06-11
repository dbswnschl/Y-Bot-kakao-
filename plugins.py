from selenium.webdriver import Chrome
import os




class plugin:
    def __init__(self):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        print(APP_ROOT)
        self.req = 0
        self.driver = Chrome(APP_ROOT+"/phantomjs.exe",service_log_path=os.path.devnull)

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
        try:
            self.driver.find_element_by_name("userid").send_keys("")
            self.driver.find_element_by_name("password").send_keys("")
            self.driver.find_element_by_xpath('//*[@id="loginFrm"]/a[2]').click()
        except:
            print("Login skip")
        self.driver.get("http://m.benefit.ticketmonster.co.kr/promotions/page/attendance")
        self.driver.find_element_by_xpath('//*[@id="attn_wrap"]/div/div/div[3]/div[2]/div[1]/button').click()
        print(self.driver.page_source)
    def ondisk(self):

        self.driver.get("https://ondisk.co.kr/index.php")
        try:
            self.driver.find_element_by_id("mb_id").send_keys("")
            self.driver.find_element_by_name("mb_pw").send_keys("")
            self.driver.find_element_by_xpath('//*[@id="page-login"]/form/div[2]/p[3]/input').click()
        except:
            print("로그인 생략")
        #
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to_window(self.driver.window_handles[0])
        try:
            alert = self.driver.switch_to_alert()
            alert.accept()
        except:
            print("skip alert")

        self.driver.get("http://ondisk.co.kr/index.php?mode=eventMarge&sm=event&action=view&idx=746&event_page=1")
        self.driver.switch_to_frame(1)
        self.driver.find_element_by_class_name('button').click()

        try:
            alert = self.driver.switch_to_alert()
            returntxt = alert.text
            print(alert.text)
            self.ret = alert.text
            alert.accept()
        except:
            print("skip alert")
            returntxt = "skip alert"
            self.ret = returntxt


