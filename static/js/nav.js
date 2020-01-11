// function getQueryString(name) {
//   let patt = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
//   let result = decodeURI(location.search).substr(1).match(patt)
//   return result[2]
// }
// function check_


let nav = new Vue({
  // el: '#nav',
  // delimiters: ['[[', ']]'],

  data: {
    json: {},


    is_login: false,

    userData: {
      "login": {
        "username": "",
        "passwd": "",

      },
      "register": {
        "username": "",
        "passwd": "",
      },
    }
  },
  methods: {


    getQueryString: function (name) {
      let patt = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
      let result = decodeURI(location.search).substr(1).match(patt)
      return result == null ? null : result[2]
    },
    setQueryString: function (name,value) {
      let delimited = location.search.length==0?"?":"&";
      let param = delimited+name+"="+value;
      let result = this.getQueryString(name);
      if(result==null)
        location.href=location.href+param;
      else
        location.href= location.href.replace(delimited+name+"="+result,param);
    },

    // loginRequest: function () {
    //   const params = new URLSearchParams();
    //   params.append("username", this.userData['login']["username"])
    //   params.append("passwd", this.userData['login']["passwd"])
    //   axios.post("/api/loginRequest", params)
    //     .then(res => {
    //       console.log(res);
    //       this.check(res.data, "login");
    //     })
    //     .catch(err => {
    //       console.error(err);
    //     })
    // },
    // check: function (flags, type) {
    //   if (type == "login") {
    //     if (flags['is_correct']) {
    //       console.log("用户名", this.userData[type]['username']);
    //       this.is_login = true;
    //       // document.getElementById("user_face").innerHTML = this.userData[type]['username'];
    //       // document.getElementById('user_login').style.display = 'none';
    //       // document.getElementById('user_face').style.display = 'inline';
    //       // document.getElementById('user_face').href = '/login?username=' + this.userData[type]['username'];
    //     } else {

    //       tip_info = flags['is_has'] ? "用户名或密码错误" : "用户未注册，请先注册";
    //       alert(tip_info);
    //     }
    //   } else {
    //     let is_legal = flags['is_legal']['username'] && flags['is_legal']['passwd'];
    //     if (!flags['is_has'] && is_legal) {
    //       alert("注册成功");
    //       this.is_login = true;

    //       // document.getElementById("user_face").innerHTML = this.userData[type]['username'];
    //       // document.getElementById('user_login').style.display = 'none';
    //       // document.getElementById('user_face').style.display = 'inline';
    //       // document.getElementById('user_face').href = '/login?username=' + this.userData[type]['username'];
    //     } else {
    //       tip_info = is_legal ? "账号已存在" : "格式错误";
    //       alert(tip_info);
    //     }
    //   }
    // },
    // registerRequest: function () {
    //   const params = new URLSearchParams();
    //   params.append("username", this.userData['register']["username"])
    //   params.append("passwd", this.userData['register']["passwd"])
    //   params.append("passwd", this.userData['register']["email"])
    //   axios.post('/api/registerRequest', params)
    //     .then(res => {
    //       console.log(res);
    //       this.check(res.data, "register");
    //     })
    //     .catch(err => {
    //       console.error(err);
    //     })
    // },

  },
  mounted() {

  },
  computed: {
    // user_image: function () {
    //   d = '../static/img/register/default.ico'
    //   u = '../static/img/register/man.png'
    //   r = this.is_login ? u : d
    //   console.log(r)
    //   return r
    // },


  },


});