// const { Client } = require("mqtt");
// const redis = require("redis")
// const redisClient = redis.createClient({
//     socket: {
//         host: '127.0.0.1',
//         port: 6379
//     }
// });

// redisClient.on("connect", ()=> console.log("Redis CONNECTED"));

// function initializeRedis() {
//     redisClient.connect();
// }

// module.exports = { initializeRedis, redisClient };

const redis = require("redis");

const redisClient = redis.createClient({
    socket: {
        host: "127.0.0.1",  // Redis host (default: localhost)
        port: 6379          // Redis default port
    }
});

// Event listeners for debugging and stability
redisClient.on("connect", () => console.log("✅ Redis CONNECTED!"));
redisClient.on("error", (err) => console.error("❌ Redis ERROR:", err));

async function initializeRedis() {
    try {
        await redisClient.connect();  // Explicitly connect to Redis
        console.log("🔄 Redis Client Connected Successfully.");
    } catch (error) {
        console.error("❌ Redis Connection Failed:", error);
    }
}

module.exports = { initializeRedis, redisClient };
