from urllib import request, parse
import sys, string, re


class Movie_list_spider:
    def __init__(self,):
        self.movie_urls = {
            "bilibili": "https://search.bilibili.com/all?from_source=banner_search&keyword=",
            "weibo": "https://s.weibo.com/video?xsort=hot&hasvideo=1&tw=video&Refer=index&q=",
            "acfun": "https://www.acfun.cn/search/#cid=0;sort=1;sid=0;query=",
            "zzzfun": "http://www.zzzfun.com/index.php/vod-search-wd-%S",
        }
        # self.movie_urls = {
        #     "tengxun": "https://v.qq.com/x/search/?q={}&stag=4&filter=duration%3D4%26tabid%3D1%%26resolution%3D0"
        # }

        self.parseData = [
            '<div class="wrapper">.*?<div class="site_footer">',
            '<a href="(https:.*?)".*?src="(.*?)".*?alt="(.*?)" />.*?"figure_info">(.*?)</span></span>.*?</a>',
            {
                "pic_url": 'src="(//puui.qpic.cn/.*?)"',
                "link_name": '<h2 class="result_title"><a href="(.*?)" target="_blank" _stat="video:poster_h_title">(.*?)</a>',
            },
        ]
        self.movieData = {"iqiyi": []}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0"
        }

    def get_html(self, interface, keyWord):
        print("正在获取:%s" % (interface + keyWord))
        url = parse.quote(interface + keyWord, safe=string.printable)
        response = request.urlopen(request.Request(url=url, headers=self.headers))
        return response.read().decode("utf-8")

    def get_movies(self, html, site_key):
        return_movies = []
        if site_key == "bilibili":
            up_playtime_list = re.findall(
                '<span class="so-imgTag_rb">(.*?)</span>', html
            )
            up_title_list = re.findall(
                '<a title="(.*?)" href="(.*?)" target="_blank" class="title">', html
            )
            up_date_list = re.findall(
                """<i class="icon-date"></i>
        (.*?)
      </span""",
                html,
            )
            up_name_list = re.findall(
                '<a href="(.*?)" target="_blank" class="up-name">(.*?)</a>', html
            )
            for i in range(0, len(up_date_list)):
                return_movies.append(
                    {
                        "up_playtime": up_playtime_list[i],
                        "up_title": {
                            "name": up_title_list[i][0],
                            "link": up_title_list[i][1],
                        },
                        "up_date": up_date_list[i],
                        "up_name": {
                            "name": up_name_list[i][1],
                            "link": up_name_list[i][0],
                        },
                    }
                )
        elif site_key == "5dm":
            return_movies = html
        # first = re.search(self.parseData[0], html)
        # print(self.parseData[1], type(self.parseData[1]))
        # second = re.finditer(self.parseData[1], first)
        # for li in second:
        #     pic_url = self.parseData[2]["pic_url"].search(li)
        #     movie_name = self.parseData[2]["movie_name"].search(li)
        #     self.movieData[site_key].append(
        #         {movie_name: {"name": movie_name, "pic_url": pic_url}}
        #     )
        return return_movies

    def run(self, site_list,word):
        html = self.get_html(self.movie_urls["weibo"], word)
        movie = self.get_movies(html, "5dm")
        return html

    # 以上测试
    # for key in self.movie_urls:
    #     html = self.get_html(self.movie_urls[key], word)
    #     movies = self.get_movies(html, key)

    # for music_url in self.music_urls:
    #     html = self.get_html(music_url[0], word)
    #     self.songs = self.get_songs(html, music_url[1])
    # html = self.get_html(self.movie_urls["tengxun"], word)
    # first = re.compile(self.parseData[0], re.S)
    # sk_mod_divs = first.search(html).group()
    # first = re.compile(self.parseData[0], re.S)
    # second = re.compile(self.parseData[1], re.S)
    # pic_url = re.compile(self.parseData[2]["pic_url"], re.S)
    # link_name = re.compile(self.parseData[2]["link_name"], re.S)
    # all = re.compile(self.parseData[1], re.S)
    # movie_name = re.compile(self.parseData[2]["movie_name"], re.S)
    # ul = first.search(html).group()
    # # data = self.get_movies(html, "iqiyi")
    # pic_urls = pic_url.findall(sk_mod_divs)
    # links_names = link_name.findall(sk_mod_divs)
    # alls = all.findall(sk_mod_divs)
    # movies_name = movie_name.findall(ul)
    # print(ul)
    # for x in alls:
    #     print({"link": x[0], "pic_url": x[1], "name": x[2], "playtime": x[3]})

    # return {
    #     "tengxun": [
    #         {"link": x[0], "pic_url": x[1], "name": x[2], "playtime": x[3]}
    #         for x in alls
    #     ]
    # }
