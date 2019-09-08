function search_unit(obj) {
    setTimeout(function () {
        var storeId = document.getElementById('dataTable');
        var rowsLength = storeId.rows.length;
        var key = obj.value.toUpperCase();
        var searchCol = 1;
        for (var i = 2; i < rowsLength; i++) {
            var searchText = storeId.rows[i].cells[searchCol].innerHTML;
            if (searchText.match(key)) {
                storeId.rows[i].style.display = '';
            } else {
                storeId.rows[i].style.display = 'none';
            }
        }
    }, 200);
}

function search_level(obj) {
    setTimeout(function () {
        var storeId = document.getElementById('dataTable');
        var rowsLength = storeId.rows.length;
        var searchCol = 2;
        var key = obj.value.toString();
        for (var i = 2; i < rowsLength; i++) {
            var searchText = storeId.rows[i].cells[searchCol].innerHTML;
            searchText.toString()
            if ((searchText == key) || (key == '')) {
                storeId.rows[i].style.display = '';
            } else {
                storeId.rows[i].style.display = 'none';
            }
        }
    }, 200);
}

function search_time() {
    setTimeout(function () {
        var storeId = document.getElementById('dataTable');
        var startime = $("#starttime").val();
        startime = startime.replace(/[-\s:]+/g, "");
        var rowsLength = storeId.rows.length;
        var searchCol = 3;
        var key = $("#endtime").val();
        key = key.replace(/[-\s:]+/g, "")
        for (var i = 2; i < rowsLength; i++) {
            var searchText = storeId.rows[i].cells[searchCol].innerHTML;
            searchText = searchText.replace(/[-\s:]+/g, "")
            if (((parseInt(searchText) < parseInt(key)) && (parseInt(searchText) > parseInt(startime))) || (key == '')) {
                storeId.rows[i].style.display = '';
            } else {
                storeId.rows[i].style.display = 'none';
            }
        }
    }, 200);
}

function search_id(obj) {
    setTimeout(function () {
        var storeId = document.getElementById('dataTable');
        var rowsLength = storeId.rows.length;
        var key = obj.value.toUpperCase();
        var searchCol = 4;
        for (var i = 2; i < rowsLength; i++) {
            var searchText = storeId.rows[i].cells[searchCol].innerHTML;
            if (searchText.match(key)) {
                storeId.rows[i].style.display = '';
            } else {
                storeId.rows[i].style.display = 'none';
            }
        }
    }, 200);
}

function search_info(obj) {
    setTimeout(function () {
        var storeId = document.getElementById('dataTable');
        var rowsLength = storeId.rows.length;
        var key = obj.value.toUpperCase();
        var searchCol = 5;
        for (var i = 2; i < rowsLength; i++) {
            var searchText = storeId.rows[i].cells[searchCol].innerHTML;
            if (searchText.match(key)) {
                storeId.rows[i].style.display = '';
            } else {
                storeId.rows[i].style.display = 'none';
            }
        }
    }, 200);
}