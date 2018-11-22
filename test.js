var obj = require('./apidata.json');
var fs = require('fs');

// console.log(obj)

var request = require("request")

var url = "https://viralinsight.co/api.php?api_key=4672ef20249ef72fd7de49d45fc11e6f&username=zeev_grim"

request({
    url: url,
    json: true
}, function (error, response, body) {

    if (!error && response.statusCode === 200) {
        // console.log(body) // Print the json response
      }   

      var obj1 = Object.assign(obj, request);
      console.log(obj1); // { a: 1, b: 2, c: 3 }
      console.log(obj);  // { a: 1, b: 2, c: 3 }, target object itself is changed
    
// fs.writeFile('myjsonfile.json', newObject);
fs.writeFile('writeMe8.json', obj1, function(err, result) {
  if(err) console.log('error', err);
});
    

  });
  


