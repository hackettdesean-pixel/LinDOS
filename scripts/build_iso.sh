#!/usr/bin/env bash
set -e

echo "Preparing ISO directory structure..."
mkdir -p iso_root/boot/grub
mkdir -p iso_root/source

cp -r * iso_root/source/ 2>/dev/null || true

cat << 'CFG' > iso_root/boot/grub/grub.cfg
set timeout=3
set default=0

menuentry "LinDOS Live Environment" {
    echo "Starting LinDOS..."
}

menuentry "Reboot" {
    reboot
}
CFG

echo "Generating bootable LinDOS.iso..."
grub-mkrescue -o LinDOS.iso iso_root/

echo "Build complete! ISO size:"
ls -lh LinDOS.iso
