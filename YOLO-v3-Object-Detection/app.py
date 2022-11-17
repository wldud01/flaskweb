from flask import Flask,jsonify, request, render_template
from yolo_detection_images import detectObjects
from dao import MyEmpDao
import dao
import googletrans
from y_video import video_id
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import re


app = Flask(__name__)
#jsonify 결과를 json화 시킴
@app.route('/')
def main():
    return render_template('/main_page.html')

@app.route('/about')
def about():
    return render_template('/about.html')

@app.route('/index')
def test():
    return render_template('/index.html')

#DB에서 json 형태로 값 가져오기 검색 결과 창
@app.route('/search_food', methods = ['GET', 'POST'])
def food_api():
    img = request.files['id_name']  # file name 으로 읽어오기
    file = img.read()  # 파일 읽고 return type byte
    print(type(file))
    # img_path = 'images/' + img
    results = detectObjects(file)
    print(results)
    a = results.split(' ')
    translator = googletrans.Translator()
    print(a)
    ttt = ""
    for i in range(0, len(a)):
        print(type(a[i]))
        if a[i].isalpha() and i > 0: # 영어로 인식된 경우 한글로 변경하는 googletrans api 사용
            results = translator.translate(a[i], dest='ko')
            ttt = results.text + ' ' + ttt
            print(ttt+'1')
        elif a[i].isalpha() and i <= 0:  # 영어로 인식된 경우 한글로 변경하는 googletrans api 사용
            results = translator.translate(a[i], dest='ko')
            ttt = results.text
            print(ttt + '2')
        elif a[i].isalpha() is False and i <= 0:
            ttt = results.text
            print(ttt + '3')
        else:
            ttt = results.text + ' ' + ttt
            print(ttt + '4')
    print(ttt)
    a = ttt
    b = a.split(' ')
    search_food = MyEmpDao().getEmps(b) # Database에서 음식 재료랑 이름 가져온 것
     # DB 재료 가져오기

    param = a  # 인식된 재료 이름
    return render_template("result_page.html", search_food=search_food,result = param)

@app.route('/myapp/detectObjects', methods = ['GET', 'POST'])
def detect():
    img = request.files['id_name'] # file name 으로 읽어오기
    file = img.read() #파일 읽고 return type byte
    print(type(file))
    #img_path = 'images/' + img
    results = detectObjects(file)
    return jsonify(results)

# 이미지 파일로 넘겨서 받고 바로 함수에 넣은 다음에 인식하고 나면 라벨을 list 형식으로 나오게 하지 말고 ,로 이음
# split 함수를 이용해서 split 하고 search food 하면 될듯.. 그래서 파일을 어떻게 전송하지...


# youtube api
@app.route('/recipe_video', methods = ['GET', 'POST'])
def get_video():
    dish = request.form['food']
    DEVELOPER_KEY = 'AIzaSyAUyicTAp0THvJ51GgdJ2rX1ae9x1uDjkw'  # youtube api
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    print(type(dish))
      # app.py food_api 함수의 변수 사용하기
    # q = keyword 여기 부분에 음식 키워드 넣기
    search_response = youtube.search().list(
        #q=request.form['food'] +'만개의 레시피',
        q= dish +'만개의 레시피',
        order='relevance',
        part='snippet',
        maxResults=5
    ).execute()
    v_id = video_id(search_response) # youtube 불러오는 api가 연결된 spript
    #return render_template('recipe_video.html', v_id=v_id)
    return render_template('recipe_video.html', dish = dish, v_id=v_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")