<template>
  <router-view />
</template>

<style>
:root {
  --app-bg: linear-gradient(180deg, #f7fbff 0%, #eef4ff 48%, #f9fbfd 100%);
  --panel-bg: rgba(255, 255, 255, 0.8);
  --panel-border: rgba(15, 23, 42, 0.08);
  --text-primary: #0f172a;
  --text-secondary: #5b6472;
  --text-tertiary: #7b8494;
  --accent: #2d6df6;
  --accent-soft: rgba(45, 109, 246, 0.12);
  --shadow-soft: 0 24px 60px rgba(148, 163, 184, 0.18);
  --radius-xl: 28px;
  --radius-lg: 20px;
}

* {
  box-sizing: border-box;
}

html,
body,
#app {
  min-height: 100%;
  margin: 0;
}

body {
  font-family: "SF Pro Display", "PingFang SC", "Microsoft YaHei", sans-serif;
  color: var(--text-primary);
  background: var(--app-bg);
}

body::before {
  content: "";
  position: fixed;
  inset: 0;
  background:
    radial-gradient(circle at top left, rgba(120, 192, 255, 0.34), transparent 28%),
    radial-gradient(circle at top right, rgba(158, 242, 225, 0.24), transparent 22%),
    radial-gradient(circle at bottom center, rgba(255, 255, 255, 0.9), transparent 26%);
  pointer-events: none;
}

.glass-panel {
  background: var(--panel-bg);
  backdrop-filter: blur(24px);
  border: 1px solid var(--panel-border);
  box-shadow: var(--shadow-soft);
}
</style>
