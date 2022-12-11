from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

import sqlite3


conn = sqlite3.connect('chat.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    server TEXT,
    username TEXT,
    message TEXT
)
''')


def add_message(server, username, message):
    cursor.execute('''
        INSERT INTO messages (server, username, message)
        VALUES (?, ?, ?)
    ''', (server, username, message))
    conn.commit()

def get_last_messages(server, count=25):
    # Fetch the last count messages from the messages table
    cursor.execute('''
        SELECT *
        FROM messages
        WHERE server = ?
        ORDER BY id DESC
        LIMIT ?
    ''', (server, count))
    return cursor.fetchall()[::-1]

def get_messages_before(server, message_id, count=25):
    cursor.execute('''
        SELECT *
        FROM messages
        WHERE id < ? AND server = ?
        ORDER BY id DESC
        LIMIT 25
    ''', (message_id, server))
    return cursor.fetchall()

app = FastAPI()

@app.get("/")
async def get_index():
    return HTMLResponse(open("./index.html", "r").read())

subprotocols: dict[bytes, list[WebSocket]] = {}

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    subprotocol = websocket.headers.get("sec-websocket-protocol")
    if subprotocol is None:
        subprotocol = "default"

    if subprotocol not in subprotocols:
        subprotocols[subprotocol] = []
    subprotocols[subprotocol].append(websocket)

    last = get_last_messages(subprotocol)
    print(last)
    for item in last:
        await websocket.send_json({"user": item[2], "message": item[3], "end": True})

    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == "message":
                for client in subprotocols[subprotocol]:
                    add_message(subprotocol, str(websocket.client), data["message"])
                    await client.send_json({"user": str(websocket.client), "message": data["message"], "end": True})
            else:
                for message in get_messages_before(subprotocol, data["message_id"]):
                    await websocket.send_json({"user": message[2], "message": message[3], "end": False})
    except WebSocketDisconnect:
        subprotocols[subprotocol].remove(websocket)
        await websocket.close()