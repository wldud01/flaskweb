from flask import Flask,jsonify, request, render_template
from yolo_detection_images import detectObjects
from dao import MyEmpDao
import googletrans
#from y_video import video_id


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
    translator = googletrans.Translator()
    if results.isalpha(): # 영어로 인식된 경우 한글로 변경하는 googletrans api 사용
        results = translator.translate(results, dest='ko')
        results = results.text
    #a = request.form.get("id_name")
    print(results)
    a = results.split(' ')
    search_food = MyEmpDao().getEmps(a) # Database에서 음식 재료랑 이름 가져온 것
    param = results  # 인식된 재료 이름
    return render_template("result_page.html", search_food=search_food, result = param)

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
#    v_id = video_id() # youtube 불러오는 api가 연결된 spript
#    return render_template('recipe_video.html', v_id=v_id)
    return render_template('recipe_video.html', dish = dish)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")