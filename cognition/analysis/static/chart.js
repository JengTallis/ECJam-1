"use strict";

$(function () {

    $("#dateInput").show();
    $("#chart").show();
    $("#add-student").hide();

    var records = [];
    var chart = $('#chart');

    initChart();

    // user click view
    $("#submitTime").click(function () {
<<<<<<< HEAD
        var date = $("#date").val();
        var hour1 = $("#hr1").val();
        var min1 = $("#min1").val();
        var hour2 = $("#hr2").val();
        var min2 = $("#min2").val();
        startTime = {
            "date": date,
            "hour": hour1,
            "minute": min1
        };
        startTime = {
            "date": date,
            "hour": hour2,
            "minute": min2
        };
        getChartData();
        drawChart();
    });


    $("#chartBtn").click(function () {
        $("#dateInput").show();
        $("#chart").show();
        $("#add-student").hide();
    });

    $("#addStudentBtn").click(function () {
        $("#dateInput").hide();
        $("#chart").hide();
        $("#add-student").show();
    });


    $("#submitStudent").click(function () {
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

    function getChartData() {
        $.ajax({
            url: "",
            type: "POST",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                "srart": {
                    "date": $("#date").val(),
                    "hour": $("#hr1").val(),
                    "minute": $("#min1").val()
                },
                "end": {
                    "date": $("#date").val(),
                    "hour": $("#hr2").val(),
                    "minute": $("#min2").val()
                }
            }),
            success: function (data) {
                records = data.records;
                snackbarMessage("getData!");
            }
        });

    }

    // initial chart
    function initChart() {

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
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 100
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
            	// This switches the class names...
    			var className = $('#chart').attr('class');
    			var newClassName = className === 'epoch category10' ? 'styles2' : 'epoch category10';
    			$('#chart').removeClass(className)
    			$('#chart').addClass(newClassName);
                    
                $('#chart').push(dtPoints[j]);
                chart.redraw();

            }, delayMillis);

            var className = $('#chart').attr('class');
			var newClassName = className === 'styles1' ? 'epoch category10' : 'styles1';
			$('#chart').removeClass(className)
			$('#chart').addClass(newClassName);
            chart.redraw();
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
