function send1() {
    document.form.action = "{{ url_for('main.set_path') }}";
    document.form.submit();
}

function send2() {
    document.form.action = "{{ url_for('main.get_path') }}";
    document.form.submit();
}

$.getJSON('/get_path', function (oData) {
    // oData = {"username":"nimojs","userid":1}
    $('.file_list').html(oData.result);
})
