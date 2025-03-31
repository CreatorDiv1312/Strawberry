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
const redisClient = require("../services/redisService");

//  Test Route (Check if API is working)
router.get("/", (req, res) => {
    res.send("✅ API is working...");
});

// API 1: ESP32 Requests Execution 
router.post("/execute", async (req, res) => {
    try {
        const { scriptname } = req.body;
        if (!scriptname) return res.status(400).json({ error: "Script name required" });

        // Rate Limiting (Preventing too many requests here )
        const rateLimitKey = `rate_limit:esp32`;
        const isLimited = await redisClient.get(rateLimitKey);
        if (isLimited) {
            return res.status(429).json({ message: "Too many requests. Try again later." });
        }
        redisClient.setex(rateLimitKey, 2, "1"); // setting a 2-second limit key 

        // Execution of Python script
        const result = await execPython(`./scripts/${scriptname}.py`);
        return res.json({ success: true, result });
    } 
    catch (error) {
        return res.status(500).json({ success: false, error: error.message });
    }
});

// ✅ API 2: Backend Termination
router.post("/shutdown", (req, res) => {
    console.log("Backend shutting down...");
    res.json({ message: "Server shutting down..." });
    process.exit();
});

module.exports = router;
