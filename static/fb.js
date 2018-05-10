

window.fbAsyncInit = function() {
    console.log('youpiii');
    FB.init({
        appId: '184032105530493',
        cookie: true,
        xfbml: true,
        version: 'v3.0'
    });
    console.log("fakt neviem preco")
    FB.AppEvents.logPageView();
    console.log("fakt neviem preco")
};

(function(d, s, id) {

    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = 'https://connect.facebook.net/en_GB/sdk.js#xfbml=1&version=v3.0&appId=184032105530493';
    fjs.parentNode.insertBefore(js, fjs);
    console.log('test');
}(document, 'script', 'facebook-jssdk'));


function checkLoginState() {
    console.log('test2');
    FB.getLoginStatus(function(response) {
        statusChangeCallback(response);
    });
}