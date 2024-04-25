<script setup>
import axios from 'axios'
import { ref } from 'vue'

const message=ref('')
const username=ref('')
const password=ref('')

function createUser(event) {
  if (username.value && password.value){
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/users/create',
      data: {
        username: username.value,
        password: password.value,
      },
    })
      .then(function (response) {
        console.log(response.data)
        message.value = `User "${username.value}" created`
      })
      .catch(function (error, response) {
        console.log(error);
        message.value = error.response.data;
    })
  } 
}
</script>


<template>
    <div class="container">
      <form @submit.prevent="onSubmit">
        <div class="form-group">
          <label>Username:</label>
          <input v-model="username" placeholder="username" required>
        </div>
        <div class="form-group">
          <label>Password:</label>
          <input v-model="password" placeholder="password" required>
        </div>
        <button type="submit" @click="createUser">Create user</button>
      </form>
      <p>{{ message }}</p>
    </div>
</template>

<style scoped>
.container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
