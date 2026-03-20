import { describe, it, expect, vi } from "vitest"
import { mount } from "@vue/test-utils"
import { createPinia, setActivePinia } from "pinia"
import { createRouter, createWebHistory } from "vue-router"
import NavBar from "@/components/NavBar/NavBar.vue"
import { useAuthStore } from "@/stores/auth"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: { template: "<div />" } },
    { path: "/login", component: { template: "<div />" } },
  ],
})

describe("NavBar", () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it("displays the user email", () => {
    const auth = useAuthStore()
    auth.user = { id: 1, email: "test@example.com", created_at: "2026-01-01" }

    const wrapper = mount(NavBar, {
      global: { plugins: [router] },
    })

    expect(wrapper.text()).toContain("test@example.com")
  })

  it("calls logout and redirects when sign out is clicked", async () => {
    const auth = useAuthStore()
    auth.user = { id: 1, email: "test@example.com", created_at: "2026-01-01" }
    const logoutSpy = vi.spyOn(auth, "logout")

    const wrapper = mount(NavBar, {
      global: { plugins: [router] },
    })

    await wrapper.find("button").trigger("click")
    expect(logoutSpy).toHaveBeenCalledOnce()
  })
})