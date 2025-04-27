// require("dotenv").config();
// const express = require("express");
// const apiRoutes = require("./routes/api");
// const { connectMQTT } = require("./services/mqttService");
// const { initializeRedis } = require("./services/redisService");

// const app = express();
// const PORT = process.env.PORT || 5000;

// app.use(express.json()); // Middleware to parse JSON requests
// app.use("/api", apiRoutes); // API routes

// // Start MQTT Connection
// connectMQTT();

// // Start Redis Connection
// initializeRedis();

// // Start Server
// app.listen(PORT, () => {
//   console.log(`🚀 Server running on http://localhost:${PORT}`);
// });


require("dotenv").config(); 
const express = require("express"); 
const apiRoutes = require("./routes/api"); 
const { connectMQTT } = require("./services/mqttService"); 
const { initializeRedis } = require("./services/redisService"); 
const dbRoutes = require("./routes/api")

//For Camera imports
const multer = require('multer');
const path = require('path');
const fs = require('fs');




const app = express(); 
const PORT = process.env.PORT || 5000;

//For camera config
const uploadDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadDir))
    fs.mkdirSync(uploadDir);

//Settingup multer

const storage = multer.diskStorage({
    destination: (req, file, cb) =>{
        res.send("Image Recieved");
    }
});

const upload = multer.diskStorage({
    destination: (req, file , cb) => {
        cb(null , "uploads/")
        // res.send("Image Uploaded")
    },
    filename: (req, file, cb) =>{
        cb(null , Date.now() + ".jpg")
    }
})

const mainUpload = multer({
    upload: upload
})


// Middleware to parse JSON requests
app.use(express.json()); 

// ✅ Default Route (Fix for "Cannot GET /")
app.get("/", (req, res) => {
    res.send("Server is running...");
});

//Serving the latest image

app.get('/live',(req,res) => {
    res.send(`
        <html>
            <body>
                <h2>Live Feed</h2>
                <img src="/latest.jpg" width="400"/>
                <script>
                    setInterval(()=>{
                        document.queryselector('img').src='./latest.jpg?t=' + new Date().getTime();    
                    }, 1000); //reload every second    
                </script>
            </body>
        </html>
    `);
});


//Serve the image statically
app.use('/latest.jpg', express.static(path.join(__dirname, 'uploads', 'latest.jpg')));

//Upload 
app.post("/upload",mainUpload.single(), (req,res) => {
    console.log("Upload url hitted!!")

    console.log("Image recived in Upload url", res.file)

    console.log("Upload successful!!!")
})

app.use("/_", express.static(path.join(__dirname,"temp", "_")))

// ✅ API Routes 
app.use("/api", apiRoutes);  
app.use("/db", dbRoutes)

// Start MQTT Connection 
connectMQTT(); 

// Start Redis Connection 
initializeRedis(); 

// Start Server 
app.listen(PORT, () => { 
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
