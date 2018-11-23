function _setPath() {
    $('#box1_input4').on('click', function () {
        $.ajax({
            url: '/set_path',
            method: 'GET',
            data: {
                "key": '查看路径列表',
            },
            dataType: 'JSON',
            success: function (data) {
                if (data.data.length > 0) {
                    var pathArray = data.data;
                    var pathHtml = '<br/>';
                    for (var i = 0; i < pathArray.length; i++) {
                        var pathItem = pathArray[i] + '<br/>';
                        pathHtml += pathItem;
                    }
                }
                $('.file_list').html(pathHtml);
            },
            error: function () {
                console.log(222);
            }
        })
    })
}


function _filter_file(val) {
    $('.box2-submit').on('click', function () {
        var submitValue = $(this).val();
        var orderNo = $('#box2_input1').val();

        $.ajax({
            url: '/filter_file',
            method: 'GET',
            data: {
                "key": submitValue,
                "orderNo": orderNo,
            },
            dataType: 'JSON',
            success: function (data) {
                if (data.result) {
                    if (data.data.length > 0) {
                        var pathArray = data.data;
                        var pathHtml = '';
                        for (var i = 0; i < pathArray.length; i++) {
                            var pathItem = pathArray[i] + '<br/>';
                            pathHtml += pathItem;
                        }
                    }
                    $('.file_content').html(pathHtml);
                } else {
                    alert(data.message);
                }
            },
            error: function () {
                console.log(222);
            }
        })
    });
    $('.box2-submit-clear').on('click', function () {
        var submitValue = $(this).val();
        var orderNo = $('#box2_input1').val();

        $.ajax({
            url: '/filter_file',
            method: 'GET',
            data: {
                "key": submitValue,
                "orderNo": orderNo,
            },
            dataType: 'JSON',
            success: function (data) {
                if (data.result) {
                    $('.file_content').html(data.message);
                    window.location.reload(); //刷新当前页面
                } else {
                    alert(data.message);
                }
            },
            error: function () {
                console.log(222);
            }
        })
    });


}

function _filterCon() {
    $('.box3-submit').on('click', function () {
        var submitKey = $(this).val();
        var order = $('#box2_input1').val();
        var keyword = $('#box3_input1').val();

        $.ajax({
            url: '/filter_con',
            method: 'GET',
            data: {
                "key": submitKey,
                "order": order,
                "keyword": keyword
            },
            dataType: 'JSON',
            success: function (data) {
                if (data.result) {
                    if (data.data.length > 0) {
                        var pathArray = data.data;
                        var pathHtml = '';
                        for (var i = 0; i < pathArray.length; i++) {
                            var pathItem = pathArray[i] + '<br/><br/>';
                            pathHtml += pathItem;
                        }
                    }
                    $('.result-container').html(pathHtml);
                } else {
                    alert(data.message);
                }
            },
            error: function () {
                console.log(222);
            }
        })
    })
}

//
//
// function _filterCon () {
//     $('.box3-submit').on('click', function () {
//         var submitKey = $(this).val();
//         var order = $('#box2_input1').val();
//         var keyword = $('#box3_input1').val();
//
//         $.ajax({
//             url: '/filter_con',
//             method: 'GET',
//             data: {
//                 "key": submitKey,
//                 "order": order,
//                 "keyword": keyword
//             },
//             dataType: 'JSON',
//             success: function (data) {
//                 if (data.result) {
//                     $('#box4 .result-container').html(data);
//                 } else {
//                     alert(data.message);
//                 }
//             },
//             error: function () {
//                 console.log(222);
//             }
//         })
//     })
// }

window.onload = function () {
    console.log(123);
    _setPath();
    _filter_file();
    _filterCon();
}
