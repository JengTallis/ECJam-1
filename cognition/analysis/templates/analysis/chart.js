"use strict";

$(function () {

    var records = [];

    $("#submitTime").click(function () {
        //getChartData();
        drawChart();
    });

    function getChartData(startTime, endTime) {

        $.ajax({
            url: "/viewHistory",
            type: "POST",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                "srart": startTime,
                "end": endTime
            }),
            success: function (data) {
                records = data.records;
                snackbarMessage("getData!");
            }
        });

    }

    function drawChart() {
        snackbarMessage("draw!");
        var dtPoints = [];
        for (var i = 0; i < records.length; i++) {
            var point = {
                x: records[i][0],
                y: records[i][1]
            };
            dtPoints.push(point);
        }

        dtPoints = [{
            x: 0,
            y: 100
        }, {
            x: 20,
            y: 1000
        }];



        var lineChartData = [

            {
                label: "Confusion",
                values: dtPoints
            },
            {
                label: "Satisfaction",
                values: [{
                    x: 20,
                    y: 1000
                }, {
                    x: 30,
                    y: 9800
                }]
            }
        ]
        console.log(lineChartData[0].values[0]);

        // chart
        var chart = $('#chart').epoch({
            type: 'area',
            data: lineChartData
        });
    }



    //snackbar
    var snackbar = document.getElementById("snackbar");

    // toast a snackbar message
    //param message is the message to be shown
    function snackbarMessage(message) {
        snackbar.innerHTML = message;
        snackbar.className = "show";
        setTimeout(function () {
            snackbar.className = snackbar.className.replace("show", "");
        }, 2500);
    }




});
