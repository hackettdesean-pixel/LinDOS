#!/bin/bash
set -e

echo "[LinDOS Builder] Setting up build workspace..."
BUILD_DIR="/tmp/lindos_iso_build"
ISO_DIR="$BUILD_DIR/iso"
LIVE_DIR="$BUILD_DIR/live"

rm -rf $BUILD_DIR
mkdir -p $ISO_DIR/boot/grub $LIVE_DIR/opt/lindos

# Compile C++ Engine
make clean && make

# Copy project files into Live ISO directory structure
cp lindos_core $LIVE_DIR/opt/lindos/
cp -r gui $LIVE_DIR/opt/lindos/

# Create GRUB configuration for bootable ISO
cat << 'GRUB' > $ISO_DIR/boot/grub/grub.cfg
set default=0
set timeout=5

menuentry "LinDOS Prime (Bare-Metal Performance OS)" {
    linux /boot/vmlinuz quiet boot=live
    initrd /boot/initrd.img
}
GRUB

# Create dummy ISO structure artifact for testing pipeline
mkdir -p release
tar -czvf release/LinDOS-Prime-live.tar.gz -C $LIVE_DIR .
echo "[LinDOS Builder] Package compiled successfully: release/LinDOS-Prime-live.tar.gz"
