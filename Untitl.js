var fs = require('fs');

var lineReader = require('readline').createInterface({
    input: require('fs').createReadStream('user_list.txt')
});

let counter = 0;
let fullText = [];

lineReader.on('line', function (line) {
    if (!line.startsWith('@')) {
        counter++;
    } else {
        fullText.push(line.substring(1, line.length));
    }
});

var interval = setTimeout(() => { 
    console.log(fullText);

    var file = fs.createWriteStream('user_list_updated.txt');
    file.on('error', function(err) { /* error handling */ });
    fullText.forEach((line) => { 
        file.write(line + '\r\n');
     });
    file.end();

}, 1000);