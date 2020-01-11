from urllib import request, parse
import sys, string, json
import time
import random


class Music_list_spider:
    def __init__(self,):
        self.music_urls = {
 "kuwo":"http://search.kuwo.cn/r.s?&ft=music&client=kt&pn=0&rn=10&rformat=json&encoding=utf8&all=",
                 "qq":"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?w=",
                   "kugou":"https://songsearch.kugou.com/song_search_v2?keyword=",
           "netease": "http://s.music.163.com/search/get/?type=1&limit=50&s=", 
        }
            
               

           
            
        # 酷我音乐、酷狗音乐、QQ音乐
        self.parse_api = {
            "qq":
            # """https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey520477223795351&g_tk=5381&loginUin=2198764529&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":%s,"calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"%s","songmid":["%s"],"songtype":[0],"uin":"2198764529","loginflag":1,"platform":"20"}},"comm":{"uin":2198764529,"format":"json","ct":24,"cv":0}}"""
            """https://u.y.qq.com/cgi-bin/musicu.fcg?loginUin=2198764529&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"4120984088","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"4120984088","songmid":["%s"],"songtype":[0],"uin":"2198764529","loginflag":1,"platform":"20"}},"comm":{"uin":2198764529,"format":"json","ct":24,"cv":0}}""",
            "kuwo": "http://www.kuwo.cn/url?format=mp3&type=convert_url3&reqId=278d1601-0076-11ea-bdcd-8bbb5d687ef1&rid=%s",
            "kugou": "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash=%s&mid=c118cea6de6705e5b2cc0d89fbb9c526",
            "netease": "http://tongzan.com/music/api.php",
        }

    def get_html(self, interface, keyWord):
        print("正在获取:" + interface + keyWord)
        url = parse.quote(interface + keyWord, safe=string.printable)
        response = request.urlopen(url)
        return response.read().decode("utf-8")

    def get_songs(self, html, site_key):
        return_json = []
        music_json = (
            (
                json.loads(html.replace("'", '"').replace("&nbsp;", " "))
                if site_key == "kuwo"
                else json.loads(html.replace("&nbsp;", " "))
            )
            if site_key != "qq"
            else json.loads(html[9:-1])
        )
        if site_key == "kuwo":
            kuwo_music_list = music_json["abslist"]
            for music in kuwo_music_list:
                return_json.append(
                    {
                        "song": music["NAME"],
                        "singer": music["ARTIST"],
                        "song_id": music["MP3RID"][4:],
                        "singer_id": music["ARTISTID"],
                        "album": music["ALBUM"],
                        "album_id": music["ALBUMID"],
                        "album_pic": "/static/img/kuwo_logo_s.png",
                        "song_mv": "",
                    }
                )
        # 酷我音乐
        elif site_key == "kugou":
            kugou_music_list = music_json["data"]["lists"]
            for music in kugou_music_list:
                songs_name = music["SongName"]
                singer = music["SingerName"]
                song_id = music["FileHash"]
                singer_id = music["SingerId"][0]
                album = music["AlbumName"]
                album_id = music["AlbumID"]
                url = (
                    "https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash=%s&mid=c118cea6de6705e5b2cc0d89fbb9c526"
                    % song_id
                )
                detail = json.loads(request.urlopen(url).read().decode("utf-8"))

                album_pic = (
                    "../static/img/kugou_logo2_small.png"
                    if "img" not in detail["data"]
                    else detail["data"]["img"]
                )
                song_mv = detail["data"]["video_id"]
                return_json.append(
                    {
                        "song": songs_name,
                        "singer": singer,
                        "song_id": song_id,
                        "singer_id": singer_id,
                        "album": album,
                        "album_id": album_id,
                        "album_pic": album_pic,
                        "song_mv": song_mv,
                    }
                )
        # 酷狗音乐
        elif site_key == "qq":
            pic_url = "https://y.gtimg.cn/music/photo_new/T002R300x300M000%s.jpg?max_age=2592000"
            qq_music_list = music_json["data"]["song"]["list"]
            for music in qq_music_list:
                if "media_mid" not in music.keys():
                    break
                songs_name = music["songname"]
                singer = music["singer"][0]["name"]
                song_id = music["media_mid"]
                singer_id = music["singer"][0]["mid"]
                album = music["albumname"]
                album_id = music["albummid"]
                album_pic = (
                    "../static/img/qq_logo_small.ico"
                    if "albummid" not in music or len(music["albummid"]) != 14
                    else pic_url % music["albummid"]
                )

                song_mv = music["vid"]
                return_json.append(
                    {
                        "song": songs_name,
                        "singer": singer,
                        "song_id": song_id,
                        "singer_id": singer_id,
                        "album": album,
                        "album_id": album_id,
                        "album_pic": album_pic,
                        "song_mv": song_mv,
                    }
                )
        # 网易云音乐
        elif site_key == "netease":
            netease_music_json = music_json["result"]["songs"]
            for music in netease_music_json:
                t = {
                    "song": music["name"],
                    "singer": music["artists"][0]["name"],
                    "song_id": music["id"],
                    "singer_id": music["artists"][0]["id"],
                    "album": music["album"]["name"],
                    "album_id": music["album"]["id"],
                    "album_pic": music["album"]["picUrl"],
                    "song_mv": "",
                }
                return_json.append(t)
        return return_json

    def parse_music(self, site, song_id):
        base_url = (
            self.parse_api[site]
            if site == "netease"
            else self.parse_api[site] % song_id
        )
        if site == "netease":
            data = parse.urlencode(
                {"types": "url", "id": song_id, "source": "netease"}
            ).encode("utf-8")
            req = request.Request(url=base_url, data=data)
            music_url = json.loads(request.urlopen(req).read())["url"]

        elif site == "kugou":
            music_url = json.loads(request.urlopen(base_url).read())["data"]["play_url"]
        elif site == "qq":

            # print(vkey_url)
            print(base_url)
            print(json.loads(request.urlopen(base_url).read()))
            urlinfo = json.loads(request.urlopen(base_url).read())["req_0"]["data"][
                "midurlinfo"
            ]
            
            if urlinfo == []:
                return ""
            vkey = urlinfo[0]["purl"]
            # url = self.parse_api[site]["api"] % (song_id, guid, vkey)
            music_url = "http://aqqmusic.tc.qq.com/amobile.music.tc.qq.com/%s" % vkey
        else:
            music_url = json.loads(request.urlopen(base_url).read())["url"]
        return music_url

    def run(self, site_list,word):
        result = {}
        print(type(site_list),site_list)
        for site in site_list:
            html = self.get_html(self.music_urls[site], word)
            result[site] = self.get_songs(html, site)

        return result

    # if __name__ == "__main__":
    #     songs = run(music_urls, word)
    #     for key in songs:
    #         print(key, songs[key], end="\n\n")
