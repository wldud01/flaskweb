from flask import Flask,jsonify, request , render_template
from yolo_detection_images import detectObjects
from dao import MyEmpDao
#from y_video import video_id


app = Flask(__name__)
#jsonify 결과를 json화 시킴

@app.route('/myapp/detectObjects') # web parameter path
def detect(): # image detect and print json
    img = request.args['image'] # arguments = image를 요청
    img_path = 'images/'+img
    results = detectObjects(img_path)
    return results
@app.route('/')
def main():
    return render_template('/main_page.html')

@app.route('/index')
def test():
    return render_template('/index.html')

#DB에서 json 형태로 값 가져오기 검색 결과 창
@app.route('/search_food', methods = ['GET', 'POST'])
def food_api():
    a = request.form.get("id_name")
    a = a.split(' ')
    print(a)
    search_food = MyEmpDao().getEmps(a)
    return render_template("result_page.html", search_food=search_food)

# youtube api
@app.route('/video', methods = ['GET', 'POST'])
def get_video():
    v_id = video_id()
    return render_template('recipe_video.html', v_id=v_id)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")