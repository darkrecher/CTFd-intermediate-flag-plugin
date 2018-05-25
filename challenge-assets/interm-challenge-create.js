// Markdown Preview
$('#desc-edit').on('shown.bs.tab', function (event) {
    if (event.target.hash == '#desc-preview'){
        $(event.target.hash).html(marked($('#desc-editor').val(), {'gfm':true, 'breaks':true}));
    }
});
$('#new-desc-edit').on('shown.bs.tab', function (event) {
    if (event.target.hash == '#new-desc-preview'){
        $(event.target.hash).html(marked($('#new-desc-editor').val(), {'gfm':true, 'breaks':true}));
    }
});
$('#solve-attempts-checkbox').change(function() {
    if(this.checked) {
        $('#solve-attempts-input').show();
    } else {
        $('#solve-attempts-input').hide();
        $('#max_attempts').val('');
    }
});


var count = 0;

function add_new_question() {
    var key = `
    <div class="form-group">

        <label>Flag
            <i class="far fa-question-circle text-muted cursor-help" data-toggle="tooltip" data-placement="right" title="This is the flag or solution for your challenge. You can choose whether your flag is a static string or a regular expression."></i>
        </label>
        <input type="text" class="form-control" name="key_solution[` + count + `]" placeholder="Enter Key Solution">
        <input type="number" class="form-control" name="award_interm[` + count + `]" placeholder="Points for intermediate flag (can be negative)" required>
        <input type="text" class="form-control" name="congrat_msg[` + count + `]" placeholder="Congratulation message">
        <input type="text" class="form-control" name="congrat_img_url[` + count + `]" placeholder="Congratulation image url">
        <input type="text" class="form-control" name="doc_filename[` + count + `]" placeholder="Link to document (optional)">

        Key type :
        <select class="custom-select" name="key_type[` + count + `]">
            <option value="static">Static</option>
            <option value="regex">Regex</option>
        </select>
        Public :
        <select class="custom-select" name="public[` + count + `]">
            <option value="yes">yes</option>
            <option value="no">no</option>
        </select>
        Cancel score when challenge is won :
        <select class="custom-select" name="cancel_score[` + count + `]">
            <option value="yes">yes</option>
            <option value="no">no</option>
        </select>

    </div>

    <div class="separator" style="border-top: 5px solid #888;"></div>`

    $('#key-list').append(key);
    count += 1;
}

$("#add-new-question").click(add_new_question);

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    add_new_question();
});
