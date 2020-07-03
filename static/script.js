// Script File

function showImage(fileInput) {
	if(fileInput.files && fileInput.files[0]) {

		$("#result").empty();
		$("#img").css('display', 'block');
		var reader = new FileReader();

		reader.onload = (e) => {
			$("#img").attr("src", e.target.result)
			$("span.file-name")[0].innerHTML = fileInput.files[0].name
		};

		reader.readAsDataURL(fileInput.files[0]);
	}

}

function sendFormData() {
	var formData = new FormData($('#form')[0]);

	$.ajax({
		type: 'POST',
		url: '/classify',
		data: formData,
		contentType: false,
		cache: false,
		processData: false,
		success: function(data) {
			$("#result").empty();
			for(var i=0; i<data.length; i++) {
				$("#result").append("<li class='subtitle is-4'>" + data[i]["name"] + " : " + data[i]["prob"] + "% </li>")
			}
			console.log('Success!');
		},
		error: function(data) {
			alert(data.responseText);
		}
	})

}

$(document).ready(function() {

	$.ajax({
		type: 'GET',
		url: '/food_classes',
		success: function(data) {
			$("#food_list").empty();
			for(var i=0; i<data.length; i++)
				$("#food_list").append("<li>"+data[i]+"</li>")
		}
	});
	
	$("#file").change(function() {
		showImage(this);
	});

	$("#predict").on('click', sendFormData);
});