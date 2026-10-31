# Jarvis frontend

Next.js / React / shadcn interface for the native Jarvis service. See the root README for setup and integration details.

```powershell
npm ci
npm run dev
```

Open http://127.0.0.1:3000. The Python service must run separately for chat, voice status and memory. The frontend uses Webpack for compatibility with this Windows environment.

```powershell
npm run build
npm run typecheck
```
