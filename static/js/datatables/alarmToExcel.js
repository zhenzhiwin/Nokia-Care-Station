function saveCode(tableid) {
    var winname;
    var title = document.getElementById('hostname').innerText.toString() + '告警详情'
    try {
        if (navigator.userAgent.indexOf("MSIE") > 0)         //IE浏览器
        {
            var strHTML = $("#" + tableid).parent().html();
            //alert("IE浏览器");
            winname = window.open("ToExcel", "_blank", 'top=10000');

            winname.document.open('text/html', 'replace');
            winname.document.write("<style>");
            winname.document.write("table{border:solid 1px #000;text-align:center;border-collapse:collapse; border-spacing:0;}");
            winname.document.write("table td{border:solid 1px #000;text-align:center;}");
            winname.document.write("table th{border:solid 1px #000;text-align:center;}");
            winname.document.write("</style>");
            winname.document.write(strHTML);
            winname.document.execCommand('SaveAs', '', title + '.xls');
            document.execCommand("ClearAuthenticationCache");
            winname.close();
        } else if (isFirefox = navigator.userAgent.indexOf("Firefox") > 0)       //Firefox
        {
            //alert("Firefox");
            var str = getTblDataByFirefox(tableid, this);
            //支持中文
            var uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(str);
            var downloadLink = document.createElement("a");
            downloadLink.href = uri;
            downloadLink.download = title + ".csv";

            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

        } else       //Google Chrome
        {
            //alert("Google Chrome等浏览器");
            var str = getTblData(tableid, this);

            //支持中文
            var uri = 'data:text/csv;charset=utf-8,\ufeff' + encodeURIComponent(str);

            var downloadLink = document.createElement("a");
            downloadLink.href = uri;
            downloadLink.download = title + ".csv";

            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        }
    } catch (e) {
        alert(e.Message);
        return false;
    }
    return false;
}


function getTblData(inTbl, inWindow) {

    var rows = 0;
    var tblDocument = document;

    tblDocument = eval(inWindow).document;
    var curTbl = tblDocument.getElementById(inTbl);
    var outStr = "";
    if (curTbl != null) {
        for (var j = 0; j < curTbl.rows.length; j++) {
            for (var i = 0; i < curTbl.rows[j].cells.length; i++) {

                if (i == 0 && rows > 0) {
                    outStr += ",";
                    rows -= 1;
                }

                outStr += curTbl.rows[j].cells[i].innerText + ",";
                if (curTbl.rows[j].cells[i].colSpan > 1) {
                    for (var k = 0; k < curTbl.rows[j].cells[i].colSpan - 1; k++) {
                        outStr += ",";
                    }
                }
                if (i == 0) {
                    if (rows == 0 && curTbl.rows[j].cells[i].rowSpan > 1) {
                        rows = curTbl.rows[j].cells[i].rowSpan - 1;
                    }
                }
            }
            outStr += "\r\n";//换行
        }
    } else {
        outStr = null;
        alert(allPage.noData);
    }
    return outStr;
}