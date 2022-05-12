$(document).ready(function() {
    $(document).on('click', "#start-chat-container", function(){
        let endpoint= $("#endpoint").val();
        window.location.href = "/chat/"+endpoint;
    })
})