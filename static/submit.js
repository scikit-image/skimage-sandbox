$(function(){
	$('#loading').hide()

	function codetoJSON(code){
		return JSON.stringify({'data': code});
	}

	function displayoutput(output){
		output = output['result'];
		$('#result').val(output);
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
});
