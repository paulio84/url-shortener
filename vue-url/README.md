# UrlMe - Vue Frontend
The frontend for UrlMe. Built with Vue 3 and TypeScript using the composition API.

## Tech Stack
| Tool           | Purpose             |
| -------------- | ------------------- |
| Vue 3          | Framework           |
| TypeScript     | Language            |
| Vite           | Build tool          |
| Vue Router 4   | Client-side routing |
| Pinia          | State management    |
| Tailwind CSS   | Styling             |
| Heroicons      | Icons               |
| Vitest         | Test suite          |
| Vue Test Utils | Component testing   |

## Project Structure
```
src/
├── api/
│   ├── index.ts      # BASE_URL and shared utilities
│   ├── types.ts      # TypeScript interfaces for API responses
│   ├── auth.ts       # Auth API calls (register, login)
│   └── urls.ts       # URL API calls (fetch, shorten)
├── components/
│   ├── AuthCard.vue      # Shared card wrapper for auth pages
│   ├── FormField.vue     # Reusable labelled input with password toggle
│   ├── NavBar.vue        # Navigation bar with logout
│   ├── ShortenForm.vue   # URL shortening form
│   └── URLTable.vue      # Table of shortened URLs
├── pages/
│   ├── LoginPage.vue
│   ├── RegisterPage.vue
│   └── DashboardPage.vue
├── router/
│   └── index.ts      # Vue Router config with navigation guards
├── stores/
│   └── auth.ts       # Pinia auth store
├── App.vue           # Layout component
├── main.ts           # Entry point and setup
└── style.css         # Stylesheet (imports Tailwind CSS)
```

## Local Development

### Prerequisites
- Node.js v22
- The Flask API running locally

### Setup
1. Clone the repository:
```bash
git clone https://github.com/paulio84/url-shortener.git
cd url-shortener/vue-url
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.development`:
```bash
cp .env.development.example .env.development
```

4. Fill in the required value:
```
VITE_API_BASE_URL=http://localhost:5000
```

5. Start the development server:
```bash
npm run dev
```

The app will be available at `http://127.0.0.1:5173`.

## Running Tests
```bash
npm test
```

## Deployment
The frontend is deployed to [Vercel](https://vercel.com) and triggered automatically when changes to `vue-url/` are merged to `main`.

### Required environment variable on Vercel
```
VITE_API_BASE_URL=https://urlme.onrender.com
```
