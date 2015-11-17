function info_index(){
    $('#page-wrapper').load('info/main');
}

function questions_index(){
    $('#page-wrapper').load('questions/main', function() {
        if($('#myModal')){
            $('#myModal').modal('show')
        }        
    });
}