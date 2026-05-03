#!/usr/bin/env bash
set -euo pipefail

# build_appimage.sh - Build an AppImage for TempMailShortcut
# Steps performed:
# 1. Run PyInstaller (onedir) to produce a dist/TempMailShortcut folder
# 2. Create an AppDir layout and copy the PyInstaller output
# 3. Generate a minimal .desktop and icon
# 4. Download linuxdeployqt AppImage if missing and run it to produce the final AppImage

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
NAME="TempMailShortcut"
DIST_DIR="$BASE_DIR/dist/$NAME"
APPDIR="$BASE_DIR/${NAME}.AppDir"
TOOLS_DIR="$BASE_DIR/tools"
LINUXDEPLOYQT="$TOOLS_DIR/linuxdeployqt.AppImage"

echo "[1/7] Cleaning previous builds..."
rm -rf "$BASE_DIR/build" "$BASE_DIR/dist" "$APPDIR" "$BASE_DIR"/*.AppImage

echo "[2/7] Running PyInstaller (onedir)..."
if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "pyinstaller not found, installing into user environment..."
  pip install --user pyinstaller
fi

pyinstaller --noconfirm --clean --onefile --name "$NAME" "$BASE_DIR/main.py"

echo "[3/7] Preparing AppDir layout..."
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# Copy the pyinstaller single-file binary into AppDir/usr/bin
if [ -f "$BASE_DIR/dist/$NAME" ]; then
  cp "$BASE_DIR/dist/$NAME" "$APPDIR/usr/bin/$NAME"
  chmod +x "$APPDIR/usr/bin/$NAME"
else
  echo "ERROR: expected PyInstaller output at dist/$NAME not found"
  exit 1
fi

echo "[4/7] Creating .desktop and icon..."
DESKTOP_FILE="$APPDIR/usr/share/applications/$NAME.desktop"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Temp Mail Shortcut
Exec=$NAME
Icon=$NAME
Type=Application
Categories=Utility;
EOF

# small transparent PNG (1x1) used as placeholder icon
ICON_PATH="$APPDIR/usr/share/icons/hicolor/256x256/apps/$NAME.png"
base64 -d > "$ICON_PATH" <<'PNGBASE64'
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=
PNGBASE64

echo "[5/7] Downloading linuxdeployqt if missing..."
mkdir -p "$TOOLS_DIR"
if [ ! -f "$LINUXDEPLOYQT" ]; then
  echo "Downloading linuxdeployqt AppImage..."
  LINUXDEPLOYQT_URL="https://github.com/probonopd/linuxdeployqt/releases/download/continuous/linuxdeployqt-continuous-x86_64.AppImage"
  curl -L -o "$LINUXDEPLOYQT" "$LINUXDEPLOYQT_URL"
  chmod +x "$LINUXDEPLOYQT"
fi

echo "[6/7] Running linuxdeployqt to produce AppImage (this may take a while)..."
# linuxdeployqt expects a desktop file path
"$LINUXDEPLOYQT" "$DESKTOP_FILE" -appimage

echo "[7/7] Done. The AppImage should be in the current directory." 
echo "Files generated:" 
ls -1t "$BASE_DIR"/*.AppImage || true

exit 0
