$(function(){
	$('#loading').hide()

	function codetoJSON(code){
		return JSON.stringify({'data': code});
	}

	function displayoutput(output){
		output = output['result'];
		imagemeta = 'data:image/png;base64,'
		// output is a key, value pair of filename: uuencoded content
		// output = JSON.stringify(output)
		// TODO: it loads the last generated image into the outputimage tag
		// that needs to be changed
		for (var key in output){
			image = output[key];
			console.log(output)
			image = imagemeta + image;
			console.log(image);
			$('#outputimage').attr('src', image);
		}
		$('#result').val("It works!");
	}

	$('#runcode').bind('click', function(){
		// debug
		console.log('detect click');
		
		$('#loading').show();
		code = $('#code').val();
		jcode = codetoJSON(code)
		// console.log(jcode);
		$.ajax({
		    type: 'POST',
		    // Provide correct Content-Type, so that Flask will know how to process it.
		    contentType: 'application/json',
		    // Encode your data as JSON.
		    data: jcode,
		    // This is the type of data you're expecting back from the server.
		    dataType: 'json',
		    url: '/runcode',
		    success: function (e) {
		    	$('#loading').hide();
		        displayoutput(e);
		    }
		});
	});

	$('.example').bind('click', function(){
		$('#loading').show();

		var example = $(this).html().toLowerCase();
		example = example.replace(' ', '_');

		var code_url = 'static/examples/plot_' + example + '.py';
		var example_image = 'static/images/plot_' + example + '.png';
		
		$.get(code_url, function(data){
			$('#code').val(data);

			$('#originalimage').attr('src', example_image).load(function(){
				$('#loading').hide();
			});
		});
	});	
});
