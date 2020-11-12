import requests
import hashlib
from flask import Flask, render_template, request

import json
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('passhtml.html')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        try:
            data = request.form["name"]
            ans = main(data, 0)
            # return render_template('thankyou.html')
            return ans
        except:
            return 'did not write to database '
    else:
        return "something is wrong "


# ****************************************************************************
def get_response_obj(find_str):
    url = 'https://api.pwnedpasswords.com/range/' + find_str
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError("url must be wrong , check conversion ")
    return res


def counting(response_obj, tail):
    response_obj = response_obj.text.splitlines()
    response_obj = (line.split(':') for line in response_obj)
    for to_match, count in response_obj:
        if to_match == tail:
            return count
    return 0


def convert_to_sha1(normal_pass):
    sha1_password = hashlib.sha1(normal_pass.encode('utf-8')).hexdigest().upper()
    find, tail = sha1_password[:5], sha1_password[5:]
    response_obj = get_response_obj(find)
    return counting(response_obj, tail)


def main(passwords, a):
    if (a):
        for password in passwords.readlines():
            password = password.strip()
            result = convert_to_sha1(password)
            if result:
                print(f' ❌  {password} has been found {result} times in breaches . BE CAREFUL!!!')
            else:
                print(f" ✅  Well Done . Safe password - {password} !!!")
    else:
        password = passwords.strip()
        result = convert_to_sha1(password)
        if result:
            return f' ❌  {password} has been found {result} times in breaches . BE CAREFUL!!!'
        else:
            return f" ✅  Well Done . Safe password - {password} !!!"

# if __name__ == '__main__':
#
#     password_data = open('password_file.txt', 'r')
#     main(password_data,1)
