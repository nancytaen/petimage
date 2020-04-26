
// called when new image is uplaoded
$('#profile_img').change(function(){
  let uploadImg = $('#profile_img').prop('files')[0];
  console.log(uploadImg);
  if(uploadImg){
    getSignedRequest(uploadImg);
  }
});

// obtain s3 signed request from server side
function getSignedRequest(file){
  alert("YAY");
  $.ajax({
    url: '/sign_s3?file_name=' + file.name + "&file_type=" + file.type,
    type: 'GET',
    success: function(result) {
      let response = JSON.parse(result);
      uploadFile(file, response.data, response.url);
    }
  })
}

function uploadFile(file, s3Data, url){

  console.log(s3Data);
  var xhr = new XMLHttpRequest()
  xhr.open("POST", s3Data.url);

  let postData = new FormData();
  for (const key in s3Data.fields){
    postData.append(key, s3Data.fields[key]);
  }
  postData.append('file', file);

  xhr.onreadystatechange = function() {
    if(xhr.readyState === 4){
      if(xhr.status === 200 || xhr.status === 204){

       $('#preview').src = url;
       $('#profile_img_url').value = url;
      } else {
        alert("Could not uplaod file");
      }
    }
  };
  xhr.send(postData);

  // $.ajax({
  //   url: s3Data.url,
  //   type: 'POST',
  //   data: postData,
  //   success: function(){
  //      $('#preview').src = url;
  //      $('#profile_img_url').value = url;
  //      console.log("success");
  //   },
  //   failure: function(){
  //     console.log("fail");
  //   }
  // })
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
