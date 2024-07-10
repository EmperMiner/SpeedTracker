<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css')}}">
    <link rel="stylesheet" href="https://maxst.icons8.com/vue-static/landings/line-awesome/font-awesome-line-awesome/css/all.min.css" />
    <link rel="stylesheet" href="https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css" />
    <link href="https://fonts.cdnfonts.com/css/digital-numbers" rel="stylesheet">
    <link href='https://fonts.googleapis.com/css?family=Inter' rel='stylesheet'>
    <title>Vehicle</title>
</head>

<body>
    <div class="wrapper_vehicle shadow">
        <div class="info">
            <p>Vehicle: {{ vehicleName }}</p>
            <p>User code: {{ code }}</p>
            <p id="violation_count"></p>
        </div>
    
        <div class="speed-display">
            <p id="curSpeed" class="curSpeed">0</p>
            <p class="unit">km/h</p>
            <span class="speedLimit">
                <p class="limit">{{ speedLimit }}</p>
            </span>
        <div id="test"></div>
    </div>

        <a class="redirect_vehicle" href="{{ url_for('home') }}">Click here to Log out</a>
    </div>
</body>

<script>
    var violation_attempt = 0;
    const speed = {{speedArray|tojson}};
    var secondsLeft = 99, deltaSpeed, i = Math.floor(Math.random() * (speed.length - 100)), displayedSpeed=0;
    var timerId = setInterval(countdown, 1000);

    function countdown() {
        if (secondsLeft == 0) { 
            document.getElementById('test').textContent = "End of tracking"; 
            clearInterval(timerId);
        } else { 
            simulateTracking(); 
        }
    }

    function simulateTracking() {
        secondsLeft--;
        deltaSpeed = Math.round(Math.abs(speed[i] - Math.min(...speed)));
        attemptSpeed = Math.round(Math.abs(speed[i-1] - Math.min(...speed)));
        i++;
        //Refresh UI
        document.getElementById('curSpeed').textContent = deltaSpeed;
        if (deltaSpeed > {{speedLimit}}) {
            document.getElementById('test').textContent = "EXCEEDED";
            document.getElementById('curSpeed').style.color = 'red';
            if (attemptSpeed < {{speedLimit}}) {
                violation_attempt++;
            }
            document.getElementById('violation_count').textContent = "Violation count: " + violation_attempt;
        } else {  
            document.getElementById('test').textContent = "";
            document.getElementById('curSpeed').style.color = 'black';
            document.getElementById('violation_count').textContent = "Violation count: " + violation_attempt;
        }
    }
</script>

</html>
