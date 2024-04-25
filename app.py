import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import (Session, sessionmaker)

from src.db.orm_models import Base, UserORM
from src.game import (ConnectionManager, Game, Player,
                      PlayerOptions, Room, RoomManager)

from src.db.db import DB
from src.models import CreateUserRequest, ErrorResponse
from src.errors import UserNotFoundError

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TIME_TO_THINK = 10

manager = ConnectionManager()
room_manager = RoomManager()

engine = create_engine(
    'postgresql+psycopg://postgres:qwerty@localhost/postgres', 
    echo=True,
    pool_size=5,
    max_overflow=10,
)

db = DB(engine)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    # Create player
    player = Player(ws=websocket, id=client_id)
    playing_room = None

    # Pick the room to attach player
    waiting_room = room_manager.get_waiting_room()
    if waiting_room is None:
        room = Room()
        room.add_player(player)
        room_manager.add_room(room)
        playing_room = room

        await websocket.send_text("Waiting for another player ...")
    else:
        playing_room = waiting_room
        
        playing_room.add_player(player)
        playing_room.game = Game()
        await playing_room.broadcast("Let's play!")

    try:
        while True:
            # task_countdown = asyncio.create_task(playing_room.countdown(TIME_TO_THINK))
            # task_choice = asyncio.create_task(websocket.receive_text())
            # choice, pending = await asyncio.wait([task_countdown, task_choice], return_when=asyncio.FIRST_COMPLETED)
            # for task in pending:
            #     task.cancel()

            choice = await websocket.receive_text()
            player.choice = PlayerOptions[choice]
            
            if playing_room.player1.choice is not None and playing_room.player2.choice is not None:
                # переписать
                playing_room.game.p1_option = playing_room.player1.choice
                playing_room.game.p2_option = playing_room.player2.choice
                result = playing_room.game.find_winner()

                # перенести в room manager?
                await playing_room.announce_result(result)

                

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await playing_room.send_message_to_another_player(player, "Waiting for another player ...")
        # remove user
        room_manager.remove_player(player.id)
        # оповестить другого игрока
     




@app.get("/rating")
async def rating():
    users_rated = db.get_rating()

    return JSONResponse(json.dumps(users_rated))

@app.post("/users/create")
async def create_user(request: CreateUserRequest):
    try:
        db.create_user(request.username, request.password)
        return JSONResponse('{}')
    except UserNotFoundError as e:
        return JSONResponse(json.dumps(e.message), status_code=400)


    
