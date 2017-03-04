"use strict";

$(function () {

    $("#dateInput").show();
    $("#chart").show();

    var records = [];
    var chart = $('#chart');
    var startTime;
    var endTime;

    initChart();

    // user click view
    $("#submitTime").click(function () {
        var date = $("#date").val();
        var hour1 = $("#hr1").val();
        var min1 = $("#min1").val();
        var hour2 = $("#hr2").val();
        var min2 = $("#min2").val();
        startTime = date + "T" + hour1 + ":" + min1 + ":00";
        endTime = date + "T" + hour2 + ":" + min2 + ":00";
        //getChartData();
        drawChart();
    });


    $("#chartBtn").click(function () {
        $("#dateInput").show();
        $("#chart").show();
    });


    $("#addStudentBtn").click(function () {
        $("#dateInput").hide();
        $("#chart").hide();
        $.ajax({
            url: "/add",
            type: "POST",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                "name": $("#name-input").val(),
                "photo": $("#photo-input").val()
            }),
            success: function (data) {
                records = data.records;
                snackbarMessage("getData!");
            }
        });


    });


    function getChartData(startTime, endTime) {

        $.ajax({
            url: "",
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

    // initial chart
    function initChart() {

        var test = Math.round(new Date(startTime).getTime() / 1000);
        console.log(test);
        var chartData = [

            {
                label: "Confusion",
                values: [{
                    time: Math.round(new Date().getTime() / 1000),
                    y: 100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 80
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 50
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 40
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 30
                }]
            }
        ];

        chart = $('#chart').epoch({
            type: 'time.area',
            data: chartData,
            axes: ['top', 'right', 'bottom', 'left'],
            ticks: {
                time: 10,
                right: 5,
                left: 5
            },
            tickFormats: {
                time: function (d) {
                    return new Date(time * 1000).toString();
                }
            }

        });
    }


    function drawChart() {
        snackbarMessage("draw!");

        // format data
        var dtPoints = [];
        for (var i = 0; i < records.length; i++) {
            var point = {
                time: records[i][0],
                y: records[i][1]
            };
            dtPoints.push(point);
        }

        dtPoints.push({
            time: new Date().getTime(),
            y: 90
        });

        // plot the chart
        var delayMillis = 1000; //1 second

        for (var j = 0; j < dtPoints.length; j++) {
            setTimeout(function () {
                $('#chart').push(dtPoints[j]);
                $('#chart').redraw();
            }, delayMillis);
        }

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