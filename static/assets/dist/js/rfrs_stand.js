function submit_pointer(pointer_text) {
    //Set value "no" to all other pointers
    var other_pointers = [
    'data_from_sheet_text',
    'view_plot_data_text',
    'view_report_text',
    'pdf_report_text',
    'delete_stand_text'
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

function unhide_update(){
    var update_button = document.getElementById("update_stand");
    update_button.style = "visibility: visible";
}


function add_data_row() {
    const headers = ['STAND', 'PLOT', 'TREE', 'SPECIES', 'DBH', 'TOTAL HEIGHT'];
    var tbody = document.getElementById("rfrs_table_body");
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
    unhide_update()
    /*var update_button = document.getElementById("update_stand");
    update_button.style = "visibility: visible";*/
}