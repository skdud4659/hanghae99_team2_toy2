from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash
from datetime import timedelta
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbhanghae2

#메인
@app.route('/')
def home():
    return render_template('home.html')

#로그인
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

#로그아웃
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#회원가입
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

#about us
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

#크루 모집
@app.route('/makecrew')
def makecrew():
    return render_template('joincrew.html')

#크루 참가
@app.route('/joincrew')
def joincrew():
    return render_template('joincrew.html')

#shop
@app.route('/shop')
def shop():
    return render_template('shop.html')

#커뮤니티
@app.route('/community')
def community():
    return render_template('/community/community.html')

#커뮤니티 - 러닝
@app.route('/community&running')
def running():
    return render_template('/community/running.html')

#커뮤니티 - 클라이밍
@app.route('/community&climbing')
def climbing():
    return render_template('/community/climbing.html')

#커뮤니티 - 라이딩
@app.route('/community&riding')
def riding():
    return render_template('/community/riding.html')

#커뮤니티 - 등산
@app.route('/community&hiking')
def hiking():
    return render_template('/community/hiking.html')

#커뮤니티 - 글쓰기
@app.route('/community&write')
def write():
    return render_template('/community/write.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)