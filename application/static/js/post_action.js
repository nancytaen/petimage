// like post and toggle button, change number
function LikePost(post_id){
  $.get('/post/like/' + post_id, function(data){
    if (data.status === 0){
      const button = $('#LikeButton' + post_id);
      const num = $('#NumLikes' + post_id);
      if (button.hasClass("btn-danger")){
        num.html(parseInt(num.html(), 10) - 1);
      } else {
        num.html(parseInt(num.html(), 10) + 1);
      }
      button.toggleClass("btn-danger btn-outline-danger");
    }
  })
}


//comment
$('.postComment').submit(function(){
  event.preventDefault();
  const postID = $('#postID').val();
  console.log($(this).serialize());
  console.log(postID);
  $.post('/post/comment/' + postID, $(this).serialize(), function(data){
    if (data.status === 0){
      $('#commentGroup' + postID).append('<div class="row">\n' +
        '                    <div class="col-sm-3 align-left"> ' + data.username + ' </div>\n' +
        '                    <div class="col-sm-9 align-left"> ' + data.comment + ' </div>\n' +
        '                </div>');
      const num = $('#NumComments' + postID);
      num.html(parseInt(num.html(), 10) + 1);
    }
  })
});