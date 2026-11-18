
#!/bin/bash
set -eu

NAME="enigma2-plugin-extensions-novalerassistant"
VERSION="1.0.0"
ARCH="all"
PLUGIN_DIR="usr/lib/enigma2/python/Plugins/Extensions/NovalerAssistant"

ROOT="$(pwd)"
WORK="$ROOT/build"
PKG="$WORK/package"
DIST="$ROOT/dist"

rm -rf "$WORK"
mkdir -p "$PKG/$PLUGIN_DIR/../" "$PKG/DEBIAN" "$DIST"

mkdir -p "$PKG/$PLUGIN_DIR"

cp "$ROOT/plugin.py" "$PKG/$PLUGIN_DIR/plugin.py"
cp "$ROOT/__init__.py" "$PKG/$PLUGIN_DIR/__init__.py"

cat > "$PKG/DEBIAN/control" <<EOF
Package: $NAME
Version: $VERSION
Architecture: $ARCH
Section: extra
Priority: optional
Maintainer: Novaler Assistant
Depends: enigma2
Description: Arabic assistant plugin for Novaler Enigma2 receivers
EOF

python3 -m py_compile "$PKG/$PLUGIN_DIR/plugin.py"
rm -rf "$PKG/$PLUGIN_DIR/__pycache__"

mkdir -p "$WORK/control" "$WORK/data"
cp "$PKG/DEBIAN/control" "$WORK/control/control"

cp -a "$PKG/usr" "$WORK/data/usr"

echo "2.0" > "$WORK/debian-binary"

tar -czf "$WORK/control.tar.gz" -C "$WORK/control" .
tar -czf "$WORK/data.tar.gz" -C "$WORK/data" .

(
    cd "$WORK"
    ar r "$DIST/${NAME}_${VERSION}_${ARCH}.ipk" \
        debian-binary control.tar.gz data.tar.gz
)

echo "IPK package created successfully:"
ls -lh "$DIST/"

