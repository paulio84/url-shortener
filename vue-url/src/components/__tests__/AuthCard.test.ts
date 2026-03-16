import { describe, it, expect } from "vitest"
import { mount } from "@vue/test-utils"
import { createRouter, createWebHistory } from "vue-router"
import AuthCard from "@/components/AuthCard.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: "/", component: { template: "<div />" } }],
})

describe("AuthCard", () => {
  it("renders the title", async () => {
    const wrapper = mount(AuthCard, {
      global: {
        plugins: [router],
      },
      props: {
        title: "Sign in to UrlMe",
      },
      slots: {
        default: "<p>slot content</p>",
      },
    })

    expect(wrapper.text()).toContain("Sign in to UrlMe")
  })

  it("renders slot content", async () => {
    const wrapper = mount(AuthCard, {
      global: {
        plugins: [router],
      },
      props: {
        title: "Sign in to UrlMe",
      },
      slots: {
        default: "<p>slot content</p>",
      },
    })

    expect(wrapper.text()).toContain("slot content")
  })
})