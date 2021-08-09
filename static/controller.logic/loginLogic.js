const inputs = document.querySelectorAll(".input");

function blur_background(){
	document.getElementById("blur-create").style.display="block";
}

function blur_view(){
	document.getElementById("blur-view").style.display="block";
}

var _id;
function blur_update(_id_current){
	document.getElementById("blur-update").style.display="block";
	console.log("parametro"+_id_current);
	_id = _id_current;
	console.log("add valor "+_id_current);
	return _id
}

function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
});