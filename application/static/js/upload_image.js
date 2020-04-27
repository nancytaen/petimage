
// called when new image is uplaoded
$('#profile_img').change(function(){
  let uploadImg = $('#profile_img').prop('files')[0];
  readURL(uploadImg);
});


// obtain s3 signed request from server side
function getSignedRequest(file, postType){
  $.ajax({
    url: '/sign_s3/' + postType + '?file_name=' + file.name + "&file_type=" + file.type,
    type: 'GET',
    success: function(result) {
      let response = JSON.parse(result);
      uploadFile(file, response.data, response.url);
    }
  })
}

// upload file to s3
function uploadFile(file, s3Data, url){

  let postData = new FormData();
  for (const key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  $.ajax({
    url: s3Data.url,
    type: 'POST',
    data: postData,
    processData: false,
    contentType: false,
    success: function(){
       $('#preview').attr("src", url);
       $('#profile_img_url').val(url);
       console.log("success");
    },
    failure: function(){
      console.log("fail");
    }
  }).done(function(){
      $.ajax({
        url: '/user/account',
        data: $("#account_form").serialize(),
        type: "POST",
        success: function() {
        },
        error: function() {
        }
      });
  });
}


$('#account_form').submit(function(){
  event.preventDefault();

  // upload image to s3 if applicable
  let uploadImg = $('#profile_img').prop('files')[0];
  if(uploadImg){
    getSignedRequest(uploadImg, "profile_pic");
  }
  $.ajax({
    url: '/user/account',
    data: $(this).serialize(),
    type: "POST",
    success: function() {
    },
    error: function() {
    }
  });
  return false;
});


// preview an image
function readURL(img) {
  if (img) {
    let reader = new FileReader();
    reader.onload = function(e) {
      $("#preview").attr('src', e.target.result);
    };
    reader.readAsDataURL(img);
  }
}
