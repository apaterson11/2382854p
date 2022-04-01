const socket = io.connect('localhost:3000');
const videoGrid = document.getElementById('video-grid')
const myPeer = new Peer(undefined, {
    host: '/',
    port: '3001'
  })
const myVideo = document.createElement('video')
myVideo.muted = true
const peers = {}
let timestamps = [];
let packetsLost = 0;
let lastPacketReceivedTimestamp = [];
let framesDropped = 0;
let estimatedPlayoutTimestamp = [];
printed=false;
totalDecodeTime = 0;
framesDecoded = 0;
framesReceived = 0;

var connections = myPeer.connections
// console.log(connections[0])

navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false
}).then(stream => {
    addVideoStream(myVideo, stream)

    myPeer.on('call', call => {
        call.answer(stream)
        const video = document.createElement('video')
        // console.log("answering to call")
        call.on('stream', userVideoStream => {
            addVideoStream(video, userVideoStream)
            // console.log("responding to user and sending back video")
        })
    })

    socket.on('user-connected', userId => {
        // console.log("other user connected")
        setTimeout(connectToNewUser,1000,userId,stream)
    })
})

socket.on('user-disconnected', userId => {
    if (peers[userId]) {
        // console.log("other user disconnected")
        peers[userId].close()
    }
})

myPeer.on('open', id => {
    socket.emit('join-room', ROOM_ID, id)
})

function connectToNewUser(userId, stream) {
    const call = myPeer.call(userId, stream)
    const video = document.createElement('video')
    // console.log("connectToNewUser called")
    media_stream = call.options._stream
    pc = call.peerConnection
    window.setInterval(function() {
        pc.getStats().then(stats => {
          let statsOutput = "";
      
          stats.forEach(report => {
            if (report.id.includes("RTCInboundRTPVideoStream"))  {
                // statsOutput += `<h2>Report: ${report.type}</h2>\n<strong>ID:</strong> ${report.id}<br>\n` +
                //            `<strong>Timestamp:</strong> ${report.timestamp}<br>\n`;
      
                // Now the statistics for this report; we intentionally drop the ones we
                // sorted to the top above
        
                Object.keys(report).forEach(statName => {
                    // if (statName !== "id" && statName !== "Timestamp" && statName !== "type" && (statName == "timestamp" || statName == "packetsLost" || statName == "packetsReceived"  || statName == "lastPacketReceivedTimestamp" || statName == "framesReceived" || statName == "framesDropped" || statName == "framesDecoded" || statName == "totalDecodeTime" || statName == "framesReceived")) {
                    //     statsOutput += `<strong>${statName}:</strong> ${report[statName]}<br>\n`;
                    // }
                    if ((statName == "packetsReceived") && report[statName] > 10000 && printed==false) {
                        printed=true;
                        console.log("result: " + report[statName] + "," + packetsLost);
                        // console.log(timestamps);
                        console.log("result: " + framesReceived + "," + framesDropped);
                        console.log("result: " + totalDecodeTime/framesDecoded)
                        // console.log(lastPacketReceivedTimestamp);
                        // console.log("result: " + estimatedPlayoutTimestamp);
                    }
                    // else if (statName == "timestamp") {
                    //     timestamps.push(report[statName]);
                    // }
                    else if (statName == "packetsLost") {
                        packetsLost = (report[statName]);
                    }
                    else if (statName == "lastPacketReceivedTimestamp") {
                        recentLastPacketReceivedTimestamp = report[statName];
                        lastPacketReceivedTimestamp.push(report[statName]);
                    }
                    else if (statName == "framesDropped") {
                        framesDropped = (report[statName]);
                    }
                    else if (statName == "framesReceived") {
                        framesReceived = (report[statName]);
                    }
                    else if (statName == "framesDecoded") {
                        framesDecoded = (report[statName]);
                    }
                    else if (statName == "totalDecodeTime") {
                        totalDecodeTime = report[statName];
                    }
                    else if (statName == "estimatedPlayoutTimestamp") {
                        fixed_value = (report[statName] / 100).toFixed(3);
                        estimatedPlayoutTimestamp.push([fixed_value, recentLastPacketReceivedTimestamp]);
                        // statsOutput += `<strong>${statName}:</strong> ${fixed_value}<br>\n`;
                    }
                });
            }
          });
      
          document.querySelector(".stats-box").innerHTML = statsOutput;
        });
      }, 1000);
    // pc.getStats(function callback(report) {
    //     var rtcStatsReports = report.result();
    //     for (var i=0; i<rtcStatsReports.length; i++) {
    //         var statNames = rtcStatsReports[i].names();

    //         var logs = "";
    //         for (var j=0; j<statNames.length; j++) {
    //             var statName = statNames[j];
    //             var statValue = rtcStatsReports[i].stat(statName);
    //             logs = logs + statName + ": " + statValue + ", ";
    //         }
    //         console.log(logs);
    //     }
    // });
    call.on('stream', userVideoStream => {
        addVideoStream(video, userVideoStream)
        // console.log("sending other user video stream")
    })
    call.on('close', () => {
        video.remove()
    })

    peers[userId] = call
    // console.log(peers)
    // console.log(peers.srcObject)
}

// once video is loaded on page, play video
function addVideoStream(video, stream) {
    video.srcObject = stream
    video.addEventListener('loadedmetadata', () => {
        video.play()
    })
    videoGrid.append(video)
}