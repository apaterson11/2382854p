// console.log = function () { };
addToEventLog = function () { };

const WIDTH = 100;
const HEIGHT = 100;
let sentCount = 0;
let recvCount = 0;
let sentFramesCount = 0;
let recvFramesCount = 0;
const FRAMESIZE = WIDTH * HEIGHT * 4;
const HEADERSIZE = 16;
const connections = {};
var queue = [];
var frameNumber = 0;
let prevFrameNumber = 0;
let forgottenFrames = [];
let dict = {};
let prevSequenceNumber = -1;
let counter = 0;
let keys = null;
let prevValue = null;
let leftoverData = [];
let timestamps = [];
let printed_once = false;

const videoGrid = document.getElementById('video-grid');

{/* shows stats, unnecessary but could be useful for metric analysis */}
const showStats = () => {
    // document.querySelector('#stats').innerHTML = `QUIC Packets sent:${sentCount}\nQUIC Packets recv:${recvCount}\nFrames sent:${sentFramesCount}\nFrames recv:${recvFramesCount}\n`;
    // if (recvCount == 10000) {
    //     t2 = performance.now();
    //     console.log(`Receiving 1000 datagrams took ${t2 - t1} milliseconds.`);
    // }
};

let currentTransport, streamNumber, currentTransportDatagramWriter;

try {
    var transport = new WebTransport('https://web-platform.test:3000');
    addToEventLog('Initiating connection...');
} catch (e) {
    addToEventLog('Failed to create connection object. ' + e, 'error');
}

try {
    await transport.ready;
    addToEventLog('Connection ready.');
    currentTransport = transport;
    streamNumber = 1;
    try {
        currentTransportDatagramWriter = transport.datagrams.writable.getWriter();
        addToEventLog('Datagram writer ready.');
        startMedia();
    } catch (e) {
        addToEventLog('Sending datagrams not supported: ' + e, 'error');
    }
    //readDatagram(transport);
    //acceptUnidirectionalStreams(transport);
} catch (e) {
    addToEventLog('Connection failed. ' + e, 'error');
}

transport.closed
    .then(() => {
    // console.log("timestamps result: " + timestamps);
    addToEventLog('Connection closed normally.');
    })
    .catch(() => {
    // console.log("timestamps result: " + timestamps);
    addToEventLog('Connection closed abruptly.', 'error');
    });


// "Send data" button handler.
async function sendData(canvasContext, video, streamId, sequenceNumber, ts, stream, reader, writer) {
    let encoder = new TextEncoder('utf-8');
    // let rawData = sending.data.value;
    // let data = encoder.encode(rawData);
    let transport = currentTransport;
    let type = 'bidi';
    try {
      switch (type) {
        case 'bidi': {
          let number = streamNumber++;
          readFromIncomingStream(stream, 2, reader);

          canvasContext.drawImage(video, 0, 0);
          const imgData = canvasContext.getImageData(0, 0, WIDTH, HEIGHT);

          ts = Date.now();
          sentFramesCount ++;
          const frameNumber = sentFramesCount;
          showStats();
          let offset = 0;
          var frame_timestamps = [];
          timestamps.push(Date.now())
          //   timestamps.push(frame_timestamps);

          // sends stream
          while (printed_once == false) {
              let size = 1024;
              if (offset + size > imgData.data.length) {
                  size = imgData.data.length - offset;
              }
              // console.log("SENDING", size);
              await writer.ready;
              const chunk = imgData.data.slice(offset, offset + size);

              let writeBuffer = new Uint8ClampedArray(chunk.length);
              const dv = new DataView(writeBuffer.buffer, 0);
              writeBuffer.set(chunk, 0);
              // dv.setUint32(0, streamId);
              // dv.setUint32(4, sequenceNumber);  // can we get rid of these?
              // dv.setUint32(8, offset + size >= imgData.data.length ? 1 : 0); // does the third parameter count as undefined? are we sending as big or little endian?
              // dv.setUint32(12, frameNumber);

              await writer.write(dv);
            //   frame_timestamps.push(Date.now());
              
              //await writer.close();
              sequenceNumber++
              sentCount++;

            //   if (sentCount == 1000) {
            //     console.log("timestamps result: " + timestamps);
            //     printed_once = true
            //     await currentTransportDatagramWriter.close();
            //     // if (printed_once==false) {
            //     //     console.log(timestamps);
            //     //     printed_once=true;
            //     // }
            //     // writer.close();
            //     // break;
            //   }
              
              showStats();
              offset += size;
              if (offset >= imgData.data.length) {
                  break;
              }
          }
          
          // addToEventLog('Opened bidirectional stream #' + number);
          break;
        }
      }
    } catch (e) {
      addToEventLog('Error while sending data: ' + e, 'error');
    }
}

async function acceptUnidirectionalStreams(transport, reader) {
    //let reader = transport.incomingUnidirectionalStreams.getReader();
    try {
      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          addToEventLog('Done accepting unidirectional streams!');
          return;
        }
        let stream = value;
        let number = streamNumber++;
        addToEventLog('New incoming unidirectional stream #' + number);
        readFromIncomingStream(stream, number);
      }
    } catch (e) {
      addToEventLog('Error while accepting streams: ' + e, 'error');
    }
}
  
async function readFromIncomingStream(stream, number, reader) {
    let decoder = new TextDecoderStream('utf-8');
    // let reader = stream.pipeThrough(decoder).getReader();
    //let reader = stream.readable.getReader();
      while (true) {
        const { value, done } = await reader.read();
        //console.log(value);
        recvCount ++;
        if (done) {
          addToEventLog('Stream #' + number + ' closed');
          return;
        }
        //let data = value;
        const dv = new DataView(value.buffer);  
        const streamId = 1;
        // const sequenceNumber = dv.getUint32(4);
        // const eof = dv.getUint32(8);
        // const frameNumber = dv.getUint32(12);
        // console.log("receiving stream %s", streamId);
        // console.log("receiving eof %s", eof);
        let dataSize = value.length;

        if (!connections[streamId]) {
          document.querySelector('#logs').innerHTML += `User ${streamId} connected\n`;    // if user's ID is not already present, show as connected
          connections[streamId] = createRemoteView(streamId);                                   // create video feed       
        }

        if (connections[streamId].bufferOffset + dataSize > FRAMESIZE) {
        //   console.log("old data size: " + dataSize); 
          dataSize = FRAMESIZE - connections[streamId].bufferOffset; 
        //   console.log("new data size: " + dataSize); 
        }
        connections[streamId].buffer.set(value.slice(0, dataSize), connections[streamId].bufferOffset);
        connections[streamId].bufferOffset += dataSize;

        leftoverData = value.slice(dataSize, );

        // if (connections[streamId].bufferOffset + dataSize <= FRAMESIZE) {          // accounts for when data size is too big
        //   connections[streamId].buffer.set(value.slice(HEADERSIZE), connections[streamId].bufferOffset);
        //   connections[streamId].bufferOffset += dataSize;
        // }

        //console.log(frameNumber, sequenceNumber, connections[streamId].bufferOffset, dataSize, eof);     // eof and bufferOffset do not line up?
        // console.log(connections[streamId].bufferOffset, dataSize);

        if (connections[streamId].bufferOffset == FRAMESIZE) {
        //   (console.log("main render"))
          render(connections[streamId]);
        }

        if (leftoverData.length != 0) {
          dataSize = leftoverData.length;
          if (connections[streamId].bufferOffset + dataSize > FRAMESIZE) {
            // console.log("old data size: " + dataSize); 
            dataSize = FRAMESIZE - connections[streamId].bufferOffset; 
            // console.log("new data size: " + dataSize); 
          }
          connections[streamId].buffer.set(leftoverData.slice(0, dataSize), connections[streamId].bufferOffset);
          connections[streamId].bufferOffset += dataSize;
          leftoverData = [];
        }

          recvCount++;
          showStats();
        }  

        //addToEventLog('Received data on stream #' + number + ': ' + data);
}

const createRemoteView = (id) => {
    //console.log("creating remote view");
    const canvas = document.createElement('canvas');
    canvas.setAttribute("id", `remote_${id}`);
    canvas.width = WIDTH;
    canvas.height = HEIGHT;
    const context = canvas.getContext('2d');
    const buffer = new Uint8ClampedArray(FRAMESIZE);
    const bufferOffset = 0;
    videoGrid.appendChild(canvas);  
    return { canvas, context, buffer, bufferOffset };
};

{/* renders received media data */}
async function render(view){
    recvFramesCount++;
    // console.log("----------------- RENDER FRAME -----------------");
    view.context.putImageData(new ImageData(view.buffer, WIDTH, HEIGHT), 0, 0);
    view.bufferOffset = 0;
};
  
function addToEventLog(text, severity = 'info') {
    let log = document.getElementById('event-log');
    let mostRecentEntry = log.lastElementChild;
    let entry = document.createElement('li');
    entry.innerText = text;
    entry.className = 'log-' + severity;
    log.appendChild(entry);
  
    // If the most recent entry in the log was visible, scroll the log to the
    // newly added element.
    if (mostRecentEntry != null &&
        mostRecentEntry.getBoundingClientRect().top <
            log.getBoundingClientRect().bottom) {
      entry.scrollIntoView();
    }
}

async function startMedia() {
    const videoStream = await navigator.mediaDevices.getUserMedia({ video: {width: {exact: WIDTH}, height: {exact: HEIGHT}}, audio: false });
    const video = document.querySelector('#local'); 
    video.srcObject = videoStream;
    video.muted = true;
    video.play();

    const stream = await transport.createBidirectionalStream();
    const reader = stream.readable.getReader();
    const writer = stream.writable.getWriter();
    let streamId = 2; 
    var sequenceNumber = 0;
    let ts = Date.now();

    const canvasContext = document.createElement("canvas").getContext("2d");
    setInterval(async () => {
        sendData(canvasContext, video, streamId, sequenceNumber, ts, stream, reader, writer);
    }, 100);
};