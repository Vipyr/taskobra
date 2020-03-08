/*
    Dynamic Hostlist Rendering function
      Specializes the <template> in the home.html sheet
      https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template
*/
function render_hostlist(hostlist) {
  console.log( "taskobra.js: entered render_hostlist" );
  // Construct the instance of the template
  var template = document.querySelector('#taskobra-hostlist-entry');

  hostlist.forEach(host => {
    // Fill in the attrs of the instance
    var instance = template.content.cloneNode(true);
    instance.querySelector(".hostlist-name").textContent = host.hostname;
    instance.querySelector(".hostlist-status").textContent = host.status;
    instance.querySelector(".hostlist-uptime").textContent = host.uptime;
    instance.querySelector(".hostlist-misc").textContent = host.misc;

    // Add it to the content section 
    document.querySelector("#taskobra-hostlist-entries").appendChild(instance);
  });
}



// Hostlist setup
var hostlist = [
  { hostname: "one", status: "good", uptime: "FOREVER", misc: "---->" }, 
  { hostname: "too", status: "bad", uptime: "1h 64m 32s", misc: "---->" }, 
  { hostname: "Thr33", status: "ok", uptime: "0h 0m 1s", misc: "---->" }
]
render_hostlist(hostlist);


/* 
    Main Callback
      When document finishes loading in the client
*/
window.onload = (event) => {
  console.log( "taskobra.js: entered onload" );

};