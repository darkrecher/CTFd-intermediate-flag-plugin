/*$('#submit-key0').unbind('click');
$('#submit-key0').click(function (e) {
    e.preventDefault();
    console.log(e);
    submitkey($('#chalid').val(), $('#answer-input0').val(), $('#nonce').val())
});
*/
$("#answer-input").keyup(function(event){
    if(event.keyCode == 13){
        $("#submit-key").click();
    }
});

$(".input-field").bind({
    focus: function() {
        $(this).parent().addClass('input--filled' );
        $label = $(this).siblings(".input-label");
    },
    blur: function() {
        if ($(this).val() === '') {
            $(this).parent().removeClass('input--filled' );
            $label = $(this).siblings(".input-label");
            $label.removeClass('input--hide' );
        }
    }
});
var content = $('.chal-desc').text();
var decoded = $('<textarea/>').html(content).val()

$('.chal-desc').html(marked(content, {'gfm':true, 'breaks':true}));

function submitkeynew(chal, key, nonce, count, keyname) {
    console.log(count);
    console.log(keyname);
    $('#submit-key').addClass("disabled-button");
    $('#submit-key').prop('disabled', true);
    $.post(script_root + "/chal/" + chal, {
        key: key,
        nonce: nonce,
        keyname: keyname,
    }, function (data) {
        var result = $.parseJSON(JSON.stringify(data));

        var result_message = $('#result-message');
        var result_notification = $('#result-notification');
        var answer_input = $('#answer-input');
        result_notification.removeClass();
        result_message.text(result.message);

        if (result.status == -1){
          window.location = script_root + "/login?next=" + script_root + window.location.pathname + window.location.hash
          return
        }
        else if (result.status == 0){ // Incorrect key
            result_notification.addClass('alert alert-danger alert-dismissable text-center');
            result_notification.slideDown();

            answer_input.removeClass("correct");
            answer_input.addClass("wrong");
            setTimeout(function () {
                answer_input.removeClass("wrong");
            }, 3000);
        }
        else if (result.status == 1){ // Challenge Solved
            result_notification.addClass('alert alert-success alert-dismissable text-center');
            result_notification.slideDown();

            $('.chal-solves').text((parseInt($('.chal-solves').text().split(" ")[0]) + 1 +  " Solves") );

            answer_input.val("");
            answer_input.removeClass("wrong");
            answer_input.addClass("correct");
        }
        else if (result.status == 2){ // Challenge already solved
            result_notification.addClass('alert alert-info alert-dismissable text-center');
            result_notification.slideDown();

            answer_input.addClass("correct");
        }
        else if (result.status == 3){ // Keys per minute too high
            result_notification.addClass('alert alert-warning alert-dismissable text-center');
            result_notification.slideDown();

            answer_input.addClass("too-fast");
            setTimeout(function() {
                answer_input.removeClass("too-fast");
            }, 3000);
        }
        marksolves();
        updatesolves();
        setTimeout(function(){
          $('.alert').slideUp();
          $('#submit-key').removeClass("disabled-button");
          $('#submit-key').prop('disabled', false);
        }, 3000);
    })
}

// TODO : pas besoin de faire une requete. On peut directement completer la page web.
$.get("/keynames/"+$('#chal-id').val(), function(data) {
    console.log(data);

    data.sort();

    $('#submit-key').unbind('click');
    $('#submit-key').click(function (e) {
        e.preventDefault();
        console.log('REC TODO. Appuyage bouton');
        j = this.name;
        // REC TODO : pas besoin de tous ces parametres.
        submitkeynew($('#chal-id').val(), $('#answer-input').val(), $('#nonce').val(), 0, $('#answer-input').attr('placeholder'));
    });

});

