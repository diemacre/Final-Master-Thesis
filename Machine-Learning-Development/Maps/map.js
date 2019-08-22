
<script>

var c1=null, c2=null;

$(document).ready(function() {
	const svg = d3.select('svg');
	svg.attr('width', '100%');
	svg.attr('height', '100vh');
});

function render_test_case(testid, t_x, t_y, e_x, e_y, error, portrait) {
	
	//Render positions in either portrait or landscape mode
	if (portrait) {
		tm_x = mapX(t_x)
		tm_y = mapY(t_y)
		em_x = mapX(e_x)
		em_y = mapY(e_y)
	} else {
		tm_y = mapX(parseFloat(d3.select('svg').attr('data-width'), 10)) - mapX(t_x)
		tm_x = mapY(t_y)
		em_y = mapX(parseFloat(d3.select('svg').attr('data-width'), 10)) - mapX(e_x)
		em_x = mapY(e_y)
	}
	
	var group = d3.select('svg').append('g').attr('class', 'tests');
	
	//The width of the tester and estimation circles
	t_r = 50
	e_r = 40
	z_r = 100	//The radius of the tester and estimation circles when hovering over them

	//Render tester position
	group.append('circle')
		.attr("cx", tm_x)
		.attr("cy", tm_y)
		.attr("data-html", "true")
		.attr("data-toggle", "tooltip")
		.attr("title", "Case: " + testid + "<br />Tester.x: " +  t_x.toFixed(4) + "<br />Tester.y: " +  t_y.toFixed(4) + "<br />Tester.error: " +  error.toFixed(4))
		.on('mouseover', function() {
			d3.select(this).transition()
				.duration(300)
				.attr("r", z_r);
			$(this).tooltip();
			$(this).tooltip('show');
		})
		.on('mouseout', function () {
			d3.select(this).transition()
				.duration(300)
				.attr("r", t_r);
		})
		.style("fill", "green")
		.style("fill-opacity", "0.6")
		.style("stroke", "black")
		.style("stroke-dasharray", "80, 50")
		.style("stroke-width", "8")
		.transition()
		.duration(300)
		.attr("r", 50)
		.attr("transform", "rotate(180deg)");

	//Render estimated position
	group.append('circle')
		.attr("cx", em_x)
		.attr("cy", em_y)
		.attr("data-html", "true")
		.attr("data-toggle", "tooltip")
		.attr("title", "Case: " + testid + "<br />Est.x: " +  e_x.toFixed(4) + "<br />Est.y: " +  e_y.toFixed(4) + "<br />Est.error: " +  error.toFixed(4))
		.on('mouseover', function() {
			d3.select(this).transition()
				.duration(300)
				.attr("r", z_r);
			$(this).tooltip();
			$(this).tooltip('show');
		})
		.on('mouseout', function () {
			d3.select(this).transition()
				.duration(300)
				.attr("r", e_r);
		})
		.style("fill", "purple")
		.style("fill-opacity", "0.6")
		.style("stroke", "black")
		.style("stroke-dasharray", "80, 50")
		.style("stroke-width", "8")
		.transition()
		.duration(300)
		.attr("r", e_r)
		.attr("transform", "rotate(180deg)");
		
	//Render the line between the circles
	group.append("line")
		.attr("x1", em_x)
		.attr("y1", em_y)
		.attr("x2", tm_x)
		.attr("y2", tm_y)
		.attr("stroke-width", 6)
		.attr("stroke", "black");
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

</script>