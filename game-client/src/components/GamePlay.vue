<script setup>
import { ref } from 'vue'
// defineProps({
//   id: {
//     type: Number,
//     required: true
//   }
// })

let status = ref('')

const clientID = Date.now() 
const ws = new WebSocket(`ws://localhost:8000/ws/${clientID}`);

ws.onmessage = function(event) {
    status.value = event.data

    if (status.value == "Let's play!"){
        setVisibility('choices', true)
    } 
};

function setVisibility(id, isVisible) {
    var div = document.getElementById(id);
    if (isVisible) {
        div.style.display = 'flex';
    } else {
        div.style.display = 'none';
    }
}

function setAvailability(id, isAvailable) {
    var div = document.getElementById(id);
    if (isAvailable) {
        div.disabled = false;
    } else {
        div.disabled = true;
    }
}

function sendChoice(event) {
    const choice = event.target.innerText.toUpperCase()
    ws.send(choice)
    status.value = "You've chosen " + choice

    setAvailability('choices', false)
}
</script>

<template>
    <h2>Your ID: <span id="ws-id">{{clientID}}</span></h2>

    <div id="choices" style="display: none;">
        <button id="rockButton" @click="sendChoice">Rock</button>
        <button id="paperButton" @click="sendChoice">Paper</button>
        <button id="scissorsButton" @click="sendChoice">Scissors</button>
    </div>       
    <div class="status">{{ status }}</div>
</template>

<style scoped>
.status {
  font-weight: 500;
  font-size: 16px;
  font-family: sans-serif;
  padding: 8px 16px;
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
  background: #4676d7;
  color: #fff;
  padding: 8px 16px;
  font-size: 1rem;
  cursor: pointer;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
