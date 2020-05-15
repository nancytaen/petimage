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
$('#postComment').submit(function(){
  event.preventDefault();
  const postID = $('#postID').val();
  $.post('/post/comment/' + postID, $(this).serialize(), function(data){
    console.log(data);
  })
});