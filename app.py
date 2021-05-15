from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbhanghae2

#메인
@app.route('/')
def home():
    return render_template('home.html')

#로그인
@app.route('/login')
def login():
    return render_template('login.html')

#회원가입
@app.route('/letin')
def letin():
    return render_template('letin.html')

#about us
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

#크루 모집
@app.route('/makecrew')
def makecrew():
    return render_template('makecrew.html')

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
    return render_template('community.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)