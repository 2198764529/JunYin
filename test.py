from flask import Flask, url_for, request, render_template, redirect
from spider import Spider
from musics_list_spider import Music_list_spider as MS
from mysql_connect import Mysql_connect
import re

app = Flask(__name__)
mc = Mysql_connect()
# 页面的控制
@app.route("/", methods=["get", "post"])
def home():
    return render_template("index.html")


@app.route("/<type>", methods=["GET"])
def render(type):
    return render_template("%s.html"%type)


# json数据的传输
@app.route("/api/<type>", methods=["GET"])
def getJson(type):
    input = request.args.get("search_input")
    site_list = request.args.get("site_list").split(',')
    print(request.args)
    json = Spider().run(site_list,input, type)
    return json


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/api/loginRequest", methods=["POST"])
def loginRequest():
    try:
        data = request.form
        print(data)
        return {"is_correct": mc.is_correct(data), "is_has": mc.is_has(data)}
    finally:
        pass
        # mc.close()


@app.route("/api/registerRequest", methods=["POST"])
def registerRequest():
    try:
        data = request.form
        return {
            "is_has": True if mc.is_has(data) else mc.add(data),
            "is_legal": is_legal(data),
        }
    finally:
        pass


def is_legal(data):
    print(
        {
            "username": re.match("[^0-9]+?", data["username"]) != None,
            "passwd": re.match("[\S]{4,10}?", data["passwd"]) != None,
        }
    )
    return {
        "username": re.match(".{4,10}?", data["username"]) != None,
        "passwd": re.match("[\S]{4,10}?", data["passwd"]) != None,
    }


@app.route("/api/parseRequest", methods=["GET"])
def parse_music():
    print(request.args.get("song_id"))
    return MS().parse_music(request.args.get("site"), request.args.get("song_id"))


if __name__ == "__main__":

    app.run(debug=True)
