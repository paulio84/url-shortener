import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/auth"

import LoginPage from "@/pages/LoginPage.vue"
import RegisterPage from "@/pages/RegisterPage.vue"
import DashboardPage from "@/pages/DashboardPage.vue"

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
    meta: { requiresAuth: false, title: "Login" },
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterPage,
    meta: { requiresAuth: false, title: "Register" },
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardPage,
    meta: { requiresAuth: true, title: "Dashboard" },
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
  // Update page title
  const title = `UrlMe | ${to.meta.title}`
  document.title = title

  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return "/login"
  }

  if (!to.meta.requiresAuth && auth.isAuthenticated && to.path !== "/") {
    return "/dashboard"
  }
})

export default router
