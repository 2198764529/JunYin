// function getQueryString(name) {
//   let patt = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
//   let result = decodeURI(location.search).substr(1).match(patt)
//   return result[2]
// }
// function check_


let mvvm = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],

  data: {
    json: {},

  },
  methods: {

    search: function () {
      // Ajax加载数据
      // console.log(this.Fsearch_type, this.Fsearch_input);
      if (this.getQueryString("search_input").length == 0) {
        window.location = '/';
      } else {
        if(this.getQueryString("site_list") == null)
              this.setQueryString('site_list','kuwo');
        axios.get('/api/novel'+location.search)
          .then(res => {
            this.json = res.data;
            console.log(res);
          })
          .catch(err => {
            console.error(err);
          })
      }


    },
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


  },
  mounted() {
    this.search();
  },
  computed: {
  
 
  },


});