<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// Main app component with router view
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #0a0a0a;
  color: #ffffff;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #1a1a2e;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(45deg, #00ffff, #ff00ff);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(45deg, #ff00ff, #00ffff);
}

/* Selection */
::selection {
  background: rgba(0, 255, 255, 0.3);
  color: #ffffff;
}

::-moz-selection {
  background: rgba(0, 255, 255, 0.3);
  color: #ffffff;
}
</style>
