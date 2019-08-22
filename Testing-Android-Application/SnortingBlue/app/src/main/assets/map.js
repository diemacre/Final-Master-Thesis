
var c1=null, c2=null;

$(document).ready(function() {
	const svg = d3.select('svg');
	svg.attr('width', '100%');
	svg.attr('height', '100vh');
});

function setTestingLocation(x, y, mobile) {

	console.log("SET TESTING LOCATION IN JS!!!");

	if(c1 == null) {
		c1 = d3.select('svg').append("circle")
					.attr("cx", 0)
					.attr("cy", 0)
					.attr("r", 15);
	}
	if(c2 == null) {
		c2 = d3.select('svg').append("circle")
						.attr("cx", 0)
						.attr("cy", 0)
						.style("fill", "black")
						.style("fill-opacity", "0.59")
						.attr("r", 10)
						.attr("r", 100);
	}

	c1
		.attr("cx", mapX(x))
		.attr("cy", mapY(y));

	c2
		.attr("cx", mapX(x))
		.attr("cy", mapY(y));


	if(typeof(window.mapInterface) === "undefined")
	{
	    setTimeout(function() { setTestingLocation(x, y, mobile) }, 250);
	    return;
    }

	console.log("SET TESTING LOCATION NEARLY OUT OF JS!!!");
	console.log(window.mapInterface);
	window.mapInterface.setTestingLocationJS(x, y);
}

function setTestingLocationPX(x, y, mobile) {

	if(c1 == null) {
		c1 = d3.select('svg').append("circle")
					.attr("cx", 0)
					.attr("cy", 0)
					.attr("r", 15);
	}
	if(c2 == null) {
		c2 = d3.select('svg').append("circle")
						.attr("cx", 0)
						.attr("cy", 0)
						.style("fill", "black")
						.style("fill-opacity", "0.59")
						.attr("r", 10)
						.attr("r", 100);
	}

	c1
		.attr("cx", x)
		.attr("cy", y)
		.attr("r", 15);

	c2
		.attr("cx", x)
		.attr("cy", y);
}

function removeAllBeacons() {
	d3.selectAll('.beacons').remove();
}

function renderBeaconByMajorMinor(major, minor, rssi, mobile, map) {
    url = "https://api.iitrtclab.com/beacons/"
    url.concat(map)

    console.log("In renderBeaconByMajorMinor");

	$.get(url, (beacons, err) => {
		beacons.forEach((beacon) => {
			if (beacon.major === major && beacon.minor === minor) {
			    console.log("FOUND MATCH!: ");
			    console.log(beacon);
				setBeacon(beacon, mobile, {rssi: rssi});
			}
		});
	});
}

function toggleSettingLocation(toggle, mobile) {

    console.log("TOGGLE SETTING LOCATION!!!");

	if (toggle) {
		d3.select('svg').on("click", function () {
			// This function will run when someone clicks on map when toggle mode is activated
			let coordinates = d3.mouse(this);
			let position = realPosition(coordinates[0], coordinates[1], mobile);
			setTestingLocationPX(coordinates[0], coordinates[1]);

            console.log("TOGGLE NEARLY OUT OF JS!!!");
            console.log(window.mapInterface);
			window.mapInterface.setTestingLocationJS(position.x, position.y);
		});
	} else {
		d3.select('svg').on('click', null);
	}
	
	console.log("TOGGLE SETTING LOCATION JS!!!\n");
}

//returns real life x and y from locked origin in meters
function realPosition(svgX, svgY, mobile) {
	let positionObject = {};
	if (mobile) {
		positionObject.x = inverseMapX(svgX);
		positionObject.y = inverseMapY(svgY);
	} else {
		positionObject.x = parseFloat(d3.select('svg').attr('data-width'), 10) - inverseMapX(svgY);
		positionObject.y = inverseMapY(svgX);
	}
	return positionObject;
}

function setBeacon(beacon, mobile, beaconRssi) {

    console.log("SETTING BEACON!!!");
    console.log("X: ");
    console.log(beacon.x)

    console.log("SET BEACON OUT OF JS!!!");
    window.mapInterface.setBeaconLocationJS(beacon.major, beacon.minor, beacon.x, beacon.y);
    console.log("SHOULD HAVE CALLED SET BEACON LOCATION!!!");

	if (mobile) {
		renderBeacon(mapX(beacon.x), mapY(beacon.y), beacon, beaconRssi);
	} else {
		const newX = mapX(parseFloat(d3.select('svg').attr('data-width'), 10)) - mapX(beacon.x);
		renderBeacon(mapY(beacon.y), newX, beacon, beaconRssi);
	}
}

function renderBeacon (x, y, beacon, beaconRssi) {
	var group = d3.select('svg').append('g').attr('class', 'beacons').attr('id', `${beacon.beacon_id}`).attr('beacon-data', JSON.stringify(beacon));

	group.append('circle')
		.attr("cx", x)
		.attr("cy", y)
		.attr("r", 15);

	group.append('circle')
		.attr("cx", x)
		.attr("cy", y)
		.attr("r", 0)
		.attr("data-toggle", "tooltip")
		.attr("title", `Major: ${beacon.major} Minor: ${beacon.minor} RSSI: ${beaconRssi.rssi}`)
		.on('mouseover', function() {
			d3.select(this).transition()
				.duration(300)
				.attr("r", "100");
			$(this).tooltip();
			$(this).tooltip('show');
		})
		.on('mouseout', function () {
			d3.select(this).transition()
				.duration(300)
				.attr("r", "50");
		})
		.style("fill", returnRGBColor((-beaconRssi.rssi)))
		.style("fill-opacity", "0.6")
		.style("stroke", "black")
		.style("stroke-dasharray", "80, 50")
		.style("stroke-width", "8")
		.transition()
		.duration(300)
		.attr("r", 50)
		.attr("transform", "rotate(180deg)");
}

function returnRGBColor(temp) {
	if (!temp) {
		return 'rgb(159, 161, 165)';
	}
	let max = 100;
	let avg = temp/max;
	let red = Math.round((1 - avg) * 255);
	let green = avg >= 0.5 ? 1 : 0;
	let blue = Math.round(avg*255);
	return `rgb(${red}, ${green}, ${blue})`;
}

function mapX (x) {
	const origin = d3.select('.origin').filter('path').node().getBBox();
	const originTop = d3.select('.originTop').filter('path').node().getBBox();
	const in_min = 0;
	const in_max = parseFloat(d3.select('svg').attr('data-width'), 10);
	const out_min = origin.x;
	const out_max = originTop.x + originTop.width;
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function inverseMapX(svgX) {
	const origin = d3.select('.origin').filter('path').node().getBBox();
	const originTop = d3.select('.originTop').filter('path').node().getBBox();
	const in_min = origin.x;
	const in_max = originTop.x + originTop.width;
	const out_min = 0;
	const out_max = parseFloat(d3.select('svg').attr('data-width'), 10);
	return (svgX - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function mapY (y) {
	const origin = d3.select('.origin').filter('path').node().getBBox();
	const originTop = d3.select('.originTop').filter('path').node().getBBox();
	const in_min = 0;
	const in_max = parseFloat(d3.select('svg').attr('data-height'), 10);
	const out_min = origin.y + origin.height;
	const out_max = originTop.y;
	return (y - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function inverseMapY(svgY) {
	const origin = d3.select('.origin').filter('path').node().getBBox();
	const originTop = d3.select('.originTop').filter('path').node().getBBox();
	const in_min = origin.y + origin.height;
	const in_max = originTop.y;
	const out_min = 0;
	const out_max = parseFloat(d3.select('svg').attr('data-height'), 10);
	return (svgY - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}