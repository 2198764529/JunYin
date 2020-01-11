from urllib import request, parse
from musics_list_spider import Music_list_spider
from movie_list_spider import Movie_list_spider 
from novel_list_spider import Novel_list_spider 


class Spider:
    def run(self, site_list,search_input, search_type):
            if (search_type == "music") :
                result = Music_list_spider().run(site_list,search_input)
            elif(search_type == "novel"):
               result = Novel_list_spider().run(site_list,search_input)
            else:
                
                result = Movie_spider.run(site_list,search_input)
            return result

