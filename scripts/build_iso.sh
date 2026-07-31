#!/usr/bin/env bash
set -e

echo "=== LinDOS x86 ISO Builder ==="

# We are running this on GitHub's Ubuntu servers, so we install the tools here
if ! command -v xorriso &> /dev/null; then
    echo "Installing ISO tools..."
    sudo apt-get update
    sudo apt-get install -y xorriso grub-pc-bin grub-efi-amd64-bin mtools dosfstools
fi

echo "Setting up custom OS profile..."
mkdir -p iso_root/boot/grub

# Make sure GRUB is configured
cat << 'CFG' > iso_root/boot/grub/grub.cfg
set timeout=5
set default=0

menuentry "LinDOS Live Environment" {
    echo "Loading LinDOS core..."
    # When you have a compiled kernel, it will be loaded here
}
CFG

echo "Building the actual ISO image..."
grub-mkrescue -o LinDOS.iso iso_root/

echo "Build complete! ISO size:"
ls -lh LinDOS.iso
