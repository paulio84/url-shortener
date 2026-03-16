import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import LoginPage from "@/pages/LoginPage.vue"
import RegisterPage from "@/pages/RegisterPage.vue"
import DashboardPage from "@/pages/DashboardPage.vue"

const routes = [
  {
    path: "/login",
    component: LoginPage,
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    component: RegisterPage,
    meta: { requiresAuth: false },
  },
  {
    path: "/dashboard",
    component: DashboardPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/",
    redirect: "/dashboard",
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return "/login"
  }

  if (!to.meta.requiresAuth && auth.isAuthenticated && to.path !== "/") {
    return "/dashboard"
  }
})

export default router
