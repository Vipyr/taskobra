/*
    Dynamic Hostlist Rendering function
      Specializes the <template> in the home.html sheet
      https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template
*/
function render_systems(system_list) {
  console.log( "taskobra.js: entered render_hostlist" );
  // Construct the instance of the template
  var template = document.querySelector('#taskobra-hostlist-entry');
  system_list.forEach(host => {
    // Fill in the attrs of the instance
    var instance = template.content.cloneNode(true);
    instance.querySelector(".hostlist-checkbox").value = host.hostname;
    instance.querySelector(".hostlist-name").textContent = host.hostname;
    instance.querySelector(".hostlist-status").textContent = host.status;
    instance.querySelector(".hostlist-uptime").textContent = host.uptime;
    instance.querySelector(".hostlist-misc").textContent = host.misc;
    instance.querySelector("tr").addEventListener("click", function(event){
      var hostlist_checkbox = event.currentTarget.querySelector(".hostlist-checkbox");
      hostlist_checkbox.checked = !hostlist_checkbox.checked;
    }, false);

    // Add it to the content section 
    document.querySelector("#taskobra-hostlist-entries").appendChild(instance);
  });
}

/*
    Dynamic Chart rendering function
      Fills in the charts for each tabbed section 
      https://developers.google.com/chart/interactive/docs/quick_start
*/
function render_charts() {
  // TODO: Fill this in with real charts
  var data = google.visualization.arrayToDataTable([
    ['Year', 'Sales', 'Expenses'],
    ['2004',  1000,      400],
    ['2005',  1170,      460],
    ['2006',  660,       1120],
    ['2007',  1030,      540]
  ]);
  
  document.querySelectorAll(".taskobra-chart").forEach(chart => {

    var options = {
      title: 'Company Performance',
      curveType: 'function',
      width: 1200, height: 500,         // TODO: This will need to be reflexive obviously 
      legend: { position: 'bottom' }
    };

    console.log(chart);
    var chart = new google.visualization.LineChart(chart);

    chart.draw(data, options);

  });
}

/* 
    Main Callback
      When document finishes loading in the client
*/
window.onload = (event) => {
  console.log( "taskobra.js: entered onload" );

  // Hostlist setup
  $.ajax({url: "/api/systems", success: function(result) { 
    render_systems(JSON.parse(result));
  }});

  // Charting setup
  // Load the Visualization API and the corechart package.
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(render_charts);
};