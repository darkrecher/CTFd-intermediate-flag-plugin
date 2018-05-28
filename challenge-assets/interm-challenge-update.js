$('#submit-key').click(function (e) {
    submitkey($('#chalid').val(), $('#answer').val())
});

$('#submit-keys').click(function (e) {
    e.preventDefault();
    $('#update-keys').modal('hide');
});

$('#limit_max_attempts').change(function() {
    if(this.checked) {
        $('#chal-attempts-group').show();
    } else {
        $('#chal-attempts-group').hide();
        $('#chal-attempts-input').val('');
    }
});

// Markdown Preview
$('#desc-edit').on('shown.bs.tab', function (event) {
    if (event.target.hash == '#desc-preview'){
        $(event.target.hash).html(marked($('#desc-editor').val(), {'gfm':true, 'breaks':true}))
    }
});
$('#new-desc-edit').on('shown.bs.tab', function (event) {
    if (event.target.hash == '#new-desc-preview'){
        $(event.target.hash).html(marked($('#new-desc-editor').val(), {'gfm':true, 'breaks':true}))
    }
});

function loadchal(id, update) {

    $.get(script_root + '/admin/chal/' + id, function(obj) {
        $('#desc-write-link').click(); // Switch to Write tab
        $('.chal-title').text(obj.name);
        $('.chal-name').val(obj.name);
        $('.chal-desc-editor').val(obj.description);
        $('.chal-value').val(obj.value);
        if (parseInt(obj.max_attempts) > 0){
            $('.chal-attempts').val(obj.max_attempts);
            $('#limit_max_attempts').prop('checked', true);
            $('#chal-attempts-group').show();
        }
        $('.chal-category').val(obj.category);
        $('.chal-id').val(obj.id);
        $('.chal-hidden').prop('checked', false);
        if (obj.hidden) {
            $('.chal-hidden').prop('checked', true);
        }

        // REC FUTURE : imbrication d'appels ajax. C'est moche.
        $.get(script_root + '/admin/interm_flags_config/' + id, function(obj) {

            key_ids_str = Object.keys(obj);
            key_ids_int = [];
            for (index=0 ; index < key_ids_str.length ; index++) {
                key_ids_int.push(parseInt(key_ids_str[index]));
            }
            key_ids_int.sort();
            count = 0;

            for (index=0 ; index < key_ids_int.length ; index++) {

                key_id_str = key_ids_int[index].toString();
                key_info = obj[key_id_str]

                var html_key = `
                <div class="form-group">
                    <input type="hidden" value="` + key_id_str + `" name="key_id[` + count + `]">
                    <input type="number" class="form-control" name="award_interm[` + count + `]" placeholder="Points for intermediate flag (can be negative)" required value="` + key_info['award'] + `">
                    <input type="text" class="form-control" name="congrat_msg[` + count + `]" placeholder="Congratulation message" value="` + key_info['congrat_msg'] + `">
                    <input type="text" class="form-control" name="congrat_img_url[` + count + `]" placeholder="Congratulation image url" value="` + key_info['congrat_img_url'] + `">
                    <input type="text" class="form-control" name="doc_filename[` + count + `]" placeholder="Link to document (optional)" value="` + key_info['doc_filename'] + `">

                    Key type :
                    <select class="custom-select" name="key_type[` + count + `]">
                        <option ` + (key_info['key_type']=='static'?'selected="selected"':'') + ` value="static">Static</option>
                        <option ` + (key_info['key_type']=='regex'?'selected="selected"':'') + ` value="regex">Regex</option>
                    </select>

                    Public :
                    <select class="custom-select" name="public[` + count + `]">
                        <option ` + ((!key_info['public'])?'selected="selected"':'') + ` value="no">no</option>
                        <option ` + (key_info['public']?'selected="selected"':'') + ` value="yes">yes</option>
                    </select>

                    Cancel score when challenge is won :
                    <select class="custom-select" name="cancel_score[` + count + `]">
                        <option ` + ((!key_info['cancel_score'])?'selected="selected"':'') + ` value="no">no</option>
                        <option ` + (key_info['cancel_score']?'selected="selected"':'') + ` value="yes">yes</option>
                    </select>

                </div>

                <div class="separator" style="border-top: 5px solid #888;"></div>`

                $('#key-list').append(html_key);

                count += 1;
            }

        });

        if (typeof update === 'undefined')
            $('#update-challenge').modal();
    });

}

function openchal(id){
    loadchal(id);
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});
