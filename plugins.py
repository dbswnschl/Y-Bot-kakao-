from selenium.webdriver import PhantomJS
import os
import requests
import datetime
import configparser
config = configparser.ConfigParser()
config.read('conf.ini')


class plugin:
    def __init__(self):
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        print(APP_ROOT)
        self.req = 0
        self.driver = PhantomJS(APP_ROOT+"/phantomjs",service_log_path=os.path.devnull)
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
    def ok_cash_bag(self):
        today= datetime.datetime.now().strftime("%Y%m%d")
        sess = requests.session()
        getdata = sess.get(
            "https://www.facebook.com/login.php?login_attempt=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.6%2Fdialog%2Foauth%3Fredirect_uri%3Dhttps%253A%252F%252Fmember.okcashbag.com%252Focb%252FsocialId%252FfacebookProcessor%26scope%3Dpublic_profile%252Cuser_birthday%252Cemail%26client_id%3D645711852239977%26ret%3Dlogin%26logger_id%3D91698e1d-fe1e-b325-4c13-b62636843a9e&lwv=101")
        param = {
            "lsd": "AVpmy4vJ",
            "api_key": "645711852239977",
            "cancel_url": "https://member.okcashbag.com/ocb/socialId/facebookProcessor?error=access_denied&error_code=200&error_description=Permissions+error&error_reason=user_denied#_=_",
            "display": "page",
            "enable_profile_selector": "",
            "isprivate": "",
            "legacy_return": "0",
            "profile_selector_ids": "",
            "return_session": "",
            "skip_api_login": "1",
            "signed_next": "1",
            "trynum": "1",
            "timezone": "-540",
            "lgndim": "eyJ3IjoxOTIwLCJoIjoxMDgwLCJhdyI6MTkyMCwiYWgiOjEwNDAsImMiOjI0fQ==",
            "lgnrnd": "173648_UqkK",
            "lgnjs": "1528418208",
            "email": config['ACCOUNT']['fb_id'],
            "pass": config['ACCOUNT']['fb_pw'],
            "prefill_contact_point": config['ACCOUNT']['fb_id'],
            "prefill_source": "last_login",
            "prefill_type": "contact_point",
            "first_prefill_source": "last_login",
            "first_prefill_type": "contact_point",
            "had_cp_prefilled": "true",
            "had_password_prefilled": "false"
        }
        postdata = sess.post(
            "https://www.facebook.com/login.php?login_attempt=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.6%2Fdialog%2Foauth%3Fredirect_uri%3Dhttps%253A%252F%252Fmember.okcashbag.com%252Focb%252FsocialId%252FfacebookProcessor%26scope%3Dpublic_profile%252Cuser_birthday%252Cemail%26client_id%3D645711852239977%26ret%3Dlogin%26logger_id%3D91698e1d-fe1e-b325-4c13-b62636843a9e&lwv=101",
            data=param)

        # print(postdata.text)
        postdata = sess.post(
            "https://member.okcashbag.com//ocb/socialId/socialIdLoginProcess/42100/687474703A2F2F7777772e6f6b636173686261672e636f6d2F696e6465782e646f3F6c6f67696e3D59")
        samlResponse = postdata.text.split("samlResponse.value = \"")[1].split("\"")[0]
        # print(samlResponse)
        param = {
            "samlResponse": samlResponse,
            "sst_cd": "",
            "return_url": ""
        }
        postdata = sess.post("http://www.okcashbag.com/index.do?login=Y", data=param)
        print(postdata.text.split('<span id="profileNickname" class="name">')[1].split("</span>")[0] + "님 로그인")
        print(postdata.text.split('<span id="spanUsablePoint">')[1].split('</span>')[0] + "포인트")
        getdata = sess.get("http://www.okcashbag.com/life/event/attend/attendMain.do")
        param = {
            "method": "",
            "myUrl": "",
            "recommUser": "",
            "today": today
        }
        postdata = sess.post("http://www.okcashbag.com/life/event/attend/attend.do", data=param)
        print(postdata.text)
        if len(postdata.text.split('<i class="win-point">')) > 1:
            print(postdata.text.split('<i class="win-point">')[1] + "포인트 적립")
        elif len(postdata.text.split("success")) > 1:
            print("출석체크 완료 ")
            self.ok_ret = "출석체크 완료"
        else:
            print('이미 출석체크 완료')
            self.ok_ret = "이미 출석체크 완료"




