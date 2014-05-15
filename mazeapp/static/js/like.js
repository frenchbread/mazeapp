function like(post_id){
    $.get('/a/like/'+post_id, function(data) {

        $("#this_p"+post_id).html('<a href="javascript:void(0);" class="link" onclick="unlike('+post_id+')">Liked</a>');

        setTimeout(function(){
            ui.notify(data)
                .effect('slide');
        });

    });
    return false
}

function unlike(post_id){
    $.get('/a/unlike/'+post_id, function(data) {

        $("#this_p"+post_id).html('<a href="javascript:void(0);" class="link" onclick="like('+post_id+')">Like</a>');

        setTimeout(function(){
            ui.notify(data)
                .effect('slide');
        });

    });
    return false
}