# pretix-event-css-js

Inject custom CSS and JavaScript into the presale pages of an organizer or an individual event in [pretix](https://pretix.eu). Useful for branding tweaks, custom layouts, tracking snippets, or any frontend customization that doesn't warrant a full theme.

**Key capabilities:**
- Organizer-wide custom CSS and JavaScript
- Optional per-event CSS and JavaScript overrides
- Organizer asset upload for fonts, images, and other files referenced by CSS
- Code editors in the organizer and event settings panels
- Content-hash based cache busting (1-year cache with automatic invalidation on change)
- Clean removal of settings when the plugin is uninstalled

## Screenshot

**Settings — custom CSS & JS editor**

![Settings](docs/images/settings.png)

## How it works

1. You enter organizer-wide CSS and/or JavaScript in the organizer settings. It is loaded on every public page belonging to that organizer.
2. You can add event-specific CSS and/or JavaScript in the event settings. It is loaded after the organizer code, so it can override it.
3. The CSS and JS are served from dedicated same-origin endpoints with a content-hash query parameter for cache busting. Browsers cache them for up to 1 year — when you update the code, the hash changes and browsers fetch the new version automatically.

## Installation

```bash
pip install pretix-event-css-js
```

Then restart the server. The plugin registers itself automatically via the `pretix.plugin` entry point — no manual `INSTALLED_APPS` edit needed.

### Development installation

```bash
git clone https://github.com/nicoknoll/pretix-event-css-js.git
cd pretix-event-css-js
pip install -e .
```

## Usage

1. Enable the plugin for your organizer under **Settings** → **Plugins**.
2. Go to **Organizer CSS & JS** in the organizer control panel and enter the shared CSS and/or JavaScript.
3. If needed, go to **Event CSS & JS** in an event's settings to add event-specific overrides.

Organizer code is loaded on all public organizer/event pages. Event code is loaded on every public page of that event.

Use **Organizer CSS & JS → Assets** to upload files. The page shows a relative URL
such as `assets/<asset-id>/`; use that URL from organizer or event CSS. Assets are
stored with the organizer and served through the same organizer/event domain.

The included `examples/designer-overlay-fixed.css` is a cleaned version of the supplied designer overlay. It references the packaged Parking font through the plugin's relative `parking.woff2` endpoint, so it also works with organizer and event domains without relying on a `/static/` URL.

> **Heads up:** Faulty JavaScript can break the checkout flow for your customers. Test thoroughly before going live.

## Dependencies

| Package | Purpose |
|---|---|
| `pretix >= 2026.6.0` | Host platform |

Python 3.10+ required. No additional dependencies beyond pretix itself.

## License

MIT — see [LICENSE](LICENSE).
