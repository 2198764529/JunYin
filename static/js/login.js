function getQueryString(name) {
    let patt = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
    let result = decodeURI(location.search).substr(1).match(patt)
    return result[2]
}
let mvvm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
    },
    mounted() {
        document.getElementById('username').innerHTML = "dear " + getQueryString('username')
    },});