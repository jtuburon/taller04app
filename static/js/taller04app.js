function info_index(){
    $('#page-wrapper').load('info/main');
}

function questions_index(page){
    $('#page-wrapper').load('questions/main/'+ page);
}

function question_detail(question_id){
    $('#page-wrapper').load('question/detail/'+ question_id);
}