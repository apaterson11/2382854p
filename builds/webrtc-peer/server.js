const express = require('express')
const app = express()
const server = require('http').Server(app)
// const peer = require('peerjs')
const io = require('socket.io')(server)
// app.use('/peerjs', require('peer').ExpressPeerServer(srv, {
// 	debug: true
// }))
const { v4: uuidV4 } = require('uuid')

app.set('view engine', 'ejs')
app.use(express.static('public'))

app.use(express.static('views'))

// gets unique room ID
app.get('/', (req, res) => {
    res.redirect(`/${uuidV4()}`)
})

app.get('/:room', (req, res) => {
    res.render('room', { roomId: req.params.room })
})

server.listen(4000)