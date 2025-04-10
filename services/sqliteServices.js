const sqlite = require('sqlite3').verbose();


let db;
//DB connection
async function startDB() {
    
    db = await new sqlite.Database('./db/database.db', (err)=>{
        if(err){
            console.error("Error while connceting Sqlite : ",err);
        }else{
            console.log("Sqlite database connected successfully");
        }
    })

}


//Creation of table
async function createTable(tableName,arg){
    await db.run(`CREATE TABLE IF NOT EXISTS ${tableName} (${arg})`, (err)=>{//note you have enter values as tableNmae="", arg="  dfjfkas TEXT, ..."
      if(err){
          console.error("Unable to create table : ", err)
      }else{
          console.log("Table created or already existed")
      }
  })
}



//PROBLEM: Not able to enter the number of ? in Values(???)
async function insertTable(tableName, rowName, values){
    const insert = `INSERT INTO ${tableName}(${rowName}) VALUES (?,?)`;//Problem above mentioned is in this line
    
    await db.run( insert, [`${values}`], (err)=>{
    if(err){
        console.error("Error while inserting values in sqlite: ",err);
    }else{
        console.log(`Row inserted Successfully`);
    }
})
}

async function selectTable(tableName) {
    
    const select = `SELECT * FROM ${tableName}`;
    await db.all(select, [], (err,rows)=>{
        if(err){
            console.error("Error while selecting : ", err)
        }
        
        rows.forEach((row)=>{
            console.log(`${row.id}: ${row.name} : ${row.address}`)
        });
    });
}

async function closeDB() {
    if(!db){
        throw new Error("DB not initialized!!");
    }
    
    db.close((err) => {
        if (err) {
            console.error("Error while closing the sqlite : ",err);
            throw err;
        }
        console.log('Closed the database connection.');
    });
}

module.exports = {startDB, createTable , insertTable , selectTable ,closeDB}




// async function closeDB() {
    
//     db.close((err) => {
//         if (err) {
//             console.error("Error while closing the sqlite : ",err);
//         }
//         console.log('Closed the database connection.');
//     });
// }
    