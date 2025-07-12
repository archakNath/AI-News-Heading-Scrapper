const os = require('os');
const qrcode = require('qrcode-terminal');

// Find local IP
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    return 'localhost';
}

const localIP = getLocalIP();
const url = `http://${localIP}:3000`;

console.log(`\n🔗 Your local server URL: ${url}`);
console.log('📱 Scan the QR code below on your phone:\n');

qrcode.generate(url, { small: true });
