added_stands = 0;

function submit_pointer(pointer_text) {
    //Set value "no" to all other pointers
    var other_pointers = [
    'export_blank_sheet_text',
    'data_from_previous_stand',
    'process_data_text',
    'data_from_sheet_text',
    'data_from_sheet_dnr',
    'data_from_sheet_fvs'
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

function add_stand(){
    var added_stands_div = document.getElementById("added_stands_div");

    if (added_stands == 0){
        var labels = ['Stand Name', 'Plot Factor'];
        var pp = document.createElement('p');
        var label;
        for (var i=0; i < labels.length; i++){
            label = document.createElement('label');
            label.style = "width: 200px; text-align: center; font-weight: bold;";
            label.innerHTML = labels[i];
            pp.appendChild(label);
        }
        added_stands_div.appendChild(pp);
    }

    var names = ['name', 'pf'];
    pp = document.createElement('p');
    var inpt;
    for (var i = 0; i < names.length; i++){
        inpt = document.createElement('input');
        inpt.type = 'text';
        inpt.style = "width: 200px;";
        inpt.name = `add_${added_stands}_${names[i]}`;
        pp.appendChild(inpt);
    }
    added_stands_div.appendChild(pp);

    var add_stand_button = document.getElementById("add_stand_button");
    add_stand_button.style = "visibility: visible;";
    added_stands ++
}

function blank_sheet(){
    var added_stands_div = document.getElementById("added_stands_div");
    added_stands_div.innerHTML = "";

    if (added_stands == 0){
        add_stand();
    }

    const headers = ['STAND', 'PLOT', 'TREE', 'SPECIES', 'DBH', 'TOTAL HEIGHT'];
    var tbody = document.getElementById("rfrs_table_body");
    tbody.innerHTML = ''

    var trow;
    var tdd;
    var inpt;

    for (row = 1; row < 41; row++){
        trow = document.createElement('tr')
        tdd = document.createElement("td");
        tdd.style = "width: 15px;";

        var sml = document.createElement("small");
        sml.innerHTML = row;

        tdd.appendChild(sml);
        trow.appendChild(tdd);

        for (var i = 0; i < headers.length; i++) {
            tdd = document.createElement("td");
            inp = document.createElement("input");
            inp.type = "text";
            inp.name = `rfrs_${headers[i]}_${row}`;
            tdd.appendChild(inp);
            trow.appendChild(tdd);
        }
        tbody.appendChild(trow);
    }
    var process_data_button = document.getElementById("process_data");
    process_data_button.style = "visibility: visible;";
}

function add_data_row() {
    const headers = ['STAND', 'PLOT', 'TREE', 'SPECIES', 'DBH', 'TOTAL HEIGHT'];
    var tbody = document.getElementById("rfrs_table_body");
    console.log("rows_length", tbody.rows.length)
    if (tbody.rows.length == 0){
        add_stand()
    }

    var next_row = tbody.rows.length + 1;
    var trow = document.createElement("tr");

    var tdd
    var inpt

    tdd = document.createElement("td");
    tdd.style = "width: 15px;";

    var sml = document.createElement("small");
    sml.innerHTML = next_row;

    tdd.appendChild(sml);
    trow.appendChild(tdd);

    for (var i = 0; i < headers.length; i++) {
        tdd = document.createElement("td");
        inp = document.createElement("input");
        inp.type = "text";
        inp.name = `rfrs_${headers[i]}_${next_row}`;
        tdd.appendChild(inp);
        trow.appendChild(tdd);
    }
    tbody.appendChild(trow);

    var process_data_button = document.getElementById("process_data");
    process_data_button.style = "visibility: visible;";

}