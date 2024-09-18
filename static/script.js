$(document).ready(function() {
    $('.json-file').click(function(e) {
        e.preventDefault();
        let filename = $(this).data('filename');

        $.ajax({
            url: '/load_json',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ filename: filename }),
            success: function(data) {
                $('#file-content').text(JSON.stringify(data, null, 4));
            },
            error: function(err) {
                $('#file-content').text('Error loading file.');
            }
        });
    });
});
