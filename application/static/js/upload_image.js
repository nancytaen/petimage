
// called when new image is uplaoded
$('#profile_img').change(function(){
  let uploadImg = $('#profile_img').prop('files')[0];
  console.log(uploadImg);
  if(uploadImg){
    getSignedRequest(uploadImg, "profile_pic");
  }
});


// obtain s3 signed request from server side
function getSignedRequest(file, postType){
  alert("YAY");
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
  })
}


$('#account_form').submit(function(){
  event.preventDefault();
  let uploadImg = $('#profile_img').prop('files');
  console.log(uploadImg);
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
