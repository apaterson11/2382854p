const express = require('express')
const app = express()
const server = require('http').Server(app)
const io = require('socket.io')(3000, {
    cors: {
        origins: ["http://localhost:4000","http://localhost:4001"],
        methods: ["GET", "POST"],
        allowedHeaders: ["my-custom-header"],
        credentials: true
    }
})
const { v4: uuidV4 } = require('uuid')

app.set('view engine', 'ejs')
app.use(express.static('public'))

// what happens when user joins room:
io.on('connection', socket => {
    socket.on('join-room', (roomId, userId) => {
        socket.join(roomId)
        socket.broadcast.to(roomId).emit('user-connected', userId)
        console.log("user joined")

        socket.on('disconnect', () => {
            socket.broadcast.to(roomId).emit('user-disconnected', userId)
            console.log("user disconnected")
        })
    })
})

// server.listen(3000)