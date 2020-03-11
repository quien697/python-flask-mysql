# -*- coding: UTF-8 -*-
import flask
from flask import jsonify, request

import mysql.connector
from mysql.connector import errorcode

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
app.after_request(after_request)

#將 SQL Data 轉換成 Json 格式
def toJson(data):
    jsonData=[]
    for row in data:  
        result = {} 
        result['id'] = row[0]
        result['account'] = row[1]
        result['password'] = row[2]
        result['nickname'] = row[3]
        jsonData.append(result)
    return jsonData

#Select Data
def select_data(nickname):
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            database='testdb',
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            user='testuser',
            password='123456'
        )
        if cnx.is_connected():
            cur = cnx.cursor()
            query = "SELECT * FROM users"
            if nickname == "":
                cur.execute(query)
            else:
                query += " WHERE nickname = %s"
                val = (nickname,)
                cur.execute(query, val)
            data = cur.fetchall()     # fetchall() 获取所有记录
            return toJson(data)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return err
    else:
        cnx.close()

#Insert Data
def insert_data(account,password,nickname):
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            database='testdb',
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            user='testuser',
            password='123456'
        )
        cur = cnx.cursor()
        query = "INSERT INTO users (account, password, nickname) VALUES (%s, %s, %s)"
        val = (account, password, nickname)
        cur.execute(query, val)
        cnx.commit()
        return (cur.rowcount, "insert success")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return err
    else:
        cnx.close()

#Update Data
def updata_data(account,password,nickname):
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            database='testdb',
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            user='testuser',
            password='123456'
        )
        cur = cnx.cursor()
        query = "UPDATE users SET account = %s, password = %s WHERE nickname = %s"
        val = (account, password, nickname)
        cur.execute(query, val)
        cnx.commit()
        return (cur.rowcount, "update success")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return err
    else:
        cnx.close()

#Delete Data
def delete_data(nickname):
    try:
        cnx = mysql.connector.connect(
            host='127.0.0.1',
            database='testdb',
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            user='testuser',
            password='123456'
        )
        cur = cnx.cursor()
        query = "DELETE FROM users WHERE nickname = %s"
        val = (nickname,)
        cur.execute(query, val)
        cnx.commit()
        return (cur.rowcount, "delete success")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            return "Database does not exist"
        else:
            return err
    else:
        cnx.close()

# 首頁
@app.route("/", methods=['GET'])
def home():
    return "<h1>Python & Mysql</h1>"

# 顯示所有使用者
@app.route("/users", methods=['GET'])
def all_user():
    return jsonify(select_data(""))

# 顯示單一使用者
@app.route("/user", methods=['GET'])
def single_user():
    if 'nickname' in request.args:
        nickname = request.args['nickname']
    else:
        return "Error: No nickname provided. Please specify a nickname."

    return jsonify(select_data(nickname))

# 新增使用者
@app.route("/adduser", methods=['GET'])
def add_user():
    if 'account' in request.args:
        account = request.args['account']
    else:
        return "Error: No account provided. Please specify a account."

    if 'password' in request.args:
        password = request.args['password']
    else:
        return "Error: No password provided. Please specify a password."

    if 'nickname' in request.args:
        nickname = request.args['nickname']
    else:
        return "Error: No nickname provided. Please specify a nickname."

    return jsonify(insert_data(account,password,nickname))

# 更新使用者
@app.route("/edituser", methods=['GET'])
def edit_user():
    if 'account' in request.args:
        account = request.args['account']
    else:
        return "Error: No account provided. Please specify a account."

    if 'password' in request.args:
        password = request.args['password']
    else:
        return "Error: No password provided. Please specify a password."

    if 'nickname' in request.args:
        nickname = request.args['nickname']
    else:
        return "Error: No nickname provided. Please specify a nickname."

    return jsonify(updata_data(account,password,nickname))

# 刪除使用者
@app.route("/deleteuser", methods=['GET'])
def delete_user():
    if 'nickname' in request.args:
        nickname = request.args['nickname']
    else:
        return "Error: No nickname provided. Please specify a nickname."

    return jsonify(delete_data(nickname))

app.run()