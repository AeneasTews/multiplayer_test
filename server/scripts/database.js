import sqlite3 from "sqlite3";

const db = new sqlite3.Database("./user_db", sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
      console.error(err);
    }

    console.log("Database Connected");
});

db.serialize();

async function close() {
  db.close((err) => {
    if (err) {
      console.error(err);
    }
    console.log("Closed Database");
  });
}

async function create_user(username, passwd_hash) {
  return new Promise((resolve, reject) => {
    db.run(`insert into user_table(username, passwd_hash) values('${username}', '${passwd_hash}')`, (err) => {
      if (err) {
        console.error(err);
        reject(err);
      }

      console.log(`Inserted ${username}:${passwd_hash}`);
      resolve("success");
    });
  });
}

async function get_user(username) {
  return new Promise((resolve, reject) => {
    db.get(`select username, passwd_hash from user_table where username='${username}'`, (err, row) => {
      if (err) {
        console.error(err);
        reject(err);
      }

      resolve(row);
    });
  });
}

export {get_user, create_user, close};