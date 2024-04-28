<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUsersStore } from '../store/users'

const usersStore = useUsersStore()
</script>

<template>
  <header class="header">
      <main>
        <RouterView />
      </main>
      <nav>
        <RouterLink to="/auth">Create user / Login</RouterLink>
        <RouterLink v-if="usersStore.isLoggedIn" to="/">Play</RouterLink>
        <RouterLink v-if="usersStore.isLoggedIn" to="/leaderboard">Leaderboard</RouterLink>
      </nav>
  </header>     
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

.header {
  display: flex;
  flex-direction: column;
}
</style>
