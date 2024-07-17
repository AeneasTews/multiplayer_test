import { WebSocketServer } from "ws";
import express from "express";
import { fileURLToPath } from 'url';
import path from 'path';
import * as bodyParser from "express";
import {get_user, create_user, close} from "./scripts/database.js";

// Initialization
const ws_port = 8080;
const http_port = 3000;

// Setup for path
const __filename = fileURLToPath(import.meta.url); // get the resolved path to the file
const __dirname = path.dirname(__filename); // get the name of the directory

// Web Socket Setup
const wss = new WebSocketServer({ port: ws_port });
const users = [];

wss.on("connection", (ws) => {
  ws.on("message", async (data) => {
    data = JSON.parse(data);
    console.log("received: %s", data);

    if (data.action === 'login') {
      if ((await get_user(data.data.username)).passwd_hash === data.data.passwd_hash) {
        const response = {result: 'success'};
        ws.send(JSON.stringify(response));
        // TODO: add every new connection to a list or dictionary or something
        users.push({ws: [0, 0, 0, data.data.car]});
      } else {
        const response = {result: 'failed'};
        ws.send(JSON.stringify(response));
        ws.close();
      }
    }

    if (data.action === "update_position") {
      const response = {result: 'failed'};
      ws.send(JSON.stringify(response));
    }
  });
  // TODO: the server needs to receive data from all connected clients and then broadcast the data to all clients
});

// Application setup
const app = express();
app.use(bodyParser.urlencoded({ extended: false}));
app.use(bodyParser.json());

app.get("/", (req, res) => {
  res.sendFile("./src/index.html", {root: __dirname});
});

app.get("/script.js", (req, res) => {
  res.sendFile("./src/script.js", {root: __dirname});
});

app.post("/create_user", async (req, res) => {
  const req_data = req.body;
  if (await get_user(req_data.username)) {
    res.json({
      "status": "username already taken",
    });
  } else {
    if (await create_user(req_data.username, req_data.passwd_hash) === "success") {
      console.log(`Successfully created user ${req_data.username}:${req_data.passwd_hash}`);
      res.json({
        "status": "success",
      });
    } else {
      console.log(`Error occurred whilst trying to create ${req_data}`);
      res.json({
        "status": "internal error occurred, please try again"
      });
    }
  }
});

app.post("/login", async (req, res) => {
  const req_data = req.body;
  if ((await get_user(req_data.username)).passwd_hash === req_data.passwd_hash) {
    res.json({
      "status": "success"
    });
  } else {
    res.json({
      "status": "failed"
    });
  }
});

const server = app.listen(http_port, async () => {
  console.log(`HTTP server listening on port ${http_port}`);
  console.log(`Websocket server listening on port ${ws_port}`);
});

process.on("SIGTERM", async () => {
  await close();
  server.close()
  console.log("Server closed");

  process.exit(0);
});

process.on("SIGINT", async () => {
  await close();
  server.close()
  console.log("Server closed");

  process.exit(0);
});