function info_index(){
    $('#page-wrapper').load('info/main');
}

function questions_index(page){
    $('#page-wrapper').load('questions/main/'+ page, function() {
        if($('#myModal')){
            $('#myModal').modal('show')
        }        
    });
}