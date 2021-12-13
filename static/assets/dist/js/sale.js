var added_units = []

function submit() {
    var form = document.getElementById("form_item");
    form.submit();
}

function submit_check() {
    var file_input = document.getElementById("shp_file");
    var num_f = file_input.files.length;

    var button_zone = document.getElementById("button_zone");
    var bz_children = button_zone.children;

    for (elem in bz_children) {
        if (bz_children[elem].tagName == "B") {
            button_zone.removeChild(bz_children[elem]);
        }
    }

    var flasher = document.createElement("b");
    flasher.style = "color: rgba(84, 216, 226, .95);";

    const FILE_TYPES1 = '.shp.dbf';
    const FILE_TYPES2 = '.dbf.shp';


    if (num_f < 2) {
        flasher.innerHTML = "Please select both SHP and DBF files for the shapefile";
        button_zone.appendChild(flasher);
    } else if (num_f > 2) {
        flasher.innerHTML = "Cannot select more than one shapefile";
        button_zone.appendChild(flasher);
    } else {
        var file_types = '';
        for (var i = 0; i < file_input.files.length; i++){
            file_types += file_input.files[i].name.slice(-4);
        }
        if (file_types == FILE_TYPES1 || file_types == FILE_TYPES2){
            var form = document.getElementById("form_item");
            form.submit();
        } else {
            flasher.innerHTML = "Please select both SHP and DBF files for the shapefile";
            button_zone.appendChild(flasher);
        }
    }
}

function delete_submit() {
    var tbody = document.getElementById("sale_table_body");
    var tbody_rows = tbody.rows;

    var delete_units = [];
    var cb_on;
    var cb_name;
    for (var row = 0; row < tbody_rows.length; row++) {
        cb_on = tbody_rows[row].children[0].children[0].checked;
        cb_name = tbody_rows[row].children[0].children[0].name;
        if (cb_on){
            if (added_units.includes(cb_name)){
                tbody.deleteRow(row);
                added_units.splice(added_units.indexOf(cb_name), 1);
            } else {
                delete_units.push(cb_name);
            }
        }
    }
    if (delete_units.length > 0){
        var delete_holder = document.getElementById("delete_on");
        delete_holder.value = 'on';
        submit();
    }
}

function add_unit_row() {
    var trusts = [1, 3, 6, 7, 8, 9, 10, 11, 12, 77];
    var tbody = document.getElementById("sale_table_body");

    var u_nums = []
    for (var i = 0; i < tbody.rows.length; i++){
        for (var j = 0; j < tbody.rows[i].children.length; j++){
            var td = tbody.rows[i].children[j];
            if (td.id.slice(-4) == 'name'){
                u_nums.push(parseInt(td.children[0].children[0].value.slice(1)));
            }
        }
    }
    var next_unit = Math.max(...u_nums) + 1;
    var trow = document.createElement("tr");

    var tdd;
    var name_id;
    var inpt;
    var sml;

    for (var i = 0; i < 4; i++){
        if (i == 0){
            tdd = document.createElement("td");

            inpt = document.createElement("input");
            name_id = `cbx_${next_unit}`;

            inpt.type = "checkbox";
            inpt.className = "form-check-input";
            inpt.id = name_id;
            inpt.name = name_id;
            added_units.push(name_id);
            console.log("added_units", added_units);
            inpt.onclick = unhide_delete;

            tdd.appendChild(inpt);
            trow.appendChild(tdd);

        } else if (i == 1) {
            name_id = `U_attr_${next_unit}_unit_name`;
            tdd = document.createElement("td");
            tdd.id = name_id
            tdd.colSpan = 2
            sml = document.createElement("small");

            inpt = document.createElement("input");
            inpt.type = "text";
            inpt.name = name_id;
            inpt.value = `U${next_unit}`;
            inpt.style = "width: 70px;";

            sml.appendChild(inpt)
            tdd.appendChild(sml);
            trow.appendChild(tdd);

        } else if (i == 2) {
            tdd = document.createElement("td");
            tdd.colSpan = 2
            sml = document.createElement("small");

            inpt = document.createElement("input");
            name_id = `U_attr_${next_unit}_harvest`;
            inpt.type = "text";
            inpt.name = name_id;
            inpt.value = "VRH";
            inpt.style = "width: 70px;";

            sml.appendChild(inpt)
            tdd.appendChild(sml);
            trow.appendChild(tdd);

        } else {
            var subs = ['acres', 'mbf'];
            for (var trust in trusts) {
                for (sub in subs) {
                    tdd = document.createElement("td");
                    sml = document.createElement("small");

                    inpt = document.createElement("input");
                    name_id = `U_trust_${next_unit}_${trusts[trust]}_${subs[sub]}`;
                    inpt.type = "text";
                    inpt.name = name_id;
                    inpt.value = "0.0";
                    inpt.style = "width: 50px;";

                    sml.appendChild(inpt)
                    tdd.appendChild(sml);
                    trow.appendChild(tdd);
                }
            }
        }
    }
    tbody.appendChild(trow)
}

function select_all_items(checkbox_ultimo) {
    var delete_unit = document.getElementById("delete_unit");
    var submit_sale_edits = document.getElementById("submit_sale_edits");
    const checkboxes = document.querySelectorAll(".form-check-input");

    if (checkbox_ultimo.checked) {
      for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].id != "readonly_check") {
            checkboxes[i].checked = true;
        }
      }
      delete_unit.style = "visibility: visible;";
      submit_sale_edits.style = "visibility: hidden;";
    } else {
      for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].id != "readonly_check") {
            checkboxes[i].checked = false;
        }
      }
      delete_unit.style = "visibility: hidden;";
      submit_sale_edits.style = "visibility: visible;";
    }
}

function unhide_delete() {
    var delete_unit = document.getElementById("delete_unit");
    var submit_sale_edits = document.getElementById("submit_sale_edits");
    const checkboxes = document.querySelectorAll(".form-check-input");
    var visible = false;
    for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].id != "readonly_check") {
          if (checkboxes[i].checked) {
            visible = true;
            break;
          }
      }
    }
    if (visible) {
      delete_unit.style = "visibility: visible;";
      submit_sale_edits.style = "visibility: hidden;";
    } else{
      delete_unit.style = "visibility: hidden;";
      submit_sale_edits.style = "visibility: visible;";
    }
}