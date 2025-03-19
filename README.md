# Habit Slap Site
Website for Habit Slap written in FastHTML and MonsterUI

## Setup

### TailwindCSS and DaisyUI Setup

This project uses TailwindCSS and DaisyUI for styling. Follow these steps to set up the CSS generation:

1. Download the TailwindCSS executable with DaisyUI included:

```bash
# For macOS ARM64 (M1/M2)
curl -sLO https://github.com/banditburai/fastwindcss/releases/latest/download/tailwindcss-macos-arm64
chmod +x tailwindcss-macos-arm64
mv tailwindcss-macos-arm64 tailwindcss

# For macOS x64 (Intel)
curl -sLO https://github.com/banditburai/fastwindcss/releases/latest/download/tailwindcss-macos-x64
chmod +x tailwindcss-macos-x64
mv tailwindcss-macos-x64 tailwindcss

# For Linux x64
curl -sLO https://github.com/banditburai/fastwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss-linux-x64
mv tailwindcss-linux-x64 tailwindcss

# For Linux ARM64
curl -sLO https://github.com/banditburai/fastwindcss/releases/latest/download/tailwindcss-linux-arm64
chmod +x tailwindcss-linux-arm64
mv tailwindcss-linux-arm64 tailwindcss

# For Windows x64
curl -sLO https://github.com/banditburai/fastwindcss/releases/latest/download/tailwindcss-windows-x64.exe
mv tailwindcss-windows-x64.exe tailwindcss.exe
```

2. Generate the CSS file:

```bash
# Build CSS once
./tailwindcss -i static/css/input.css -o static/css/output.css

# Or in watch mode during development (automatically rebuilds when files change)
./tailwindcss -i static/css/input.css -o static/css/output.css --watch
```

Note: The TailwindCSS executable and generated CSS files are excluded from version control. Each developer needs to download the appropriate executable for their system and generate the CSS locally.

## Running the Application

### Command Line Arguments

The application supports command line arguments to control the build process:

```bash
# Run the application with default settings
python main.py

# Rebuild Tailwind CSS before starting the application
python main.py -rt
```

Full list of command line arguments:

- `-rt, --reload_tailwind`: Run the Tailwind CLI build

### Theming

The application uses a custom theme defined in `static/css/themes.css`. This file is loaded directly in the application headers, making theme changes straightforward.

#### How Themes Work

The theme is defined using CSS variables in the format:

```css
@layer base {
  :root:has(input.theme-controller[value="mytheme"]:checked),
  [data-theme="mytheme"] {
    color-scheme: light;
    --color-base-100: oklch(28% 0.141 291.089);
    --color-primary: oklch(80% 0.114 19.571);
    /* other color variables */
  }
}
```

The application uses the `data-theme` attribute in the HTML element to apply the theme:

```html
<html lang="en" dir="ltr" data-theme="light">
```

You can change this value in `main.py` to use a different theme:

```python
app, rt = fast_app(
    # ...
    htmlkw=dict(lang="en", dir="ltr", data_theme="mytheme"),
)
```

#### Modifying Themes

To modify or create a new theme:

1. Edit `static/css/themes.css` to change existing themes or add new ones
2. Restart the application to see your changes

The `themes.css` file can contain multiple themes. For example:

```css
/* Light theme */
@layer base {
  :root:has(input.theme-controller[value="light"]:checked),
  [data-theme="light"] {
    /* theme variables */
  }
}

/* Dark theme */
@layer base {
  :root:has(input.theme-controller[value="dark"]:checked),
  [data-theme="dark"] {
    /* theme variables */
  }
}

/* Custom theme */
@layer base {
  :root:has(input.theme-controller[value="mytheme"]:checked),
  [data-theme="mytheme"] {
    /* theme variables */
  }
}
```

### Recommended Development Workflow

For the most efficient development experience, follow this workflow:

1. Start Tailwind in watch mode in one terminal:
   ```bash
   ./tailwindcss -i static/css/input.css -o static/css/output.css --watch
   ```

2. In a second terminal, run the application:
   ```bash
   python main.py
   ```

3. When making theme changes:
   - Edit `static/css/themes.css`
   - Restart the application to see your changes

4. When making Tailwind class changes in your HTML/components:
   - The watch mode will automatically rebuild the CSS
   - Refresh the browser to see your changes

This setup allows you to:
- Automatically rebuild Tailwind CSS when you change classes in your HTML
- Easily update themes by editing the themes.css file
- Keep your development environment responsive and up-to-date

For production deployment, you can use:
```bash
# Build optimized CSS for production
./tailwindcss -i static/css/input.css -o static/css/output.css --minify

# Then run the application
python main.py
```
