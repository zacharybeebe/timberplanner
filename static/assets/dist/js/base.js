
function readonly_change(){
    var form = document.getElementById('readonly_form');
    var readonly = document.getElementById('readonly');
    var readonly_check = document.getElementById('readonly_check');
    var val;
    if(readonly_check.checked){
        val = true;
    } else {
        val = false;
    }
    readonly.value = val;
    form.submit()
}