import { describe, it, expect } from "vitest"
import { mount } from "@vue/test-utils"
import URLTable from "@/components/URLTable/URLTable.vue"
import type { ShortURL } from "@/api/types"

const mockURLs: ShortURL[] = [
  {
    id: 1,
    original_url: "https://example.com",
    short_code: "abc123",
    short_url: "/abc123",
    clicks: 5,
    created_at: "2026-03-16T10:00:00",
    user_id: 1,
  },
]

describe("URLTable", () => {
  it("shows loading state", () => {
    const wrapper = mount(URLTable, {
      props: { urls: [], loading: true },
    })
    const imgs = wrapper.findAll("img[alt='Loading...']")
    expect(imgs).toHaveLength(1)
  })

  it("shows empty state when no URLs", () => {
    const wrapper = mount(URLTable, {
      props: { urls: [], loading: false },
    })
    expect(wrapper.text()).toContain("No URLs yet")
  })

  it("renders a row for each URL", () => {
    const wrapper = mount(URLTable, {
      props: { urls: mockURLs, loading: false },
    })
    const rows = wrapper.findAll("tbody tr")
    expect(rows).toHaveLength(1)
  })

  it("displays the original URL", () => {
    const wrapper = mount(URLTable, {
      props: { urls: mockURLs, loading: false },
    })
    expect(wrapper.text()).toContain("https://example.com")
  })

  it("displays the click count", () => {
    const wrapper = mount(URLTable, {
      props: { urls: mockURLs, loading: false },
    })
    expect(wrapper.text()).toContain("5")
  })

  it("formats the date in British format", () => {
    const wrapper = mount(URLTable, {
      props: { urls: mockURLs, loading: false },
    })
    expect(wrapper.text()).toContain("16 Mar 2026")
  })
})