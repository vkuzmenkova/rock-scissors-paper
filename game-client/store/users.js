import { defineStore } from 'pinia'

export const useUsersStore = defineStore('users', {
  state: () => {
    return {
      userName: '',
      isLoggedIn: false
    }
  },

  actions: {
    setUserName(newValue) {
      this.userName = newValue
    },
    setIsLoggedIn(newValue) {
      this.isLoggedIn = newValue
    },
  },
})