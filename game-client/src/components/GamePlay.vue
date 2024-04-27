<script setup>
import { ref } from 'vue'

defineProps({
  username: {
    type: String,
    required: true
  }
})

const clientID = Date.now() 
const ws = new WebSocket(`ws://localhost:8000/ws/${clientID}`);
const timer_sec = 10
const timer = ref(0)

let status = ref('')
let isTimerShown = ref(false)
let isChoicesShown = ref(false)
let isOneMoreShown = ref(false)
let timerId = ref()
let timeoutId = ref()

const areChoicesDisabled = ref(false)

ws.onmessage = function(event) {
  switch (event.data) {
    case "WAITING":
      status.value="Waiting for another player...";
      isChoicesShown.value = false
      isOneMoreShown.value = false
      isTimerShown.value = false
      break;
    case "CREATED":
      status.value="Let's play! Choose the option:";

      isChoicesShown.value = true
      areChoicesDisabled.value = false
      isOneMoreShown.value = false
      isTimerShown.value = true

      setTimer(timer_sec)
      break;
    default:
      // results
      status.value=event.data;

      isOneMoreShown.value = true
      isChoicesShown.value = true
      areChoicesDisabled.value = true
      isTimerShown.value = false

      clearTimeout(timeoutId.value)
  }  
};

function setNoResult() {
  isTimerShown.value = false
  isChoicesShown.value = false
  isOneMoreShown.value = true

  status.value="Other player and/or you did't make a choice :("
}

function setTimer(sec) {
  clearInterval(timerId.value)
  clearTimeout(timeoutId.value)

  timer.value = sec
  timerId.value = setInterval(() => {
      if (timer.value > 0) {
        timer.value--; // уменьшаем значение таймера каждую секунду
      } 
  }, 1000);

  timeoutId.value = setTimeout(() => {
    clearInterval(timerId.value);
    setNoResult();
  }, sec * 1000);
}


function sendRock(event) {
    const choice = "ROCK"
    ws.send(choice)
    status.value = "You've chosen " + choice

    areChoicesDisabled.value = true
}
function sendPaper(event) {
    const choice = "PAPER"
    ws.send(choice)
    status.value = "You've chosen " + choice

    areChoicesDisabled.value = true
}
function sendScissors(event) {
    const choice = "SCISSORS"
    ws.send(choice)
    status.value = "You've chosen " + choice

    areChoicesDisabled.value = true
}

function oneMore(event){
  ws.send("ONE_MORE")

  status.value="Waiting for another player...";
  isChoicesShown.value = false
  isOneMoreShown.value = false

  clearInterval(timerId.value)
}
</script>

<template>
  <p align="right">{{ username }}</p>
  <div align="center" class="status">{{ status }}</div>
    <div v-if="isChoicesShown" class="choices">
        <button :disabled=areChoicesDisabled id="rockButton" @click="sendRock"><img src="./icons/rock.svg" alt="Icon" class="icon">Rock</button>
        <button :disabled=areChoicesDisabled id="paperButton" @click="sendPaper"><img src="./icons/paper.svg" alt="Icon" class="icon">Paper</button>
        <button :disabled=areChoicesDisabled id="scissorsButton" @click="sendScissors"><img src="./icons/scissors.svg" alt="Icon" class="icon">Scissors</button>
    </div>
    <div v-if="isTimerShown" align="center" class="timer">{{ timer }}</div>
    <div align="center">
      <button v-if="isOneMoreShown" class="oneMore" @click="oneMore">One more round?</button>
    </div>      
</template>

<style scoped>
.status {
  font-weight: 500;
  font-size: 20;
  font-family: sans-serif;
  padding: 30px 30px;
}

.choices {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.oneMore{
  border: 3px solid black;
  border-style: groove;
  border-radius: 6px;
  background: white;
  color: black;
  padding: 8px 16px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  flex-direction: row;
}

h2 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

button {
  min-width: 100px;
  font-family: inherit;
  appearance: none;
  border: 0;
  border-radius: 5px;
  background: white;
  color: black;
  padding: 8px 16px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  text-align: center;
}

img {
  max-width: 150px;
  max-height: 150px;
  font-family: inherit;
  appearance: none;
  border: 1;
  border-radius: 5px;
  background: white;
  color: #fff;
  padding: 8px 16px;
  font-size: 12rem;
  cursor: pointer;
}
</style>
