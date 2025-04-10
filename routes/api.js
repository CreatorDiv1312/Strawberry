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
const { redisClient } = require("../services/redisService");
const { startDB, createTable , insertTable , selectTable ,closeDB } = require("../services/sqliteServices");
//  Test Route (Check if API is working)
router.get("/", (req, res) => {
    res.send("✅ API is working...");
});

// API 1: ESP32 Requests Execution 
router.post("/execute", async (req, res) => {
    try {
        const {scriptname} = req.body;

        // console.log(scriptname);
        // console.log(Object.keys(redisClient));

        if (!scriptname) return res.status(400).json({ error: "Script name required" });

        // Rate Limiting (Preventing too many requests here )
        const rateLimitKey = `rate_limit:esp32`;
        // const val = await redisClient.get(rateLimitKey);
        // if (val) {
        //     console.log("Value retrieved: ", val);
        // } else {
        //     console.log("Key does not exist!!");
        // }
        

        const isLimited = await redisClient.get(rateLimitKey);
        if (isLimited) {
            return res.status(429).json({ message: "Too many requests. Try again later." });
        }
        await redisClient.setEx(rateLimitKey, 2, "1"); // setting a 2-second limit key 

        // Execution of Python script
        const result = await execPython(`./scripts/${scriptname}.py`);
        return res.json({ success: true, result });
    } 
    catch (error) {
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
    console.log("Backend shutting down...");
    res.json({ message: "Server shutting down..." });
    process.exit();
});

module.exports = router;
