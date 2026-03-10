const mqtt = require('mqtt');
const { exec } = require('child_process');

const client = mqtt.connect('mqtt://127.0.0.1:1883');

client.on('connect', () => {
    console.log("Fog node connected");
    client.subscribe("hospital/vitals");
});

client.on('message', (topic, msg) => {

    const d = JSON.parse(msg.toString());

    const features = `${d.hr},${d.spo2},${d.temp},${d.acc_mag}`;

    exec(`node run-impulse.js "${features}"`, (err, stdout) => {
        if (err) return;

        console.log("Vitals:", features);
        console.log(stdout);
    });
});

