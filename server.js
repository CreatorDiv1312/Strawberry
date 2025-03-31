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

const app = express(); 
const PORT = process.env.PORT || 5000;

// Middleware to parse JSON requests
app.use(express.json()); 

// ✅ Default Route (Fix for "Cannot GET /")
app.get("/", (req, res) => {
    res.send("Server is running...");
});

// ✅ API Routes 
app.use("/api", apiRoutes);  

// Start MQTT Connection 
connectMQTT(); 

// Start Redis Connection 
initializeRedis(); 

// Start Server 
app.listen(PORT, () => { 
    console.log(`🚀 Server running on http://localhost:${PORT}`);
});
