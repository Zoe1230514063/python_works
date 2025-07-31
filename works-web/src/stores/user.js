import { defineStore } from 'pinia'
export const useUserStore = defineStore('user', {
  state: () => ({ token: localStorage.getItem('token') || '' }),
  actions: {
    setToken(t) { this.token = t; localStorage.setItem('token', t) }
  }
})
