/**
 * Created by French on 2/19/14.
 */

jQuery(document).ready(function($)
{
    $("#logo").click(function() {
        window.location = $(this).find("a").attr("href");
        return false;
    });
});

function deletepost(post_id){
    new ui.Confirmation({ title: 'Delete post', message: 'Are you sure?' })
        .ok('Remove')
        .overlay()
        .show(function(ok){
            if (ok) {
                //ui.dialog('Post deleted!').show().hide(2500);
                window.location.href = "/a/p/delete/"+post_id;
            }

        });
};