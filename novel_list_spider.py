from urllib import request, parse
import sys, string, re


class Novel_list_spider:
    def __init__(self,):
        self.novel_urls = {
            "qidian": "https://www.qidian.com/search?kw=",
            "zongheng": "http://search.zongheng.com/s?keyword=",
            "17k": "https://search.17k.com/search.xhtml?c.st=0&book_status=0&word_count=0&sort=0&fuzzySearchType=1&book_free=1&c.q=",
        }
        # self.novel_urls = {
        #     "policy": "http://sousuo.gov.cn/s.htm?t=zhengce&q={}&sortType=1&searchfield=title",
        #     "policy_test": "http://sousuo.gov.cn/list.htm?n=100&t=paper&searchfield=title&title={}",
        # }

        self.parseData = [
            re.compile(
                '<ul class="middle_result_con show" index="(zhongyangfile|gongwen|otherfile)">(.*?)</ul>',
                re.S,
            ),
            re.compile(
                '<a href="(.*?)".*?>(.*?)<span class="date">&nbsp;&nbsp;(.*?)</span>',
                re.S,
            ),
            re.compile(
                '<td class="novel"><a href="(.*?)" target="_blank">(.*?)</a>.*?<td>(.*?)</td>.*?<td>(\d{4}年\d{2}月\d{2}日) </td>.*?<td>(\d{4}年\d{2}月\d{2}日) </td>',
                re.S,
                # '<tr style=.*?<td class="novel"><a href="(.*?)" target="_blank">(.*?)</a>.*?</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',
            ),
        ]

    def get_html(self, interface, keyWord):
        print("正在获取:" + (interface + keyWord))
        url = parse.quote(interface + keyWord, safe=string.printable)
        response = request.urlopen(url)
        return response.read().decode("utf-8")

    def get_novel(self, html, site_key):
        return_novel = []
        r_html_tab_pattern = re.compile("<.*?>")
        if site_key == "qidian":
            data_page = re.search(
                '<div id="result-list" data-l1="3">.*?(?=<div class="page-box cf" data-l1="3">)',
                html,
                re.S,
            ).group()

            imgUrl_list = re.findall('"(//bookcover.yuewen.com/qdbimg.*?)"', data_page)
            link_tittle_list = re.findall(
                '<h4><a href="(//book.qidian.com/novel/.*?)" .*?>(.*?)</a></h4>', html
            )
            intro_list = re.findall('<p class="intro">(.*?)</p>', data_page)
            link_author_link_type_label_list = re.findall(
                '<a.*?href="(//my.qidian.com/author/.*?)" target="_blank">(.*?)</a>.*?href="(//.*?)".*?>(.*?)</a>.*?<span>(.*?)</span>',
                data_page,
            )
            words_sugs_list = re.findall(
                """<p><span> (.*?)</span>总字数</p>.*?<p><span> (.*?)</span>总推荐</p>""",
                data_page,
            )
            ulink_utitle_utime_list = re.findall(
                '<p class="update"><a href="/(.*?)".*?>(.*?)</a>.*?<span>(.*?)</span>',
                data_page,
            )
            data_len = len(imgUrl_list)

            for i in range(0, data_len):
                return_novel.append(
                    {
                        "words": words_sugs_list[i][0],
                        "intro": r_html_tab_pattern.sub("", intro_list[i]),
                        "imgUrl": imgUrl_list[i],
                        "link": link_tittle_list[i][0],
                        "title": r_html_tab_pattern.sub("", link_tittle_list[i][1]),
                        "type": link_author_link_type_label_list[i][3],
                        "type_link": link_author_link_type_label_list[i][2],
                        "author_name": link_author_link_type_label_list[i][1],
                        "author_link": link_author_link_type_label_list[i][0],
                        "update_time": ulink_utitle_utime_list[i][2],
                        "update_title": ulink_utitle_utime_list[i][1],
                        "update_link": ulink_utitle_utime_list[i][0],
                    }
                )
            print(return_novel)
        elif site_key == "zongheng":
            data_page = re.search(
                '<div class="search-tab">.*?(?=<div class="h20-blank"></div>)',
                html,
                re.S,
            ).group()
            imgUrl_list = re.findall('src="(.*?)"', data_page)
            link_tittle_list = re.findall(
                '<h2 class="tit"><a href="(.*?)" .*?>(.*?)</a></h2>', data_page
            )
            '.*?href="(.*?).html".*?>(.*?)</a>.*?href="(.*?).html".*?>(.*?)</a>([./s]*?)'
            link_author_type_link_lable_words_list = re.findall(
                '<div class="booknovel">.*?href="(.*?).html".*?>(.*?)</a>.*?href="(.*?).html".*?>(.*?)</a>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?</div>',
                data_page,
                re.S,
            )
            intro_list = re.findall(
                '<p>(.*?)</p>.*?<div class="key-word">关键词：(.*?)\r', data_page, re.S
            )
            r_html_tab_pattern = re.compile("<.*?>")
            data_len = len(imgUrl_list)
            for i in range(0, data_len):
                return_novel.append(
                    {
                        "words": link_author_type_link_lable_words_list[i][5],
                        "intro": intro_list[i][0],
                        "imgUrl": imgUrl_list[i],
                        "link": link_tittle_list[i][0],
                        "type": link_author_type_link_lable_words_list[i][2],
                        "type_link": link_author_type_link_lable_words_list[i][3],
                        "title": r_html_tab_pattern.sub("", link_tittle_list[i][1]),
                        "author_name": link_author_type_link_lable_words_list[i][1],
                        "author_link": link_author_type_link_lable_words_list[i][0],
                        "lable_list": intro_list[i][1].split(" "),
                    }
                )
            print(return_novel)
        elif site_key == "17k":
            data_page = re.search(
                '<div class="textlist">.*?(?=<div class="page">)', html, re.S
            ).group()
            link_imgUrl_title_list = re.findall(
                '<a href="(//.*?)".*?src="(https://cdn.static.17k.com/book/.*?)" alt="(.*?)"',
                data_page,
                re.S,
            )

            # '.*?href="(.*?).html".*?>(.*?)</a>.*?href="(.*?).html".*?>(.*?)</a>([./s]*?)'
            link_author_list = re.findall(
                """<span class="ls">作者：\n                                    <a href="(//.*?)" target="_blank">
                                        (.*?)
                                    </a>""",
                data_page,
                re.S,
            )
            lable_list = re.findall("<strong>标签：(.*?)</p>", data_page, re.S)
            intro_list = re.findall(
                "<li><strong>简介：.*? <a.*?>(.*?)</a>", data_page, re.S
            )
            update_words_list = re.findall("<code>(.*?)</code>", data_page, re.S)
            data_len = len(intro_list)
            lables_to_lable_pattern = re.compile('title="(.*?)"', re.S)
            for i in range(0, data_len):
                return_novel.append(
                    {
                        "update": update_words_list[i],
                        "words": update_words_list[i + 1],
                        "intro": intro_list[i],
                        "imgUrl": link_imgUrl_title_list[i][1],
                        "link": "https://" + link_imgUrl_title_list[i][0],
                        "title": link_imgUrl_title_list[i][2],
                        "author_name": link_author_list[i][1],
                        "author_link": link_author_list[i][0],
                        "lable_list": lables_to_lable_pattern.findall(lable_list[i]),
                    }
                )
        return return_novel

    def run(self,site_list, word):
        novel = {}
        for key in self.novel_urls:
            html = self.get_html(self.novel_urls[key], word)
            novel[key] = self.get_novel(html, key)
        return novel

    # html = self.get_html(self.novel_urls["policy"], word)
    # ul_list = self.parseData[0].findall(html)[0:3]
    # all_dict = {}
    # # print(ul_list)
    # for ul in ul_list:
    #     all_dict[ul[0]] = []
    #     for x in self.parseData[1].findall(ul[1]):
    #         all_dict[ul[0]].append({"link": x[0], "name":更新时间： 2019-07-26 10:17:41


#  x[1], "date": x[2]})

# htm = self.get_html(self.novel_urls["policy_test"], word)
# novel_list = [
#     {
#         "name": x[1],
#         "link": x[0],
#         "promulgator": x[2],
#         "w_date": x[3],
#         "release_date": x[4],
#     }
#     for x in self.parseData[2].findall(htm)
# ]
# novel_dic = {}/';./'';;

# return {"policy": novel_list}

