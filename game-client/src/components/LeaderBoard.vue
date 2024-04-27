<script setup>
import { ref } from 'vue'
import axios from 'axios'


defineProps({
  username: {
    type: String,
    required: true
  }
})
let users = ref([])

axios({
  method: 'get',
  url: 'http://127.0.0.1:8000/rating',
})
  .then(function (response) {
    users.value = JSON.parse(response.data)
    users.value = users.value.map(user=>JSON.parse(user))
    console.log(users)  
  })
  .catch(function (error) {
    console.log(error);
  })
  .finally(function () {
  });

</script>

<template>
  <p align="right">{{ username }}</p>
  <table align="center">
    <caption>
      Leader Board
    </caption>
    <thead>
      <tr>
        <th>#</th>
        <th scope="col">Username</th>
        <th scope="col">Total</th>
        <th scope="col">Wins</th>
        <th scope="col">Losses</th>
        <th scope="col">% of wins</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(user, index) in users" :class="{ bold: username === user.username}" >
        <td>{{index+1}}</td>
        <td>{{user.username}}</td>
        <td>{{user.total}}</td> 
        <td>{{user.wins}}</td>
        <td>{{user.total - user.wins}}</td>
        <td>{{!isNaN(user.wins/user.total * 100) ? user.wins/user.total * 100 : 0}}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.bold{
  font-weight: bold;
  background-color: pink;
}

table {
  table-layout: fixed;
  width: 100%;
  border-collapse: separate;
  border-spacing: 0px;
  border: 3px solid purple;
}
td {
  border: 1px solid black;
  text-align: center;
}

th {
  border: 1px solid black;
  font-weight: bold;
}




</style>
