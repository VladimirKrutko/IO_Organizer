from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect('chat.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            server TEXT,
            username TEXT,
            message TEXT
        )
        ''')

    def add_message(self, server, username, message):
        self.cursor.execute('''
            INSERT INTO messages (server, username, message)
            VALUES (?, ?, ?)
        ''', (server, username, message))
        self.conn.commit()

    def get_last_messages(self, server, count=25):
        self.cursor.execute('''
            SELECT *
            FROM messages
            WHERE server = ?
            ORDER BY id DESC
            LIMIT ?
        ''', (server, count))
        return self.cursor.fetchall()[::-1]

    def get_messages_before(self, server, message_id, count=25):
        self.cursor.execute('''
            SELECT *
            FROM messages
            WHERE id < ? AND server = ?
            ORDER BY id DESC
            LIMIT 25
        ''', (message_id, server))
        return self.cursor.fetchall()

app = FastAPI()
db = Database()

@app.get("/{server}/{user}")
async def get_index(request: Request, server: str, user: str):
    base_url = str(request.base_url)
    stripped_protocol = base_url.split("//")[1]
    host = stripped_protocol.split("/")[0]
    
    template = open("./index.html", "r").read()
    rendered_template = template.replace("{{host}}", host) \
        .replace("{{server}}", server) \
        .replace("{{user}}", user)
    
    return HTMLResponse(rendered_template)

servers: dict[bytes, list[WebSocket]] = {}

async def send_message(to: WebSocket, user: str, message: str, end: bool = True):
    await to.send_json({
        "user": user, 
        "message": message, 
        "end": end
    })

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    server, user = websocket.headers.get("sec-websocket-protocol").split("|")

    if server not in servers:
        servers[server] = []
    servers[server].append(websocket)

    last = db.get_last_messages(server)
    for item in last:
        await send_message(websocket, *item[2:])
        
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "message":
                db.add_message(server, user, data["message"])
                for client in servers[server]:
                    await send_message(client, user, data["message"])
            else:
                for message in db.get_messages_before(server, data["message_id"]):
                    await send_message(websocket, *message[2:], False)
    except WebSocketDisconnect:
        servers[server].remove(websocket)
        await websocket.close()