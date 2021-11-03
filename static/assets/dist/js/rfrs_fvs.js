added_stands = [];

function submit() {
    var form = document.getElementById("form_item");
    form.submit();
}


function toggle_create(visibility){
    var create_fvs = document.getElementById('create_fvs');
    create_fvs.style = `visibility: ${visibility};`;
}


function stand_select(selection){
    var options = selection.options;

    for (i = 0; i < options.length; i++) {
        var val = options[i].value;
        if (options[i].selected) {
            if (! added_stands.includes(val)){
                added_stands.push(val);
                create_fvs_stand_div(val);
                toggle_create('visible')
            }
        } else {
            if (added_stands.includes(val)){
                added_stands.splice(added_stands.indexOf(val), 1)
                document.getElementById(`stand_div_${val}`).remove();
            }
        }
    }
    if (added_stands.length == 0){
        toggle_create('hidden')
    }
}


function create_fvs_stand_div(stand_name){
    var form = document.getElementById('form_item');
    var div = document.createElement('div');
    div.id = `stand_div_${stand_name}`;

    var heads = [['Variant', 'PN'], ['Forest Code', 612], ['Region Code', 6], ['Stand Age', ''], ['Site Species', 'DF'], ['Site Index', '']];

    var p = document.createElement('p');
    var stand_label = document.createElement('label');
    stand_label.innerHTML = 'Stand';
    stand_label.style = 'width: 200px; font-weight: bold;';
    p.appendChild(stand_label)

    var label;
    for (var i = 0; i < heads.length; i++){
        label = document.createElement('label');
        label.innerHTML = heads[i][0]
        label.style = 'width: 100px; font-weight: bold; text-align: center;';
        p.appendChild(label)
    }
    div.appendChild(p)

    p = document.createElement('p');
    stand_label = document.createElement('label');
    stand_label.innerHTML = stand_name;
    stand_label.style = 'width: 200px; font-weight: bold;';
    p.appendChild(stand_label)

    var inpt;
    for (var i = 0; i < heads.length; i++){
        inpt = document.createElement('input');
        inpt.type = "text";
        inpt.style = 'width: 100px;';
        var name_id = `${heads[i][0]}_${stand_name}`;
        inpt.id = name_id;
        inpt.name = name_id;
        inpt.value = heads[i][1]
        p.appendChild(inpt)
    }
    div.appendChild(p)
    p = document.createElement('p')
    p.innerHTML = '&emsp;'
    div.append(p)
    form.appendChild(div)
}

function submit_pointer(pointer_text) {
    //Set value "no" to all other pointers
    var other_pointers = [
    'data_from_previous_stand',
    'process_data_text',
    'data_from_sheet_text',
    'data_from_sheet_dnr'
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




