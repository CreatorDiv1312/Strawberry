// const { Client } = require("mqtt");
// const redis = require("redis")
// const client = redis.createClient({
//     socket: {
//         host: '127.0.0.1',
//         port: 6379
//     }
// });

// client.on("connect", ()=> console.log("Redis CONNECTED"));

// function initializeRedis() {
//     client.connect();
// }

// module.exports = { initializeRedis, client };

const redis = require("redis");

const client = redis.createClient({
    socket: {
        host: "127.0.0.1",  // Redis host (default: localhost)
        port: 6379          // Redis default port
    }
});

// Event listeners for debugging and stability
client.on("connect", () => console.log("✅ Redis CONNECTED!"));
client.on("error", (err) => console.error("❌ Redis ERROR:", err));

async function initializeRedis() {
    try {
        await client.connect();  // Explicitly connect to Redis
        console.log("🔄 Redis Client Connected Successfully.");
    } catch (error) {
        console.error("❌ Redis Connection Failed:", error);
    }
}

module.exports = { initializeRedis, client };
