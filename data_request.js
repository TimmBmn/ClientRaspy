setInterval(setTime, 1000);
setInterval(getData, 5000);

function setTime() {
    const time = new Date().toLocaleTimeString()
    document.getElementById("time").innerText = time;

}

async function getData() {

	const data = await fetch("/data");
	const response = await data.json()
	
	insertToWebsite(response);
}

function insertToWebsite(data) {
	document.getElementById("room").innerText = data.room;
	document.getElementById("temp").innerText = data.temp;
	document.getElementById("limit").innerText = data.tlimit;

	if (data.water == 1) {
		document.getElementById("nass").innerText = "nass";
	} else {
		document.getElementById("nass").innerText = "trocken";
	}
}
