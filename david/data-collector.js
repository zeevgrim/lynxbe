const https = require('https');
const fs = require('fs');

const usernamesList = ['zeev_grim', 'grim_valerie'];
const dataFileName = 'data.json';
const apiKey = '4672ef20249ef72fd7de49d45fc11e6f';
let url = "";

usernamesList.forEach(userName => {
  url = `https://viralinsight.co/api.php?api_key=${apiKey}&username=${userName}`

  https.get(url, (res) => {
    res.setEncoding('utf8');
    res.on('data', (chunk) => {
      const chunkJson = JSON.parse(chunk);
      if (chunkJson.username === userName) {
        console.log(`Got the data for ${userName} from viralinsight`);
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
      } else { 
        console.log(`The request did not return any data for: ${userName}.\nError message: ${chunk}`);
      }
    });
  }).end();
});

function getDataFromFile(path, userName) {
  let json = {}
  let contents = fs.readFileSync(path, 'utf8');
  if (contents.length === 0) {
    return { [userName]: [] }
  } else {
    const fileData = JSON.parse(contents);
    if (!fileData[userName]) {
      fileData[userName] = []
    }
    
    return fileData;
  }
}
