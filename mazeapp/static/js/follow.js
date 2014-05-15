/**
 * Created by French on 4/24/14.
 */

function follow(user_id){
    $.get('/u/follow/'+user_id, function(data) {
        $("#followThatShit").html('<a href="javascript:void(0);" class="link" onclick="unfollow('+user_id+')">Unfollow</a>');
        $("#this_f"+user_id).html('<a href="javascript:void(0);" class="link" onclick="unfollow('+user_id+')">Unfollow</a>');
        setTimeout(function(){
            ui.notify(data)
                .effect('slide');
        });

    });
    return false
}

function unfollow(user_id){
    $.get('/u/unfollow/'+user_id, function(data) {
        $("#followThatShit").html('<a href="javascript:void(0);" class="link" onclick="follow('+user_id+')">Follow</a>');
        $("#this_f"+user_id).html('<a href="javascript:void(0);" class="link" onclick="follow('+user_id+')">follow</a>');
        setTimeout(function(){
            ui.notify(data)
                .effect('slide');
        });
    });
    return false
}
