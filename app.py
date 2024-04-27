import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import (Session, sessionmaker)

from src.db.orm_models import Base, UserORM
from src.game import (ConnectionManager, Game, Player,
                      PlayerOptions, Room, RoomManager, GameStatus)

from src.db.db import DB
from src.models import CreateUserRequest
from src.errors import UserNotFoundError, UserAlreadyExists, WrongPassword
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

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


    try:
        while True:
            # If user already in a room
            if playing_room is not None and playing_room.is_player_here(player.id):
                pass
            else:
                # Find a vacant room and attach player
                waiting_room = room_manager.get_waiting_room()
                # If all rooms are nont vacant
                if waiting_room is None:
                    room = Room()
                    room.add_player(player)
                    room_manager.add_room(room)
                    playing_room = room
                    player.ready = True

                    await websocket.send_text(GameStatus.WAITING.name)
                # Attach user to the room
                else:
                    playing_room = waiting_room
                    
                    playing_room.add_player(player)
                    player.ready = True
                    playing_room.game = Game()
                    await playing_room.broadcast(GameStatus.CREATED.name)

            # Waiting for the choice if both are ready
            choice = await websocket.receive_text()

            if choice == "ONE_MORE":
                player.ready = True
                if playing_room.are_players_ready() is True:
                    await playing_room.broadcast(GameStatus.CREATED.name)
            else:
                player.choice = PlayerOptions[choice]
            
                if playing_room.player1.choice is not None and playing_room.player2.choice is not None:
                    playing_room.game.p1_option = playing_room.player1.choice
                    playing_room.game.p2_option = playing_room.player2.choice
                    result = playing_room.game.find_winner()

                    # перенести в room manager?
                    await playing_room.announce_result(result)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await playing_room.send_message_to_another_player(player, GameStatus.WAITING.name)
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
    except UserAlreadyExists as e:
        return JSONResponse(json.dumps(e.message), status_code=400)


@app.post("/auth/login")
async def login(request: CreateUserRequest):
    try:
        db.login(request.username, request.password)
        return JSONResponse('{}')
    except UserNotFoundError as e:
        return JSONResponse(json.dumps(e.message), status_code=400)
    except WrongPassword as e: 
        return JSONResponse(json.dumps(e.message), status_code=401)
    
