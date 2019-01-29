function getIP()
{
	window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;   //compatibility for firefox and chrome
    var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};      
    pc.createDataChannel("");    //create a bogus data channel
    pc.createOffer(pc.setLocalDescription.bind(pc), noop);    // create offer and set local description
    pc.onicecandidate = function(ice){  //listen for candidate events
        if(!ice || !ice.candidate || !ice.candidate.candidate)  return;
        var myIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1];
        console.log('my IP: ', myIP);
        pc.onicecandidate = noop;
        return myIP;
    };

}

var internal_ip = getIP();
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
//AJAX request to backend
$(document).ready(function() {
    $.post("/track/internal/", {
        internal : internal_ip,
        csrfmiddlewaretoken: '{{ csrf_token }}'
    }, function(data){
        console.log(data);
        console.log("Internal", internal_ip);
    });
});
