$('#account_form').submit(function(){
  event.preventDefault();
  console.log(123);
  alert(123);
  $.ajax({
    url: '/users/login',
    data: $(this).serialize(),
    type: "POST",
    success: function() {
    },
    error: function() {
    }
  });
  return false;
});

function getSignedRequest() {
  alert("here!");
  console.log("here!");
  return false;
}