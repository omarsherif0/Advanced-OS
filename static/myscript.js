$(function () {
  $("#navbarToggle").blur(function (event) {
    var screenWidth = window.innerWidth;
    if (screenWidth < 768) {
      $("#collapsable-nav").collapse("hide");
    }
  });

  $("#navbarToggle").click(function (event) {
    $(event.target).focus();
  });
});

$("#plot-button").click(function () {
  console.log("Plot button clicked");
  var btn1 = document.getElementById("plot-button");
  btn1.disabled = true;

  var b = document.forms["myForm"]["bitstream-input"].value;
  var i = document.forms["myForm"]["initial-input"].value;

  if (b == "") {
    alert("Enter the Sequence of Request queue!");
    return false;
  }
  if (b != "" && i == "") {
    alert("Enter the value of Initial Cylinder!");
    return false;
  }

  var ini = parseInt(document.getElementById("initial-input").value);
  var final = parseInt(document.getElementById("final-input").value);
  var str = document.getElementById("bitstream-input").value;
  var dir = document.getElementById("direction").value;

  var inp = [],
    r2 = str.split(" "),
    r3;

  for (a1 = 0; a1 < r2.length; ++a1) {
    if (r2[a1] == "") {
      continue;
    }
    r3 = parseInt(r2[a1]);
    inp.push(r3);

    if (r3 > final || ini > final) {
      alert("Invalid Input: Final cylinder has to be Greater!");
      return;
    }
  }

  final = parseInt(final);
  ini = parseInt(ini);

  document.getElementById("canvas").style.visibility = "visible";
  setTimeout(function () {
    document.getElementById("canvas").style.visibility = "visible";
    myalgorithm(
      document.getElementById("algorithm").value,
      inp,
      ini,
      final,
      dir,
      "none"
    );
  }, 500);

  // Optionally adjust layout for smaller screens (similar to animate-button logic)
  if (window.matchMedia("(min-width: 1249px)").matches) {
    $(".container2").css("top", "800px");
  } else if (window.matchMedia("(min-width: 992px)").matches) {
    $(".container2").css("top", "1250px");
  } else if (window.matchMedia("(min-width: 768px)").matches) {
    $(".container2").css("top", "1500px");
  } else if (window.matchMedia("(min-width: 600px)").matches) {
    $(".container2").css("top", "1450px");
  } else {
    $(".container2").css("top", "1350px");
  }
});

$("#animate-button").click(function () {
  console.log("Animation button clicked");
  var btn1 = document.getElementById("animate-button");
  btn1.disabled = true;
  var b = document.forms["myForm"]["bitstream-input"].value;
  var i = document.forms["myForm"]["initial-input"].value;
  if (b == "") {
    alert("Enter the Sequence of Request queue!");
    return false;
  }
  if (b != "" && i == "") {
    alert("Enter the value of Initial Cylinder!");
    return false;
  }

  var ini = parseInt(document.getElementById("initial-input").value);
  var final = parseInt(document.getElementById("final-input").value);
  var str = document.getElementById("bitstream-input").value;
  var dir = document.getElementById("direction").value;

  var inp = [],
    r2 = str.split(" "),
    r3;
  for (a1 = 0; a1 < r2.length; ++a1) {
    if (r2[a1] == "") {
      continue;
    }
    r3 = parseInt(r2[a1]);
    inp.push(r3);

    if (r3 > parseInt(final) || parseInt(ini) > parseInt(final)) {
      alert("Invalid Input: Final cylinder has to be Greater!");
      return;
    }
  }

  final = parseInt(final);
  ini = parseInt(ini);

  if (
    $("div.left").hasClass("transform") &&
    window.matchMedia("(min-width: 1249px)").matches
  ) {
    $(".left").css("width", "30%");
    $(".left").css("margin", "30px");
    $("#plot-button").css("margin-left", "30px");
    $("#plot-button").css("margin-bottom", "5%");
    $("#animate-button").css("margin-bottom", "5%");
    $("#cmpr-button").css("margin-left", "25%");
    $(".container2").css("top", "800px");
    $(".container3").css("top", "1500px");

    setTimeout(function () {
      document.getElementById("canvas").style.visibility = "visible";
      cylinders = myalgorithm(
        document.getElementById("algorithm").value,
        inp,
        ini,
        final,
        dir,
        animation
      );
    }, 500);
    animation(cylinders);
  } else if (window.matchMedia("(min-width: 992px)").matches) {
    document.getElementById("canvas").style.visibility = "visible";
    cylinders = myalgorithm(
      document.getElementById("algorithm").value,
      inp,
      ini,
      final,
      dir,
      animation
    );
    $(".container2").css("top", "1250px");
    animation(cylinders);
  } else if (window.matchMedia("(min-width: 768px").matches) {
    document.getElementById("canvas").style.visibility = "visible";
    cylinders = myalgorithm(
      document.getElementById("algorithm").value,
      inp,
      ini,
      final,
      dir,
      animation
    );
    $(".container2").css("top", "1500px");
    animation(cylinders);
  } else if (window.matchMedia("(min-width: 600px").matches) {
    document.getElementById("canvas").style.visibility = "visible";
    cylinders = myalgorithm(
      document.getElementById("algorithm").value,
      inp,
      ini,
      final,
      dir,
      animation
    );
    $(".container2").css("top", "1450px");
    animation(cylinders);
  } else {
    document.getElementById("canvas").style.visibility = "visible";
    cylinders = myalgorithm(
      document.getElementById("algorithm").value,
      inp,
      ini,
      final,
      dir,
      animation
    );
    $(".container2").css("top", "1350px");
    animation(cylinders);
  }
});

/**** ANIMATION ****/

function myalgorithm(alg, inp, ini, final, dir, callback) {
  // Prepare the request data in the format your API expects
  const requestData = {
    algorithm: alg,
    requests: inp,
    initial: ini,
    final: final,
  };

  // Show loading indicator (optional)
  document.getElementById("am_alg_name").innerHTML = "Loading...";
  document.getElementById("am_alg_seek").innerHTML = "Calculating...";

  // Make API call to your Python backend
  fetch("/run-scheduling", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Process the response from your API
      const cylinders = data.cylinders; // This should be the sequence of disk positions
      const seekTime = data.seek_time;
      console.log("Seek Time:", seekTime);
      console.log("Cylinders:", cylinders);
      if (typeof callback === "function") {
        callback(cylinders); // 💡 call animation or plot or whatever
        document.getElementById("am_alg_name").innerHTML = alg.toUpperCase();
        document.getElementById("am_alg_seek").innerHTML =
          "Total head movements: " + seekTime;
      }
      return cylinders;

      // Update the displayed algorithm name and seek time
      document.getElementById("am_alg_name").innerHTML = alg.toUpperCase();
      document.getElementById("am_alg_seek").innerHTML =
        "Total head movements: " + seekTime;
    })
    .catch((error) => {
      console.error("Error fetching algorithm data:", error);
      document.getElementById("am_alg_name").innerHTML = "Error";
      document.getElementById("am_alg_seek").innerHTML =
        "Failed to run algorithm";
    });
}

function animation(cylinders) {
  console.log("cylinders:", cylinders);
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");

  var cx = 350;
  var cy = 320;
  var PI2 = Math.PI * 2;
  var radius = 0;
  var totRadius = 0;

  var circles = [];

  // Convert the cylinder sequence to the target format if needed
  const target = cylinders;
  var max = Math.max(...target);

  // Calculate scale factor if max value exceeds 30
  const scaleFactor = max > 30 ? max / 30 : 1;
  console.log("Scaling factor:", scaleFactor);

  addCircle(20, "black");

  for (i = 0; i < 30; i++) {
    addCircle(10, "#A79C9D");
  }

  var targetIndex = 1;

  function addCircle(lineWidth, color) {
    if (radius == 0) {
      radius = lineWidth / 2;
    } else {
      radius += lineWidth;
    }
    totRadius = radius + lineWidth / 2;
    circles.push({
      radius: radius,
      color: color,
      width: lineWidth,
    });
  }

  function drawCircle(circle, color) {
    ctx.beginPath();
    ctx.arc(cx, cy, circle.radius, 0, PI2);
    ctx.closePath();
    ctx.lineWidth = circle.width;
    ctx.strokeStyle = color;
    ctx.stroke();
  }

  function canvas_arrow(context, fromx, fromy, tox, toy) {
    var headlen = 5; // length of head in pixels
    var dx = tox - fromx;
    var dy = toy - fromy;
    var angle = Math.atan2(dy, dx);
    context.moveTo(fromx, fromy);
    context.lineTo(tox, toy);
    context.lineTo(
      tox - headlen * Math.cos(angle - Math.PI / 6),
      toy - headlen * Math.sin(angle - Math.PI / 6)
    );
    context.moveTo(tox, toy);
    context.lineTo(
      tox - headlen * Math.cos(angle + Math.PI / 6),
      toy - headlen * Math.sin(angle + Math.PI / 6)
    );
  }

  var fps = 1;
  let request;
  var sik = "Seek-Time: ";
  function animate() {
    setTimeout(function () {
      request = requestAnimationFrame(animate);

      // Drawing code goes here
      if (targetIndex < target.length && targetIndex > 0) {
        sik =
          sik +
          "|" +
          target[targetIndex].toString() +
          "-" +
          target[targetIndex - 1].toString() +
          "|";
        document.getElementById("cl-seek").innerHTML = sik;
        sik = sik + "+";
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (var i = 0; i < circles.length; i++) {
        var circle = circles[i];
        var color = circle.color;
        drawCircle(circles[i], color);
      }

      for (var i = 0; i < circles.length; i++) {
        var circle = circles[i];
        var color = circle.color;

        // Scale the previous target value
        var prevTargetScaled = Math.min(
          Math.round(target[targetIndex - 1] / scaleFactor),
          30
        );
        var p_circle = circles[prevTargetScaled];

        // Scale the current target value
        var currentTargetScaled = Math.min(
          Math.round(target[targetIndex] / scaleFactor),
          30
        );

        if (i == currentTargetScaled) {
          color = "white";
          ctx.font = "10px Arial";
          ctx.fillStyle = "black";
          drawCircle(circles[i], color);

          ctx.font = "15px Arial";
          ctx.fillStyle = "darkblue";
          // Display actual value, not scaled value
          ctx.fillText(target[targetIndex], 350 + circle.radius, 310);
          ctx.fillStyle = "black";
          ctx.fillText(target[targetIndex - 1], 350 + p_circle.radius, 310);
          ctx.textAlign = "center";
          ctx.beginPath();
          canvas_arrow(
            ctx,
            350 + p_circle.radius,
            320,
            350 + circle.radius,
            320
          );
          ctx.strokeStyle = "black";
          ctx.lineWidth = 3;
          ctx.stroke();
        }
      }

      ctx.beginPath();
      ctx.arc(cx, cy, totRadius, 0, PI2);
      ctx.closePath();
      ctx.strokeStyle = "black";
      ctx.lineWidth = 5;
      ctx.stroke();

      targetIndex++;
      if (targetIndex == target.length) {
        cancelAnimationFrame(request);
        var btn = document.getElementById("animate-button");
        btn.disabled = false;
      }
    }, 3000);
  }

  animate();
}

function getBitStreamAndPlot(event, r1, ini, final, alg, side, b) {
  var i = document.forms["myForm"]["initial-input"].value;
  if (b == "") {
    alert("Enter the Sequence of Request queue!");
    return false;
  }
  if (i == "") {
    alert("Enter the value of Initial Cylinder!");
    return false;
  }

  var inp = [],
    r2 = r1.split(" "),
    r3;
  for (a1 = 0; a1 < r2.length; ++a1) {
    if (r2[a1] == "") {
      continue;
    }
    r3 = parseInt(r2[a1]);
    inp.push(r3);

    if (r3 > parseInt(final) || parseInt(ini) > parseInt(final)) {
      alert("Invalid Input: Final cylinder has to be Greater!");
      return;
    }
  }

  final = parseInt(final);
  ini = parseInt(ini);
  dir = side;

  // Show loading indicator
  document.getElementById("plt_alg_name").innerHTML = "Loading...";
  document.getElementById("cal-seek").innerHTML = "Calculating...";

  // Make API call to your Python backend
  fetch("/run-scheduling", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      algorithm: alg,
      requests: inp,
      initial: ini,
      final: final,
      direction: dir,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      // Process the response from your API
      const cylinders = data.cylinders; // This should be the sequence of disk positions
      const seekTime = data.seek_time;

      // Create the plot data
      var trace = {
        x: cylinders,
        y: Array.from({ length: cylinders.length }, (_, i) => i),
        type: "scatter",
        mode: "lines+markers",
        marker: { size: 10 },
      };

      var plotData = [trace];

      var layout = {
        xaxis: {
          autorange: true,
          showgrid: true,
          zeroline: false,
          showline: true,
          autotick: true,
          ticks: "",
          showticklabels: true,
          title: "Cylinder Number",
        },
        yaxis: {
          autorange: true,
          showgrid: false,
          zeroline: false,
          showline: false,
          autotick: true,
          ticks: "",
          showticklabels: false,
        },
        title: alg.toUpperCase() + " Disk Scheduling",
      };

      // Plot the graph
      Plotly.newPlot("graph_area", plotData, layout);

      // Calculate and display seek time
      var tot_seek = "Seek-Time: ";
      for (var i = 1; i < cylinders.length; i++) {
        tot_seek +=
          "|" +
          cylinders[i].toString() +
          "-" +
          cylinders[i - 1].toString() +
          "|";
        if (i < cylinders.length - 1) tot_seek += "+";
      }

      // Update UI with algorithm name and seek time
      document.getElementById("plt_alg_name").innerHTML = alg.toUpperCase();
      document.getElementById("cal-seek").innerHTML =
        tot_seek + " = " + seekTime;
      document.getElementById("graph_area").style.visibility = "visible";
    })
    .catch((error) => {
      console.error("Error fetching algorithm data:", error);
      document.getElementById("plt_alg_name").innerHTML = "Error";
      document.getElementById("cal-seek").innerHTML = "Failed to run algorithm";
    });
}

function cmprPlot(event, r1, ini, final, alg, side) {
  document.getElementById("cmpr-head").innerHTML = "Comparison-Chart";

  var b = document.forms["myForm"]["bitstream-input"].value;
  var i = document.forms["myForm"]["initial-input"].value;
  if (b == "") {
    alert("Enter the Sequence of Request queue!");
    return false;
  }
  if (b != "" && i == "") {
    alert("Enter the value of Initial Cylinder!");
    return false;
  }

  var ini = parseInt(document.getElementById("initial-input").value);
  var final = parseInt(document.getElementById("final-input").value);
  var str = document.getElementById("bitstream-input").value;
  var dir = document.getElementById("direction").value;

  var inp = [],
    r2 = str.split(" "),
    r3;
  for (a1 = 0; a1 < r2.length; ++a1) {
    if (r2[a1] == "") {
      continue;
    }
    r3 = parseInt(r2[a1]);
    inp.push(r3);

    if (r3 > parseInt(final) || parseInt(ini) > parseInt(final)) {
      alert("Invalid Input: Final cylinder has to be Greater!");
      return;
    }
  }

  final = parseInt(final);
  ini = parseInt(ini);

  var op1 = fcfs(inp, ini, final);
  var seek1 = op1[1];

  var op2 = sstf(inp, ini, final);
  var seek2 = op2[1];

  var op3 = scan(inp, ini, final, dir);
  var seek3 = op3[1];

  var op4 = cscan(inp, ini, final, dir);
  var seek4 = op4[1];

  var op5 = look(inp, ini, final, dir);
  var seek5 = op5[1];

  var op6 = clook(inp, ini, final, dir);
  var seek6 = op6[1];

  var data = [
    {
      x: ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"],
      y: [seek1, seek2, seek3, seek4, seek5, seek6],
      type: "bar",
    },
  ];

  Plotly.newPlot("cmpr_area", data);

  document.getElementById("cmpr_area").style.visibility = "visible";
}
