
function change_check(div_id, check_name) {
    var div = document.getElementById(div_id);
    var sub_div;
    var elem;
    for (var i=0; i < div.children.length; i++){
        sub_div = div.children[i];
        for (var j=0; j < sub_div.children.length; j++) {
            elem = sub_div.children[j];
            if (elem.type == 'checkbox' && elem.name != check_name && elem.checked){
                elem.checked = false;
            }
        }
    }
}