function main(){
	var xhr = new XMLHttpRequest();
	var feed = document.getElementById("ookook");

	xhr.addEventListener("loadend", function(){
		if (xhr.readyState === 4 && xhr.status === 200) {
			var res = xhr.responseText;
			var res = JSON.parse(res);
			feed.innerHTML = "";
			for (var i=res.length-1; i>=0; --i){
			    var feed_string = "<p align='left' class='ook'><span class='foo'>" + res[i].username + " " + res[i].time + "</span><br> " + res[i].ook + "</p>";
			    feed.innerHTML += feed_string;
			}
			setTimeout(main, 5000)
		}
	});
	xhr.open("GET", "/feed.html");
	xhr.send(null);
}