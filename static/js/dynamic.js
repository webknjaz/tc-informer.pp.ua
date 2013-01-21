_debug = true;

function debug(msg)
{
    if (_debug)
            console.log('[Debug]', msg);
}

function parseGetParams() {
    var $_GET={};
    var __GET=window.location.search.substring(1).split("&");
    for(var i=0;i<__GET.length;i++) {
        var getVar=__GET[i].split("=");
        $_GET[getVar[0]]=typeof(getVar[1])=="undefined"?"":getVar[1];
    }
    return $_GET;
}

function getVKheight() {
    // Size of VK frame equals to body size
    return $('body').height();
}

function getVKwidth() {
    // Size of VK frame equals to body size
    return $('body').width();
}

function getContentHeight() {
    // #wrap equals to all content size
    return $('#wrap').height();
}

function getFooterHeight() {
    // #footer equals to all content size
    return $('#footer').height();
}

function getRequiredHeight() {
    var h = getContentHeight();
    if (h > 5000)
        h = 5000;
    return h;
}

function resize_iframe(w, h) {
    VK.callMethod('resizeWindow', w, h);
}

$(function(){
    // Tip: m.b. it's better to use jquery.form
    $('#main_form').submit(function(event){
        $('.btn.btn-primary').css('after', '<img src="/img/ajax-loader.gif" alt="Loading..." title="Loading..." />');
        event.preventDefault();
        $('.alert .close').click(); // closing previous alert
        $.ajax({
           type: 'POST',   
           url: $(this).attr('action'),   
           data: $(this).serialize(),
        })
        .success(function(response){
            var alert = '';
            switch(response.status) {
                case 'ok':
                    debug('click ok');
                    debug($(this));
                    var tr = '<tr id="u_' + response.user.id + '"><td>' + response.user.id + '</td><td>' + response.user.name + '</td><td><a href="http://vk.com/id' + $('.form input[name="vk_link"]').val() + '" target="_blank">http://vk.com/id' + $('.form input[name="vk_link"]').val() + '</a></td><td class="pagination-centered" style="text-align: center;"><form action="/api/remove" method="post" class="form form-inline removal-form"><div class="controls row-fluid"><button type="submit" class="btn btn-danger"><i class="icon-remove"></i></button><input type="hidden" value="' + response.user.id + '" name="uid" ></div></form></td></tr>';
                    $('.table').append(tr);
                    var alert = '\
                    <div class="alert alert-success">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>\
                        <h4>Congrats!</h4>\
                        ' + response.msg + '\
                    </div>\
                    ';
                    $('#main_form').reset();
                    break;
                case 'fail':
                    debug('click fail');
                    var alert = '\
                    <div class="alert alert-error">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>\
                        <h4>Fail!</h4>\
                        ' + response.msg + '\
                    </div>\
                    ';
                    break;
                default:
                    debug('unknown fail');
                    var alert = '\
                    <div class="alert alert-error">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>\
                        <h4>Fail!</h4>\
                        User not added.\
                    </div>\
                    ';
                    break;
            }
            $(alert).prependTo('#main_form');
        })
        .fail(function(response){
            debug('click fail');
            var alert = '\
            <div class="alert alert-error">\
                <button type="button" class="close" data-dismiss="alert">&times;</button>\
                <h4>Fail!</h4>\
                User not added.\
            </div>\
            ';
            $(alert).prependTo('#main_form');
        })
        .always(function(){
            $('.btn.btn-primary').css('after', '');
        })
        ;
    });
    
    $('.form.removal-form').submit(function(event){
        event.preventDefault();
        $('.alert .close').click(); // closing previous alert
        $.ajax({
           type: 'POST',   
           url: $(this).attr('action'),   
           data: $(this).serialize(),
        })
        .success(function(response){
            var alert = '';
            switch(response.status) {
                case 'ok':
                    debug('click ok');
                    debug($(this));
                    $('.table tr#u_' + response.user_id).remove();
                    var alert = '\
                    <div class="alert alert-success">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>\
                        <h4>Congrats!</h4>\
                        ' + response.msg + '\
                    </div>\
                    ';
                    break;
                case 'fail':
                    debug('click fail');
                    var alert = '\
                    <div class="alert alert-error">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>\
                        <h4>Fail!</h4>\
                        ' + response.msg + '\
                    </div>\
                    ';
                    break;
                default:
                    debug('unknown fail');
                    var alert = '\
                    <div class="alert alert-error">\
                        <button type="button" class="close" data-dismiss="alert">&times;</button>\
                        <h4>Fail!</h4>\
                        User not removed.\
                    </div>\
                    ';
                    break;
            }
            console.log(alert);
            $(alert).prependTo('.table');
        })
        .fail(function(response){
            debug('click fail');
            var alert = '\
            <div class="alert alert-error">\
                <button type="button" class="close" data-dismiss="alert">&times;</button>\
                <h4>Fail!</h4>\
                User not removed.\
            </div>\
            ';
            $(alert).prependTo('.table');
        })
        ;
    });

    $_GET=parseGetParams();
    VK.init(function(){
        /*VK.api("getProfiles",{uid:$_GET['viewer_id']},function(data) {
            $("#main").prepend("Привіт, "+ data.response[0].first_name+"!");
        });*/

        $('#wrap').resize(function(obj,w,h) {
            debug('vk_height = ' + getVKheight() + ', height = ' + getRequiredHeight() + '.');
            if(getVKheight() == getRequiredHeight())
                return;
            resize_iframe(getVKwidth(), getRequiredHeight());
        });
        
        $('#wrap').resize();
    });
});