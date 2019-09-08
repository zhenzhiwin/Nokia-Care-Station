function waitforsmartcheck() {
    var loading = '<div id="loading"><img src="/static/images/timg.gif"></div>';
    $('body').append($(loading));

    setTimeout(function () {
        $('#loading').remove();
    }, 100000);
}