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