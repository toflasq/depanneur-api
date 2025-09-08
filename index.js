const fs = require('fs');

const data = JSON.parse(fs.readFileSync('./data.json', 'utf-8'));

console.log("Nombre d'appareils :", data.length);
console.log("Premier appareil :", data[0].device, "-", data[0].scenario);
