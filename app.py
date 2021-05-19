from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash
from datetime import timedelta
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbhanghae2


# 메인
@app.route('/')
def home():
    return render_template('home.html')


# 로그인
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        userid = request.form['userid']
        userpw = request.form['userpw']
        users = db.members.find_one({'user_id': userid, 'user_pw': userpw})
        if users is None:
            flash("아이디와 비밀번호를 확인해주세요.")
            return redirect('login')
        else:
            session['user'] = userid
            return redirect('/')
        return redirect('/login')


# 로그아웃
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# 회원가입
app.config["SECRET_KEY"] = "hanghaeeeeee"


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('letin.html')
    else:
        username = request.form['username']
        userid = request.form['userid']
        userpw = request.form['userpw']
        re_pw = request.form['re_pw']

        doc = {'user_name': username, 'user_id': userid, 'user_pw': userpw, 'user_repw': re_pw}

        if username == '' or userid == '' or userpw == '' or re_pw == '':
            flash('입력되지 않은 값이 있습니다.')
            return render_template('letin.html')
        if userpw != re_pw:
            flash('비밀번호를 확인해주세요.')
            return render_template('letin.html')
        else:
            db.members.insert_one(doc)
            flash('회원가입 완료, 로그인을 해주세요.')
            return redirect('/login')


# about us
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


# 크루 모집
@app.route('/makecrew')
def makecrew():
    return render_template('makecrew.html')

#크루모집(POST)API
@app.route('/crew', methods=['POST'])
def save_crew():
    exercise_receive = request.form['exercise_give']
    place_receive = request.form['place_give']
    time_receive = request.form['time_give']
    people_receive = request.form['people_give']

    doc = {
        'exercise' : exercise_receive,
        'place' : place_receive,
        'time' : time_receive,
        'people' : people_receive
    }
    db.crew.insert_one(doc)

    return jsonify({'msg': '크루가 생성되었습니다!'})

#크루목록보기(GET)API
@app.route('/crew', methods=['GET'])
def view_crew():
    crew = list(db.crew.find({}, {'_id': False}))
    return jsonify({'crew': crew})

# 크루 참가
@app.route('/joincrew')
def joincrew():
    return render_template('makecrew.html')


# shop
@app.route('/shop')
def shop():
    return render_template('shop.html')

# 커뮤니티
@app.route('/community')
def community():
    return render_template('/community/community.html')

# 커뮤니티 - 글쓰기
@app.route('/community&write')
def write():
    return render_template('/community/write.html')

@app.route('/community&write&get', methods=["GET", "POST"])
def posting():
    if request.method == "POST":
        tag_receive = request.form['tag_give']
        title_receive = request.form['title_give']
        cmt_receive = request.form['cmt_give']

        doc = {
            'tag': tag_receive,
            'title': title_receive,
            'cmt': cmt_receive,
        }
        db.post.insert_one(doc)

        return jsonify({'msg': '작성이 완료되었습니다.'})

    elif request.method =='GET':
        posts = list(db.post.find({}, {'_id': False}))
        return jsonify({'all_posts': posts})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
