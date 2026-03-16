import { defineStore } from "pinia"
import { ref, computed } from "vue"
import type { User } from "@/types/api"

export const useAuthStore = defineStore("auth", () => {
  // -- State --
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem("accessToken"))

  // -- Getters --
  const isAuthenticated = computed(() => !!accessToken.value)

  // -- Actions -- 
  function login(token: string, refreshToken: string, loggedInUser: User) {
    accessToken.value = token
    user.value = loggedInUser
    localStorage.setItem("accessToken", token)
    localStorage.setItem("refreshToken", refreshToken)
    localStorage.setItem("user", JSON.stringify(loggedInUser))
  }

  function logout() {
    accessToken.value = null
    user.value = null
    localStorage.removeItem("accessToken")
    localStorage.removeItem("refreshToken")
    localStorage.removeItem("user")
  }

  return { user, accessToken, isAuthenticated, login, logout }
})
