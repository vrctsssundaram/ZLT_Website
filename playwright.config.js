const { defineConfig } = require('@playwright/test');
module.exports = defineConfig({
  timeout: 35000,
  expect: { timeout: 7000 },
  use: { headless: true },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } }
  ]
});
