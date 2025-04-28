const fs = require("fs");
const path = require("path");

function searchFile(dir, fileName){
    const files= fs.readdirSync(dir);

    for(const file of files){
        const filePath = path.join(dir, file);
        const stat = fs. statSync(filePath);
        if (stat.isDirectory()){
            const found = searchFile(filePath, fileName);
            if(found) return found;
        }else if( file === fileName){
            return filePath;
        }
    }
    return null;
}

module.exports = { searchFile };

// const result = searchFile('../scripts', 'run_mod.py');

// if(result) {
//     console.log( ` File found at : ${result}`);
// }else{
//     console.log("File not found");
// }