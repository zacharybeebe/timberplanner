function submit() {
    var form = document.getElementById("form_filter");
    form.submit();
}

function delete_alert() {
    var warning = "Deleting a sale is permanent\n\nWould you like to continue with the sale deletion?";
    var delete_account = document.getElementById("delete_on");
    if (confirm(warning)) {
        delete_account.value = "on";
        submit();
    }
}

function select_all_items(checkbox_ultimo) {
    var delete_sale = document.getElementById("delete_sale");
    const checkboxes = document.querySelectorAll(".form-check-input");

    if (checkbox_ultimo.checked) {
      for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = true;
      }
      delete_sale.style = "visibility: visible;";
    } else {
      for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = false;
      }
      delete_sale.style = "visibility: hidden;";
    }
}

function unhide_delete() {
    var delete_sale = document.getElementById("delete_sale");
    var swap_sale = document.getElementById("swap_sale");
    var swap_text = document.getElementById("swap_on");

    const checkboxes = document.querySelectorAll(".form-check-input");
    var boxes_on = 0
    for (i in checkboxes){
        if (checkboxes[i].checked){
            boxes_on ++;
        }
    }

    if (boxes_on > 0) {
        delete_sale.style = "visibility: visible;";
        if (boxes_on == 2) {
            swap_sale.style = "visibility: visible;";
            swap_on.value = 'on'
        } else {
            swap_sale.style = "visibility: hidden;";
            swap_on.value = 'off'
        }
    } else {
        delete_sale.style = "visibility: hidden;";
    }
}

function row_onclick(event, redirect) {
    var elem = event.srcElement;
    if (elem.type != 'checkbox'){
      window.location.href = redirect;
    }
}