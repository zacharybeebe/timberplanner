$(document).ready(function() {
    $('#readonly_check').on('click', function(event){
        $.ajax({
            data: {
                'readonly': event.currentTarget.checked
            },
            type: 'POST',
            url: '/readonly'
        })
    });
});