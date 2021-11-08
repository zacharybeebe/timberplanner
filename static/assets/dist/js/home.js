function submit_pointer(pointer_text) {
    //Set value "no" to all other pointers
    var other_pointers = [
    'read_only',
    'editable'
    ];

    var other_pointer;
    for (var i = 0; i < other_pointers.length; i++){
        if (other_pointers[i] != pointer_text){
            other_pointer = document.getElementById(other_pointers[i]);
            other_pointer.value = "no";
        }
    }

    var pointer_text_elem = document.getElementById(pointer_text);
    pointer_text_elem.value = "yes";

    var form = document.getElementById("form_item");
    form.submit();
}
