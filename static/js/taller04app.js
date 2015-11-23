var timeout= 5 * 60 * 1000;

function info_index(){
    $('#page-wrapper').load('info/main');
}

function questions_index(page){
    $('#page-wrapper').load('questions/main/'+ page);
}

function question_detail(question_id, ner_id){
    $('#page-wrapper').load('question/detail/'+ question_id+"/"+ ner_id);
}

function refresh_question_info(question_id, ner_id){
    $('#question_info').load('question/detail/info/'+ question_id+"/"+ ner_id);
}

function load_resource_info(uri){
	console.log(uri)
	$('#resource_info_modal_content').html('');
	$('#resource_info_modal_content').load('resource/info/'+ uri, function(){
		if($('#myModal')){
			$('#myModal').modal('show')
		}
	});
}

function tagcloud_index(){
    $('#page-wrapper').load('tagcloud/index', function(){
		$.ajax({
		    type: "POST",
		    url: "get_trending_topics",
		    dataType: "json",
		    timeout:  timeout, // in milliseconds
		    success: function (tags_data) {
		    	initTagsCloud(tags_data)
		    },
		    error: function (request, status, err) {
		    }
		});
    });
}


function initTagsCloud(tags_data){
	var fill = d3.scale.category20();
	var data = tags_data.map(function(d) {
		return d;
	});
	d3.layout.cloud().size([500, 500])

	.words(data)
	.rotate(function() { return ~~(Math.random() * 2) * 90; })
	.font("Impact")
	.fontSize(function(d) { return d.size; })
	.on("end", draw)
	.start();

	function draw(words) {
		$("#cloud-div").html('')
		d3.select("#cloud-div").append("svg")
		.attr("width", "700")
		.attr("height", "500")
		.append("g")
		.attr("transform", "translate(350,250)")
		.selectAll("text")
		.data(words)
		.enter().append("text")
		.style("font-size", function(d) { return d.size + "px"; })
		.style("font-family", "Impact")
		.style("fill", function(d, i) { return fill(i); })
		.attr("text-anchor", "middle")
		.attr("transform", function(d) {
			return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
		})
		.text(function(d) { return d.text; });
	}
}
