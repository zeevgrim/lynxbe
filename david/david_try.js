const https = require('https')
const fs = require('fs');

const userData = [];
const usernamesList = ['zeev_grim'];
const dataFileName = 'data.json';
const apiKey = '4672ef20249ef72fd7de49d45fc11e6f';
let url = `https://viralinsight.co/api.php?api_key=${apiKey}&username=`

usernamesList.forEach(userName => {
  url = url.concat(userName);

  https.get(url, (res) => {
    res.setEncoding('utf8');
    res.on('data', (chunk) => {
      console.log(`Got the data for ${userName} from viralinsight`);
      const chunkJson = JSON.parse(chunk);
      const data = getDataFromFile(`${__dirname}/${dataFileName}`, userName);

      const newData = {
        date: chunkJson.last_check_date,
        followers: chunkJson.followers,
        following: chunkJson.following,
        avgEngagement: chunkJson.average_engagement_rate
      }
      data[userName].push(newData)
      
      fs.writeFileSync(dataFileName, JSON.stringify(data), 'utf8');

      console.log(`Finished writing the new data to the file.\nThe file now contains: ${data[userName].length} jsons of data for ${userName}`);
    });
  }).end();
});

function getDataFromFile(path, userName) {
  let json = {}
  let contents = fs.readFileSync(path, 'utf8');
  if (contents.length === 0) {
    return { [userName]: [] }
  } else {
    return JSON.parse(contents);
  }
}
