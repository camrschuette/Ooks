"use strict"

function soundPlay(){
	var sound = document.getElementById("audio");
	sound.play();
	setTimeout(function() {
    x = x * 3 + 2;
    y = x / 2;
	}, 5000);
}