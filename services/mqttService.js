const mqtt = require("mqtt");
const client = mqtt.connect("mqtt://localhost");

client.on("connect", ()=> console.log("MQTT Connected"));

function connectMQTT(){
    client.subscribe("esp32/execute");
    client.on("message", ()=> {
        console.log(`MQTT Message Recieved: ${message.toString()}`)
    });
}

module.exports = { connectMQTT };