function showImage(fileInput) {
	if(fileInput.files && fileInput.files[0]) {
		$("#img").css('display', 'block');
		var reader = new FileReader();

		reader.onload = (e) => $("#img").attr("src", e.target.result);

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
				$("#result").append("<p>" + data[i]["name"] + " : " + data[i]["prob"] + "%")
			}
			console.log('Success!');
		}
	})

}

$(document).ready(function() {
	$("#file").change(function() {
		showImage(this);
	});

	$("#predict").on('click', sendFormData);
});