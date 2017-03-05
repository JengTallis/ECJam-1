"use strict";

$(function () {

    $("#dateInput").show();
    $("#chart").show();
    $("#add-student").hide();

<<<<<<< HEAD
    //var chart = $('#chart');
=======
    var records = [];
    var chart = $('#chart');

>>>>>>> end

    //initChart();
    //mock_Chart()
    // user click view
    $("#submitTime").click(function () {
<<<<<<< HEAD
        getChartData();
=======
        //getChartData();
        drawChart();
>>>>>>> end
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
                var records = data.records;
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
                "start": {
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

                var records = data.records;
                snackbarMessage("getData!");
                drawChart(records);
                alert(  JSON.stringify(records) );
                
            }
        });

    }

    // initial chart
    function initChart() {

        $('canvas').empty();
        
        var seed = Math.random()*1;
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
                    y: Math.random(seed)*100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: Math.random(seed)*100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: Math.random(seed)*100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: Math.random(seed)*100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: Math.random(seed)*100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: Math.random(seed)*100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: Math.random(seed)*100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 100
                }, {
                    time: Math.round(new Date().getTime() / 1000),
                    y: 50
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

        initChart();

        snackbarMessage("draw!");

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

    function drawChart(records) {
        snackbarMessage("draw!");
        var chart = $('#chart');
        // format data
        var dtPoints = [];
        console.log(records.length);
        for (var i = 0; i < records.length; i++) {

            //record string from server 
            var t_str = JSON.stringify(records[i]);

            //parse string to date type
            var year = t_str.slice(2, 6);
            var month = t_str.slice(7, 9);
            var day = t_str.slice(10, 12);
            var hours = t_str.slice(13, 15);
            var minutes = t_str.slice(16, 18);
            var seconds = t_str.slice(19, 20);

            //construct date object
            var d = new Date(year, month-1, day, hours, minutes, seconds, 10);
            console.log(d);
            //convert to long time format 
            var long_time = Math.round( d.getTime() / 1000 ); 
            
            //build a data point 
            var point = {
                time: Number(long_time),
                y: Number(records[i][1])
            };

            //push a point onto the array
            dtPoints.push(point);

        }

        console.log(dtPoints);
        // plot the chart
        var delayMillis = 10; //1 second
        mock_Chart(records, chart);


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
