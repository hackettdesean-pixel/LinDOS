#!/bin/bash
set -e

echo "[LinDOS] Setting up ISO staging directory..."
STAGING_DIR="iso_staging"
rm -rf "$STAGING_DIR"
mkdir -p "$STAGING_DIR/boot/grub"
mkdir -p "$STAGING_DIR/bin"
mkdir -p "$STAGING_DIR/gui"

# Copy compiled binaries and UI files
if [ -f "./bin/lindos-optimizer" ]; then
    cp ./bin/lindos-optimizer "$STAGING_DIR/bin/"
    echo "[LinDOS] Copied C++ optimizer daemon."
fi

if [ -d "./gui" ]; then
    cp -r ./gui/* "$STAGING_DIR/gui/"
    echo "[LinDOS] Copied Python desktop UI."
fi

# Write GRUB configuration for boot menu
cat << 'EOF' > "$STAGING_DIR/boot/grub/grub.cfg"
set timeout=3
set default=0

menuentry "LinDOS Prime - Low Resource Environment" {
    echo "Loading LinDOS Prime workspace..."
    insmod gzio
    insmod all_video
}
