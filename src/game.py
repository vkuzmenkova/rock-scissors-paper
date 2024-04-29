import asyncio
import uuid as pyuuid
from enum import Enum

from fastapi import WebSocket
from loguru import logger


class PlayerOptions(Enum):
    ROCK = 1
    SCISSORS = 2
    PAPER = 3


class GameStatus(Enum):
    WAITING = 0
    CREATED = 1
    IN_PROGRESS = 2
    FINISHED = 3


class Result(Enum):
    PLAYER1_WON = 1
    PLAYER2_WON = 2
    TIE = 3


BEAT_RULES = {
    # choices: winner option
    frozenset({PlayerOptions.ROCK, PlayerOptions.PAPER}): PlayerOptions.PAPER,
    frozenset({PlayerOptions.SCISSORS, PlayerOptions.PAPER}): PlayerOptions.SCISSORS,
    frozenset({PlayerOptions.ROCK, PlayerOptions.SCISSORS}): PlayerOptions.ROCK,
}


class Game:
    def __init__(self) -> None:
        self.p1_option = None
        self.p2_option = None
        self.status = GameStatus.CREATED

    def __find_win_option(self) -> PlayerOptions:
        return BEAT_RULES[frozenset({self.p1_option, self.p2_option})]
        
    def find_winner(self) -> Result:
        if self.p1_option == self.p2_option:
            return Result.TIE

        if self.__find_win_option() == self.p1_option:
            return Result.PLAYER1_WON
        
        return Result.PLAYER2_WON    


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class Player:
    choice: PlayerOptions
    
    def __init__(self, ws: WebSocket, id: str):
        self.websocket = ws
        self.id = id
        self.choice = None
        self.ready: bool = False

        logger.debug(f"Player #{id} created")


class Room:    
    def __init__(self):
        self.id: pyuuid.UUID = pyuuid.uuid4()
        self.player1: Player = None
        self.player2: Player = None
        self.game: Game = None
        
        logger.debug(f"Room #{self.id} created.")

    def is_empty(self) -> bool:
        return self.player1 is None and self.player2 is None
    
    def is_waiting(self) -> bool:
        return self.player1 is None or self.player2 is None and not self.is_empty()
    
    def add_player(self, player: Player):
        if self.is_empty():
            self.player1 = player
        else:
            self.player2 = player
        logger.debug(f"Player #{player.id} added to the room #{self.id}.")    

    def is_player_here(self, player_id: str) -> bool:
        return (self.player1 is not None and self.player1.id == player_id) or (self.player2 is not None and self.player2.id == player_id)

    def remove_player(self, player_id: str):
        if self.is_player_here(player_id):
            if self.player1.id == player_id:
                self.player1 = None
            else:
                self.player2 = None
            
            logger.debug(f"Player #{player_id} removed from the room #{self.id}.")
            return
    
    async def announce_result(self, result: Result):
        if result is Result.PLAYER1_WON:
            await self.player1.websocket.send_text(f"Other player: {self.game.p2_option.name}. You: {self.game.p1_option.name}. You win!")
            await self.player2.websocket.send_text(f"Other player: {self.game.p1_option.name}. You: {self.game.p2_option.name}.You lose!")
        elif result is Result.PLAYER2_WON:
            await self.player1.websocket.send_text(f"Other player: {self.game.p2_option.name}. You: {self.game.p1_option.name}.You lose!")
            await self.player2.websocket.send_text(f"Other player: {self.game.p1_option.name}. You: {self.game.p2_option.name}.You win!")
        else:
            await self.broadcast("It's a tie!")

        self.set_default()

    def set_default(self):
        self.player1.choice = None
        self.player2.choice = None
        self.player1.ready = False
        self.player2.ready = False
    
    def are_players_ready(self):
        return self.player1.ready and self.player2.ready
    
    async def countdown(self, seconds: int):
        while seconds > 0:
            await self.broadcast(f"{seconds} seconds left")
            await asyncio.sleep(1)
            seconds -= 1
        await self.broadcast("Time off!")
    
    async def send_message_to_another_player(self, sender: Player, message: str):
        if sender is self.player1 and self.player1 is not None and self.player2 is not None:
            await self.player2.websocket.send_text(message)
        
        if sender is self.player2 and self.player2 is not None and self.player1 is not None:
            await self.player1.websocket.send_text(message)
    
    async def broadcast(self, message: str):
        await self.player1.websocket.send_text(message) 
        await self.player2.websocket.send_text(message)


class RoomManager:
    def __init__(self):
        self.rooms: list[Room] = []

    def get_waiting_room(self) -> Room:
        for room in self.rooms:
            if room.is_waiting():
                return room
        
        return None
    
    def add_room(self, room: Room) -> None:
        self.rooms.append(room)

    def remove_player(self, player_id: int):
        for room in self.rooms:
            if room.is_player_here(player_id):
                room.remove_player(player_id)
                if room.is_empty():
                    self.remove_room(room)
                return
    
    def remove_room(self, room: Room):
        self.rooms.remove(room)
        logger.debug(f"Room #{room.id} removed.")
        
