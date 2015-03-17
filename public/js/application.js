$(document).ready(function(){
	image_search();
});

//-------------------------------

function image_search(){
	$.ajax({
		url: '/images',
		success: function(data){
			data = $.parseJSON(data);
			load_images(data);
			$("#word").html(decodeURIComponent(data[0]));
		},
		complete: function(){

		}
	});
}

function load_images(json_data){
	len = json_data.length;
	for (var i = 1; i < len; i ++){
		$("#" + i.toString()).attr("src", json_data[i]);
	}
}

//--------------------------------