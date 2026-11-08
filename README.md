# Kitchen Recipes app

An installable, offline-first web app with 218 recipes and 11 seven-day meal plans.
Once it has loaded once, everything (recipes, fonts, icons) is stored on the device and it opens with no internet connection.

## Features

- Browse by category, filter by tag, search titles and ingredients, star favourites.
- Recipe pages scale quantities by serves, let you tick off ingredients and steps, and can keep the screen awake.
- **Selected meals**: plan 3 to 7 days of breakfast, lunch, snacks and dinner. Add from any recipe page with the + button, from the planner grid, or load one of the seven-day meal plans.
- **Shopping list**: built from the selected meals, grouped by supermarket aisle, with quantities combined where units match. Tap anything you already have to move it out of the way. Copy or share the list, open nearby supermarkets in Maps, or jump to the Woolworths and Coles listing for an item to check its price.

## What is in the folder

| File | Purpose |
| --- | --- |
| `index.html` | The whole app: all recipe data, styles and logic |
| `manifest.webmanifest` | App name, icon and standalone window settings |
| `sw.js` | Service worker that caches everything for offline use |
| `fonts.css`, `fonts/` | Fraunces and Figtree, self-hosted so they work offline |
| `icons/` | Home-screen and browser icons |

## 1. Put it online (one-time, takes a couple of minutes)

Installable apps need to be served over HTTPS. Any static host works. Two easy options:

**Netlify Drop (no account needed to start)**
1. Open https://app.netlify.com/drop
2. Drag the whole `kitchen-recipes-app` folder onto the page.
3. Copy the URL it gives you.

**GitHub Pages**
1. Create a repository and upload these files to its root.
2. Settings → Pages → Branch: `main`, folder `/ (root)` → Save.
3. The app is served at `https://<you>.github.io/<repo>/`.

To try it on your own computer only:

```bash
python3 -m http.server 8080
```

then open http://localhost:8080 in a browser.

## 2. Install it

Open the URL on each device, then:

- **iPhone / iPad (Safari):** tap Share → Add to Home Screen. A hint appears in the app the first time.
- **Android (Chrome):** tap the Install app button in the top bar, or the browser menu → Install app.
- **Mac (Safari 17+):** File → Add to Dock.
- **Mac / Windows (Chrome or Edge):** click the Install app button in the top bar, or the install icon in the address bar.

Favourites, light/dark choice and ticked-off items stay on each device.

## 3. Updating the recipes later

1. Replace `index.html` with the new version (or edit the JSON inside the `<script id="data">` block).
2. Open `sw.js` and change the version line, for example `kitchen-recipes-v1` → `kitchen-recipes-v2`.
3. Upload the folder again.

Installed copies show an "Update" button the next time they open while online.
