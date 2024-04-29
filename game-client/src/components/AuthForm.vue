<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useUsersStore } from '../../store/users'

const usersStore = useUsersStore()
const message=ref('')
const password=ref('')

function createUser(event) {
  if (usersStore.userName && password.value){
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/users/create',
      data: {
        username: usersStore.userName.toLowerCase(),
        password: password.value,
      },
    })
      .then(function (response) {
        message.value = `User "${usersStore.userName}" created`
      })
      .catch(function (error, response) {
        message.value = error.response.data;
    })
  } 
}

function login(event) {
  if (usersStore.userName && password.value){
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/auth/login',
      data: {
        username: usersStore.userName.toLowerCase(),
        password: password.value,
      },
    })
      .then(function (response) {
        message.value = `You logged in as "${usersStore.userName}"`
        usersStore.setIsLoggedIn(true)
      })
      .catch(function (error, response) {
        message.value = error.response.data;
    })
  } 
}

const handleChange = (event) => {
  usersStore.setUserName(event.target.value);
};

</script>

<template>
<div class="authForm">
  <p v-if="usersStore.isLoggedIn" align="right">{{ usersStore.userName }}
  </p>
  <div class="container">
    <form @submit.prevent="onSubmit">
      <div class="form-group">
        <label>Username:</label>
        <input @input="handleChange" placeholder="username" required>
      </div>
      <div class="form-group">
        <label>Password:</label>
        <input v-model="password" placeholder="password" required>
      </div>
      <button type="submit" @click="createUser">Create user</button>
      <p align="center">or</p>
      <button type="submit" @click="login">Login</button>
    </form>
    <p>{{ message }}</p>
  </div>
</div>
</template>


<style scoped>
.authForm {
  min-width: 500px;
}
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
