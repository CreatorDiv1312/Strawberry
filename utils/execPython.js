// const { exec } = require("child_process");
// const { stdout, stderr } = require("process");

// function execPython(scriptName){
//     return new Promise((resolve, reject)=>{
//         exec(`python3 scripts/${scriptName}`, (error, stdout, stderr)=>{
//             if(error){
//                 return reject(`Execution Error: ${stderr}`);
//             }
//             resolve(stdout.trim());
//         });
//     });
// }

// module.exports = { execPython }


const { exec } = require("child_process");

function execPython(scriptPath) {
    return new Promise((resolve, reject) => {
        console.log(`🚀 Running Python script: ${scriptPath}`); // ✅ Log script execution

        exec(`python ${scriptPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`❌ Error: ${error.message}`);
                return reject(error.message);
            }
            if (stderr) {
                console.error(`⚠️ Stderr: ${stderr}`);
            }
            console.log(`✅ Output: ${stdout}`); // ✅ Log script output
            resolve(stdout);
        });
    });
}

module.exports = { execPython };
