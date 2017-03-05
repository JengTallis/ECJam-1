"use strict";

$(function () {

    $("#dateInput").show();
    $("#chart").show();
    $("#add-student").hide();

    var records = [];
    var chart = $('#chart');


    // user click view
    $("#submitTime").click(function () {
        //getChartData();
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

                records = data.records;
                snackbarMessage("getData!");

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

        // format data
        var dtPoints = [];
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
            var d = new Date(year, month, day, hours, minutes, seconds, 10);
            
            //convert to long time format 
            var long_time = Math.round( d.getTime() / 1000 ); 
            
            //alert("long time: " + long_time);

            //build a data point 
            var point = {
                time: long_time,
                y: records[i][1]
            };

            //push a point onto the array
            dtPoints.push(point);
        }

        // plot the chart
        var delayMillis = 10; //1 second

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

            // This switches the class names...
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
