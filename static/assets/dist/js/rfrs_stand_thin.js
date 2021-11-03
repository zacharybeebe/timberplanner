function export_report() {
    var form = document.getElementById("form_item");
    var export_pdf = document.getElementById("export_report_pdf");
    export_pdf.value = "yes";
    form.submit();
}