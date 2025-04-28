// const express = require("express");
// const router = express.Router();
// const { execPython } = require("../utils/execPython");
// const redisClient = require("../services/redisService");

// // API 1 : ESP32 Requests Execution 
// router.post("/execute", async(req, res) => {
//     try{
//         const { scriptname } = req.body

//         // Rate Limiting (Preventing too many requests here )
//         const rateLimitKey = `rate_limit:esp32`;
//         const isLimited = await redisClient.get(rateLimitKey);
//         if(isLimited){
//             return res.status(429).json({ message: "Too many requests. Try again later."});
//         }
//         redisClient.setex(rateLimitKey, 2, "1") // setting a 2 second limit key basically pipeline formation

//         //Execution of python script
//         const result = await execPython("./scripts/testscript.py");
//         return res.json({success: true, result})
//     }
//     catch(error){
//         return res.status(500).json({message: false, error: error.message});
//     }
// });

// //API 2: Backend Termination

// router.post("/shutdown", (req,res) => {
//     console.log("Backend shutting down...");
//     res.json({message:"Server shutting down...."});
//     process.exit();
// });

// module.exports = router;


const express = require("express");
const router = express.Router();
const { execPython } = require("../utils/execPython");
const { searchFile } = require("../utils/searchFile")
const { redisClient } = require("../services/redisService");
const { startDB, closeDB } = require("../services/sqliteServices");
const sendMail = require("../services/nodemailerService")
//  Test Route (Check if API is working)
router.get("/", (req, res) => {
    

    
    (async () => {
        try {
            await sendMail(
                'Server Started!!!',
                'This is to inform that the home api route "/api/" is successfully executed'
            );
            console.log('Email successfully sent!');
        } catch (error) {
            console.error('Failed to send email:', error);
        }
    })();

    res.send("✅ API is working...");
});

// API 1: ESP32 Requests Execution 

    router.post("/execute", async (req, res) => {
    try {
        const { scriptnames } = req.body || ['test0']; // Accept an array of script names
        if (!Array.isArray(scriptnames) || scriptnames.length === 0) {
            return res.status(400).json({ error: "Script names required as an array" });
        }

        const rateLimitKey = `rate_limit:esp32`;
        const isLimited = await redisClient.get(rateLimitKey);
        if (isLimited) {
            return res.status(429).json({ message: "Too many requests. Try again later." });
        }
        await redisClient.setEx(rateLimitKey, 2, "1");

        const results = [];
        for (const scriptname of scriptnames) {
            const path = await searchFile('./scripts' , `${scriptname}.py`)
            console.log(path)


            const result = await execPython(path);
            results.push({ script: scriptname, result });
        }

        return res.json({ success: true, results });
    } catch (error) {
        return res.status(500).json({ success: false, error: error.message });
    }
});


router.get("/start-db",async(req,res)=>{
    try{
        console.log("DB start route executed");
        await startDB();
        res.status(200).send("DB started successfully")
    } catch (err) {
        res.status(500).send("DB failed to start :", err.message)
    }

    
})
router.get("/close",async (req,res)=>{
    try{
        console.log("Close DB route hitted!!");
        await closeDB();
        res.status(200).send("DB closed successfully");
    } catch (err) {
        res.status(500).send("DB failed to close :", err)
    }
})



// ✅ API 2: Backend Termination
router.post("/shutdown", (req, res) => {

    (async () => {
        try {
            await sendMail(
                'Server Closed!!!',
                'This is to inform that the api route "/api/shutdown" is successfully executed \n See You Next Time!!!'
            );
            console.log('Email successfully sent!');
        } catch (error) {
            console.error('Failed to send email:', error);
        }
    


    console.log("Backend shutting down...");
    res.json({ message: "Server shutting down..." });
    process.exit();
})();
});

module.exports = router;
