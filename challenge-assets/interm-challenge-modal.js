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


function submitkeynew(chal, key, nonce) {
    $('#submit-key').addClass("disabled-button");
    $('#submit-key').prop('disabled', true);
    $.post(script_root + "/chal/" + chal, {
        key: key,
        nonce: nonce,
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


$('#submit-key').unbind('click');
$('#submit-key').click(function (e) {
    e.preventDefault();
    submitkeynew($('#chal-id').val(), $('#answer-input').val(), $('#nonce').val());
});

function load_interm_award(chal) {
    $.get(script_root + '/intermflags/awards_mine/' + chal, function(obj) {

        $('#intermflag-list').html('');

        if (obj.length == 0) {

            html_award = `<div>Nothing for the moment. Keep searching !</div>`;
            $('#intermflag-list').append(html_award);

        } else {

            for (index=0 ; index < obj.length ; index++) {

                interm_award = obj[index];
                interm_award_title = interm_award[2];
                interm_award_img_url = interm_award[3];
                interm_award_score = interm_award[4];

                if (interm_award_score >= 0) {
                    color_class = "color-good";
                } else {
                    color_class = "color-bad";
                }

                if (interm_award_img_url != "") {
                    var html_award = `<div class="intermflag-list-elem ` + color_class + `"><img src="` + interm_award_img_url + `"> ` + interm_award_title + `</div>`;
                } else {
                    var html_award = `<div class="intermflag-list-elem ` + color_class + `">` + interm_award_title + `</div>`;
                }

                $('#intermflag-list').append(html_award);
            }

        }

    });
}

load_interm_award($('#chal-id').val());

// REC FUTURE : Sorry about that. Couldn't find better.
// https://stackoverflow.com/questions/11833325/css-hack-adding-css-in-the-body-of-a-website
function loadCSS(filename){
   var file = document.createElement("link");
   file.setAttribute("rel", "stylesheet");
   file.setAttribute("type", "text/css");
   file.setAttribute("href", filename);
   document.head.appendChild(file);
}
loadCSS(script_root + "/plugins/CTFd-intermediate-flag-plugin/challenge-assets/interm-challenge-style.css");


function load_interm_award_all(chal) {
    $.get(script_root + '/intermflags/awards_all/' + chal, function(obj) {

        $('#intermflag-list-all').html('');

        for (index=0 ; index < obj.length ; index++) {

            interm_award = obj[index];
            interm_award_date = interm_award[1];
            interm_award_team = interm_award[2];
            interm_award_title = interm_award[3];
            interm_award_img_url = interm_award[4];
            interm_award_score = interm_award[5];

            if (interm_award_score >= 0) {
                html_color_class = ``;
            } else {
                html_color_class = ` class="color-bad"`;
            }

            if ((interm_award_title == null) || (interm_award_img_url == null) || (interm_award_score == null)) {
                var html_award = `
                    <tr>
                        <td></td>
                        <td>????</td>
                        <td>` + interm_award_team + `</td>
                        <td>` + interm_award_date + `</td>
                    </tr>`;
            } else {
                if (interm_award_img_url == '') {
                    html_img = ``
                } else {
                    html_img = `<img src="` + interm_award_img_url + `">`
                }
                var html_award = `
                    <tr>
                        <td` + html_color_class + `>` + html_img + `</td>
                        <td` + html_color_class + `>` + interm_award_title + `</td>
                        <td` + html_color_class + `>` + interm_award_team + `</td>
                        <td` + html_color_class + `>` + interm_award_date + `</td>
                    </tr>`;
            }

            $('#intermflag-list-all').append(html_award);

        }

    });
}

$('.interm-awards-all').click(function (e) {
    load_interm_award_all($('#chal-id').val());
});


function load_authorized_files(chal) {

    $.get(script_root + '/intermflags/authorized_files/' + chal, function(obj) {

        $('#chal-files').html('');

        for (index=0 ; index < obj.length ; index++) {

            file_path = obj[index];
            var file_name = file_path.substring(file_path.lastIndexOf("/") + 1, file_path.length);

            html_file_button = `
                <div class='col-md-4 col-sm-4 col-xs-12 file-button-wrapper d-block'>
                    <a class='btn btn-info btn-file mb-1 d-inline-block px-2 w-100 text-truncate' href='` + script_root + `/files/` + file_path + `'>
                        <i class="fas fa-download"></i>
                        <small>` + file_name + `</small>
                    </a>
                </div>`;

            $('#chal-files').append(html_file_button);

        }

    });

}

load_authorized_files($('#chal-id').val());
