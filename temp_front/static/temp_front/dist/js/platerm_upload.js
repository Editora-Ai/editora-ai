var btnUpload = $("#upload_file"),
		btnOuter = $(".button_outer");
	btnUpload.on("change", function(e){
		var ext = btnUpload.val().split('.').pop().toLowerCase();
		if($.inArray(ext, ['gif','png','jpg','jpeg']) == -1) {
			$(".error_msg").text("Not an Image...");
		} else {
		// Multiple file upload
		var form = $('#form_upload')[0];
		var data = new FormData(form);

		var action = function(d) {
			setTimeout(function(){
				window.location.replace("/dashboard/tasks")
			},1000);
		};
		$.ajax({
			xhr: function() {
				var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
						var percentComplete = evt.loaded / evt.total;
						$('.progress').prop('hidden', false);
						$('.progress-bar').width(percentComplete *100+'%');
						$('.progress-bar').html("Uploading files " +(percentComplete *100).toFixed(0)+'%');                    }
                }, false);
                return xhr;
            },
			url: '/api/v1/pr/',
			data: data,
			type: "POST",
			cache: false,
			contentType: false,
			processData: false,
            success: action,
			error: action,
		});
		$(".error_msg").text("");
		btnOuter.addClass("file_uploading");
		var uploadedFile = URL.createObjectURL(e.target.files[0]);
		}

	});
	$(".file_remove").on("click", function(e){
		$("#uploaded_view").removeClass("show");
		$("#uploaded_view").find("img").remove();
		btnOuter.removeClass("file_uploading");
		btnOuter.removeClass("file_uploaded");
	});