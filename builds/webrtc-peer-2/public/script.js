// const socket = io.connect('localhost:3000');
// const videoGrid = document.getElementById('video-grid')
// const myPeer = new Peer(undefined, {
//     host: '/',
//     port: '3001'
//   })
const socket = io.connect('http://10.0.0.4:3000');
const videoGrid = document.getElementById('video-grid')
const myPeer = new Peer(undefined, {
    host: '10.0.0.3',
    port: '3001'
  })
const myVideo = document.createElement('video')
myVideo.muted = true
const peers = {}
navigator.mediaDevices.getUserMedia({
    video: true,
    audio: false
}).then(stream => {
    addVideoStream(myVideo, stream)

    myPeer.on('call', call => {
        call.answer(stream)
        const video = document.createElement('video')
        console.log("answering to call")
        call.on('stream', userVideoStream => {
            addVideoStream(video, userVideoStream)
            console.log("responding to user and sending back video")
        })
    })

    socket.on('user-connected', userId => {
        console.log("other user connected")
        setTimeout(connectToNewUser,1000,userId,stream)
    })
})

socket.on('user-disconnected', userId => {
    if (peers[userId]) {
        console.log("other user disconnected")
        peers[userId].close()
    }
})

myPeer.on('open', id => {
    socket.emit('join-room', ROOM_ID, id)
})

function connectToNewUser(userId, stream) {
    const call = myPeer.call(userId, stream)
    const video = document.createElement('video')
    console.log("connectToNewUser called")
    console.log(call)
    call.on('stream', userVideoStream => {
        addVideoStream(video, userVideoStream)
        console.log("sending other user video stream")
    })
    call.on('close', () => {
        video.remove()
    })

    peers[userId] = call
}

// once video is loaded on page, play video
function addVideoStream(video, stream) {
    video.srcObject = stream
    video.addEventListener('loadedmetadata', () => {
        video.play()
    })
    videoGrid.append(video)
}