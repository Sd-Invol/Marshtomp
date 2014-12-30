	var get_image = function(){
		var im = document.getElementById("image");
		var src = document.getElementById("imgurl");
		im.src = src.value;
		return false;
	}
