var added_species = 2;

function submit_pointer(pointer_text) {
    //Set value "no" to all other pointers
    var other_pointers = [
    'rerun_report_text',
    'new_report_text'
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

function add_species(div_id, unit_list) {
    const PLANT_SPP = ['DOUGLAS_FIR', 'W_REDCEDAR', 'NOBLE_FIR', 'W_HEMLOCK', 'RED_ALDER',
                       'PAC_SILV_FIR', 'GRAND_FIR', 'SITKA_SPRUCE', 'W_WHITE_PINE', 'WHTBARK_PINE'];

    const STOCK_TYPE = ['1+1', 'P+1', 'P+0', 'P+P1', '2+0', 'P+1/2', 'P2+0', 'NATURAL'];

    var div = document.getElementById(div_id);
    div.appendChild(document.createElement('br'));

    div.appendChild(create_label(`UNITS ${added_species}:`));
    div.appendChild(create_select_units(`regen=mul|units_${added_species}`, unit_list));
    div.appendChild(document.createElement('br'));

    div.appendChild(create_label(`SPECIES ${added_species}:`));
    div.appendChild(create_select(`regen=addsel|species_${added_species}`, PLANT_SPP));
    div.appendChild(document.createElement('br'));

    div.appendChild(create_label(`STOCK TYPE ${added_species}:`));
    div.appendChild(create_select(`regen=addsel|stock_type_${added_species}`, STOCK_TYPE));
    div.appendChild(document.createElement('br'));

    div.appendChild(create_label(`TARGET TPA ${added_species}:`));
    div.appendChild(create_input(`regen=inpt|target_tpa_${added_species}`));
    div.appendChild(document.createElement('br'));

    added_species ++
}


function delete_activity(div_id) {
    div = document.getElementById(div_id);
    div.innerHTML = "";
    div.remove();
}


function create_label(val){
    var lab = document.createElement('label');
    lab.style = "width: 125px; text-align: left; font-weight: bold;";
    var sml = document.createElement('small');
    sml.innerHTML = val;
    lab.appendChild(sml);
    return lab
}

function create_select(name_id, opt_list){
    var sel = document.createElement('select');
    sel.id = name_id;
    sel.name = name_id;
    sel.className = "form-select form-select-sm mb-3";
    sel.ariaLabel = ".form-select-lg example";
    sel.style = "width: 300px; display: inline; vertical-align: top;";
    var opt;
    for (var i=0; i < opt_list.length; i++){
        opt = document.createElement('option');
        opt.value = opt_list[i];
        opt.innerHTML = opt_list[i];
        sel.add(opt);
    }
    return sel
}

function create_input(name_id){
    var inpt = document.createElement('input');
    inpt.type = 'text';
    inpt.id = name_id;
    inpt.name = name_id;
    inpt.style = "width: 300px;";
    inpt.value = 30;
    return inpt
}

function create_select_units(name_id, unit_list){
    var sel = document.createElement('select');
    sel.multiple = true;
    sel.size = Math.min(unit_list.length, 3);
    sel.id = name_id;
    sel.name = name_id;
    sel.className = "form-select form-select-sm mb-3";
    sel.ariaLabel = ".form-select-lg example";
    sel.style = "width: 300px; display: inline; vertical-align: top;";
    var opt;
    for (var i=0; i < unit_list.length; i++){
        opt = document.createElement('option');
        opt.selected = true;
        opt.value = unit_list[i];
        opt.innerHTML = unit_list[i];
        sel.add(opt);
    }
    return sel
}