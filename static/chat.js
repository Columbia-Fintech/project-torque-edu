function displayHistory(history){
    $("#answer-display").empty();
    $.each(history, function(i, h){
        let new_row_q = $("<div class=q-container></div>")
        let q_display = $("<div class='display display_q'>"+h['question']+"</div>")
        $(new_row_q).append(q_display);
        let new_row_a = $("<div class=a-container></div>")
        let a_display = $("<div class='display display_a'>"+h['answer']+"</div>")
        $(new_row_a).append(a_display);

        $("#answer-display").append(new_row_q);
        $("#answer-display").append(new_row_a);
    })
    // console.log($("#answer-display")[0].scrollHeight, $("#answer-display")[0].clientHeight)
    $("#answer-display")[0].scrollTop = $("#answer-display")[0].scrollHeight - $("#answer-display")[0].clientHeight;

}
function q_check(question){

    if ($.trim(question)==''){
            console.log("NO input")
    }
    else{
        let max_tokens = $("#max-tokens").val();

        let to_ask = {
            'endpoint': endpoint,
            'question': question,
            'max_tokens': max_tokens,
        }
        if (endpoint == 'answer') {
            let max_rerank = $("#max-rerank").val();
            to_ask['max_rerank'] =  max_rerank;
        }
        else if(endpoint == "completion"){
            let temp = $("#temperature").val();
            let max_tokens = $("#max-tokens").val();
            to_ask['temperature'] = temp;
        }
       $.ajax({
           type: "POST",
           url: "/ask",
           dataType : "json",
           contentType: "application/json; charset=utf-8",
           data : JSON.stringify(to_ask),
           success: function(result){
               let r = result["data"]
               data = r
               console.log(data)
               displayHistory(data);
           }
       }).done(function() {
        setTimeout(function(){
            $("#overlay").fadeOut(300);
        },500);
       });
    }
    $("#question").val("")
}

function getPosition(element) {
    console.log(element)
    var xPosition = 0;
    var yPosition = 0;

    while (element) {
        xPosition += (element.offsetLeft - element.scrollLeft + element.clientLeft);
        yPosition += (element.offsetTop - element.scrollTop + element.clientTop);
        element = element.offsetParent;
    }

    return {'x': xPosition, 'y': yPosition}
}

$(document).ready(function() {

    displayHistory(history);
     $(document).ajaxSend(function() {
         console.log($("#answer-display"))
         // var elDistanceToTop = $("#answer-display").offsetTop;
         //     console.log(elDistanceToTop)
         $("#overlay").offset({top:$("#answer-display").offset().top});
         $("#overlay").height($("#answer-display").height());
         $("#overlay").width($("#answer-display").width());

        $("#overlay").fadeIn(300);　
      });
    if (endpoint == "completion"){
        $("#max-rerank").prop('disabled', true)
    }
    else{
        $("#temperature").prop('disabled', true)
    }
    $(document).on('click', "#q-btn", function(){
        // console.log("button clicked")
        question = $("#question").val();
        q_check(question);
    })
    $("#question").on("keypress", function(event){
        // console.log("ENTER pressed")
        let keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            question = $("#question").val();
            q_check(question);
        }
    })
})
