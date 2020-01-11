

let mvvm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],

  data: {
    json: {},

    show_flag: {
      'kuwo': {
        "source": true,
        "singer": true
      },
      "kugou": {
        "source": true,
        "singer": true
      },
      "qq": {
        "source": true,
        "singer": true
      },
      "netease": {
        "source": true,
        "singer": true
      }
    },
    page_urls: {
      "kuwo": {
        "link": "http://www.kuwo.cn/",
        "song": "http://www.kuwo.cn/play_detail/%S",
        "singer": "http://www.kuwo.cn/singer_detail/%S",
        "album": "http://www.kuwo.cn/album_detail/%S",
        "mv": "http://www.kuwo.cn/mvplay/%S",
        "s_logo": "../static/img/kuwo_logo_s.png",
      },
      "kugou": {
        "link": "https://www.kugou.com/",
        "song": "https://www.kugou.com/song/#hash=%S",
        "singer": "https://www.kugou.com/singer/%S.html",
        "album": "https://www.kugou.com/yy/album/single/%S.html",
        "mv": "https://www.kugou.com/mvweb/html/mv_%S.html",
        "s_logo": "../static/img/kugou_logo_s.png",
      },
      "qq": {
        "link": "https://y.qq.com/",
        "song": "https://y.qq.com/n/yqq/song/%S.html",
        "singer": "https://y.qq.com/n/yqq/singer/%S.html",
        "album": "https://y.qq.com/n/yqq/album/%S.html",
        "mv": "https://y.qq.com/n/yqq/mv/v/%S.html",
        "s_logo": "../static/img/qq_logo_s.png",
      },
      "netease": {
        "link": "https://music.163.com",
        "song": "https://music.163.com/#/song?id=%S",
        "singer": "https://music.163.com/#/artist?id=%S",
        "album": "https://music.163.com/#/album?id=%S",
        "mv": "https://y.qq.com/n/yqq/mv/v/%S.html",
        "s_logo": "../static/img/netease_logo_s.png",
      },
    },
    logo_urls: {
      "kuwo": "../static/img/kuwo_logo.png",
      "kugou": "../static/img/kugou_logo.png",
      "qq": "../static/img/qq_logo.png",
      "netease": "../static/img/netease_logo.png"
    },
    userData: {
      "login": {
        "username": "",
        "passwd": "",

      },
      "register": {
        "username": "",
        "passwd": "",
      },
    },
    is_login: false,
    is_playing: false,
    song_play_url: undefined,
    player: document.getElementById('music_player'),
    plays: [],
    playing_site: undefined,
    playing_song: undefined,

  },
  methods: {

    search: function () {
      // Ajax加载数据
      // console.log(this.Fsearch_type, this.Fsearch_input);
      if (nav.getQueryString("search_input").length == 0) {
        window.location = '/';
      } else {
        if(nav.getQueryString("site_list") == null)
        nav.setQueryString('site_list','kuwo');
        axios.get('/api/music'+location.search)
          .then(res => {
            this.json = res.data;
            console.log(res);
          })
          .catch(err => {
            console.error(err);
          })
      }


    },



    get_songurl: function (site, song_id) {
      axios.get("/api/parseRequest?" + "site=" + site + "&song_id=" + song_id)
        .then(res => {
          this.plays.set(song_id, res.data);

        })
        .catch(err => {
          console.error(err);
        });
    },
    get_singerDetail: function (site, singer_id) {
      singer_Detail_url = this.page_urls[site]["singer"].replace("%S", singer_id);
      window.open(singer_Detail_url, "_blank");
    },
    get_albumDetail: function (site, album_id) {
      album_Detail_url = this.page_urls[site]["album"].replace("%S", album_id);
      window.open(album_Detail_url, "_blank");
    },
    get_mvDetail: function (site, mv_id) {
      mv_Detail_url = this.page_urls[site]["mv"].replace("%S", mv_id);
      window.open(mv_Detail_url, "_blank");
    },
    // get_user: function (type) {
    //   return this.userData[type]['username']
    // },
    hasMV: function (song_mv) {
      return song_mv != ""
    },
    search_type: function () {
      return this.search_type == "search_movie"
    },
    Rcolor: function (site, type) {
      return type + this.colors[site]
    },
    loginRequest: function () {
      const params = new URLSearchParams();
      params.append("username", this.userData['login']["username"])
      params.append("passwd", this.userData['login']["passwd"])
      axios.post("/api/loginRequest", params)
        .then(res => {
          console.log(res);
          this.check(res.data, "login");
        })
        .catch(err => {
          console.error(err);
        })
    },
    check: function (flags, type) {
      if (type == "login") {
        if (flags['is_correct']) {
          console.log("用户名", this.userData[type]['username']);
          this.is_login = true;
          // document.getElementById("user_face").innerHTML = this.userData[type]['username'];
          // document.getElementById('user_login').style.display = 'none';
          // document.getElementById('user_face').style.display = 'inline';
          // document.getElementById('user_face').href = '/login?username=' + this.userData[type]['username'];
        } else {

          tip_info = flags['is_has'] ? "用户名或密码错误" : "用户未注册，请先注册";
          alert(tip_info);
        }
      } else {
        let is_legal = flags['is_legal']['username'] && flags['is_legal']['passwd'];
        if (!flags['is_has'] && is_legal) {
          alert("注册成功");
          this.is_login = true;

          // document.getElementById("user_face").innerHTML = this.userData[type]['username'];
          // document.getElementById('user_login').style.display = 'none';
          // document.getElementById('user_face').style.display = 'inline';
          // document.getElementById('user_face').href = '/login?username=' + this.userData[type]['username'];
        } else {
          tip_info = is_legal ? "账号已存在" : "格式错误";
          alert(tip_info);
        }
      }
    },
    registerRequest: function () {
      const params = new URLSearchParams();
      params.append("username", this.userData['register']["username"])
      params.append("passwd", this.userData['register']["passwd"])
      params.append("passwd", this.userData['register']["email"])
      axios.post('/api/registerRequest', params)
        .then(res => {
          console.log(res);
          this.check(res.data, "register");
        })
        .catch(err => {
          console.error(err);
        })
    },
    add_song: function (site, item) {
      axios.get("/api/parseRequest?" + "site=" + site + "&song_id=" + item.song_id)
        .then(res => {
          console.log(item);
          item.set("url", res.data);

          this.plays.push(item);
          this.play(item);
        })
        .catch(err => {
          console.error(err);
        });
      // console.log(this.get_songurl(site, song_id));
      // if (this.plays == {}) {
      //     this.plays[song_id] = this.song_play_url;

      //     this.playing_index = song_id;

      //     this.play(this.song_id);
      // } else {
      //     console.log('已添加');
      //     this.plays[song_id] = this.song_play_url;
      // }
    },
    play: function (song_map) {
      if (song_map == undefined) {
        console.log('没传歌曲信息,代表点击播放按钮');
        this.player.play();
        this.is_playing = true;
      } else {
        console.log("正在播放", song_map.url);
        this.player.src = song_map.url;
        this.playing_song = song_map;
        this.progress_compute(this.player);
        this.player.play();
        this.is_playing = true;
      }
    },
    pause: function () {
      this.played_time = Math.round(this.player.currentTime);
      this.player.pause();
      this.is_playing = false;
      // 当is_playing为true,is_playing==flase返回flase,为flase返回true
    },
    next: function () {
      let index = this.plays.indexOf(this.playing_song) + 1;
      if (index == this.plays.length)
        index = index - 1;
      let song_map = this.plays[index];
      this.play(song_map);
    },
    to_page: function (search_type) {
      return '/search?search_input=' + nav.getQueryString('search_input') + '&search_type=' + search_type;
    },

    played_time: function (player) {
      m = Math.floor(Math.round(player.currentTime) / 60);
      second = Math.round(player.currentTime) - m * 60;
      return m;

    },
    play_total_time: function (player) {
      return Math.round(player.duration) / 60;
    },
    progress_compute: function (player) {
      setInterval(function () {
        m = Math.floor(Math.round(player.currentTime) / 60);
        s = Math.round(player.currentTime) % 60;
        total_m = Math.floor(Math.round(player.duration) / 60);
        total_s = Math.round(player.duration) - Math.floor(Math.round(player.duration) / 60) * 60;
        play_total_time = total_m + ":" + total_s;
        played_time = m + ":" + s;
        document.getElementById("myprogress").style.width = Math.round(player.currentTime) * 100 / player.duration + "%";
        document.getElementById("play_time").innerText = played_time + "/" + play_total_time;
      }, 1000);
    },

  },
  mounted() {
    this.search();
  },
  computed: {
    user_image: function () {
      d = '../static/img/register/default.ico'
      u = '../static/img/register/man.png'
      r = this.is_login ? u : d
      console.log(r)
      return r
    },
    play_flag: function () {
      return this.is_playing;
    },
    get_play_url: function () {
      axios.get("/api/parseRequest?" + "site=" + this.playing_site + "&song_id=" + this.playing_index)
        .then(res => {
          this.song_play_url = res.data;

        })
        .catch(err => {
          console.error(err);
        });
    },
    auto_play: function () {
      if (this.player.ended) {
        this.next();
      }
    },

    // progress_compute: function () {
    //     if (this.playing_index != undefined) {

    //         setInterval(function () {
    //             console.log("正计算");
    //             document.getElementById("myprogress").style.width = Math.round(this.player.currentTime) / this.player.duration + "%";
    //         }, 1000);
    //     }
    // }




    //     user_image:{
    //     // getter
    //     get: function () {
    //         return this.name + ' ' + this.url
    //     },
    //     // setter
    //     set: function (newValue) {
    //         var names = newValue.split(' ')
    //         this.name = names[0]
    //         this.url = names[names.length - 1]
    //     }
    // }
  },


});