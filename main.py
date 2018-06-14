from selenium.webdriver import PhantomJS
from flask import Flask
from flask import request
import _thread
import plugins
import json
import time
global plugin
plugin = plugins.plugin()

app = Flask(__name__)


def flaskThread(app):
    print("start ")
def reqcheck():
    while 1:
        try:
            if plugin.req == 1:
                print("동작 시작 ondisk")
                plugin.ondisk()
                print("동작 종료 ondisk")
                plugin.req = 0
            elif plugin.req == 2:
                print("동작 시작 TMON")
                plugin.tmon()
                print("동작 종료 TMON")
                plugin.req = 0
            elif plugin.req == 3:
                print("동작 시작 OK CASH BAG")
                plugin.ok_cash_bag()
                print("동작 종료 OK CASH BAG")
                plugin.req = 0
            time.sleep(1)
        except:
            print("err")


@app.route('/keyboard')
def keyboard():
    returnobj = {

        'type': 'buttons',
        'buttons': ['요청', '최초']
    }
    return json.dumps(returnobj)
@app.route('/message', methods=['POST'])
def message():
    data = request.data.decode('utf-8')
    jdata = json.loads(data)
    print(jdata)

    if jdata['content'] == "요청":
        # t = threading.Thread(target=plugin.ondisk())
        # t.daemon = True
        # t.start()

        returnobj = {
            'message': {
                'text': "종류를 선택해 주세요.",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "온디스크",
                    "티켓몬스터",
                    "OK캐시백",
                    "최초"
                ]}
        }
        return json.dumps(returnobj)
    elif jdata['content'] == "OK캐시백":
        plugin.req = 3
        returnobj = {
            'message': {
                'text': "기능을 선택해 주세요.",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "결과보기(OK캐시백)",
                    "최초"
                ]}
        }
        return json.dumps(returnobj)
    elif jdata['content'] == "결과보기(OK캐시백)":
        if plugin.req != 0:
            txt = "요청이 진행중 입니다."
            returnobj = {
                'message': {
                    'text': txt
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": [
                        "결과보기(OK캐시백)",
                        "최초"
                    ]}
            }
        elif plugin.req == 0:
            txt = plugin.ondisk_ret
            returnobj = {
            'message': {
                'text': txt
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "최초"
                ]}
            }

        return json.dumps(returnobj)
    elif jdata['content'] == "온디스크":
        plugin.req = 1
        returnobj = {
            'message': {
                'text': "기능을 선택해 주세요.",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "결과보기(온디스크)",
                    "최초"
                ]}
        }
        return json.dumps(returnobj)
    elif jdata['content'] == "결과보기(온디스크)":
        if plugin.req == 1:
            txt = "요청이 진행중 입니다."
            returnobj = {
                'message': {
                    'text': txt
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": [
                        "결과보기(온디스크)",
                        "최초"
                    ]}
            }
        elif plugin.req == 0:
            txt = plugin.ondisk_ret
            returnobj = {
            'message': {
                'text': txt
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "티켓몬스터",
                    "최초"
                ]}
            }

        return json.dumps(returnobj)
    elif jdata['content'] == "티켓몬스터":
        plugin.req = 2
        returnobj = {
            'message': {
                'text': "기능을 선택해 주세요.",
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "결과보기(티켓몬스터)",
                    "최초"
                ]}
        }
        return json.dumps(returnobj)
    elif jdata['content']== "결과보기(티켓몬스터)":
        if plugin.req == 2:
            txt = "요청이 진행중 입니다."
            returnobj = {
                'message': {
                    'text': txt
                },
                "keyboard": {
                    "type": "buttons",
                    "buttons": [
                        "결과보기(티켓몬스터)",
                        "최초"
                    ]}
            }
        elif plugin.req == 0:
            txt = plugin.tmon_ret
            returnobj = {
            'message': {
                'text': txt
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "OK캐시백",
                    "최초"
                ]}
            }

        return json.dumps(returnobj)
    elif jdata['content'] == '응답':
        if plugin.req == 1:
            txt = "요청이 진행중 입니다."
        else:
            txt = plugin.ondisk_ret
        returnobj = {
            'message': {
                'text': txt
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "요청",
                    "응답",
                    "최초"
                ]}
        }

        return json.dumps(returnobj)
    elif jdata['content'] == "재시작":

        plugin.restart()
        returnobj = {
            'message': {
                'text': "재시작 하였습니다."
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "요청",

                    "최초"
                ]}

        }
        return json.dumps(returnobj)
    else:
        returnobj = {
            'message': {
                'text': "처음 화면 입니다."
            },
            "keyboard": {
                "type": "buttons",
                "buttons": [
                    "요청",

                    "최초","재시작"
                ]}

        }
        return json.dumps(returnobj)



if __name__ == '__main__':
    _thread.start_new_thread(reqcheck, ())
    # _thread.start_new_thread(flaskThread,(app,))

    app.run(host='0.0.0.0', port=80, threaded=True)
    while 1:
        pass