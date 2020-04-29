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
  document.querySelectorAll(".taskobra-chart").forEach(chart => {
    if ($( chart ).parent('.active').length == 0) { return }
    var metric_type = chart.getAttribute('data-metric-type')
    $.ajax({url: "/api/metrics/" + metric_type, chart: chart, success: function(chart_data) {
      var labels = [ [ {label: 'Time', id: 'time'}, {label: 'Utilization', id: 'utilization', type: 'number'} ] ];
      var data = google.visualization.arrayToDataTable(
        labels.concat(chart_data)
      );

      var options = {
        curveType: 'function',
        width: $(window).width()*0.80, 
        height: $(window).height()*0.50, 
        chartArea: {'width': '90%', 'height': '80%'},
        legend: {position: 'none'}
      };

      var chart = new google.visualization.LineChart(this.chart);
      chart.draw(data, options);
    }})
  });
}

/* 
    Main Callback
      When document finishes loading in the client
*/
window.onload = (event) => {
  console.log( "taskobra.js: entered onload" );

  // Hostlist setup
  $.ajax({url: "/api/systems", success: render_systems});

  // Charting setup
  // Load the Visualization API and the corechart package.
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(render_charts);
  setInterval(render_charts, 1000);
};

/* 
    On Ready Callback
      After the load finishes
*/
$( document ).ready(function () {
  $('#v-pills-cpu-tab').tab('show')
})