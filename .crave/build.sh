#!/bin/bash
set -e

echo "=== LinDOS Crave Build ==="

cd ~/LinDOS

echo "[1/5] Installing build tools..."
apt update
apt install -y git build-essential bc bison flex cpio gzip xz-utils bzip2 wget

echo "[2/5] Preparing tools..."

mkdir -p tools

if [ ! -d tools/busybox-1.36.1 ]; then
    cd tools
    wget https://busybox.net/downloads/busybox-1.36.1.tar.bz2
    tar xf busybox-1.36.1.tar.bz2
    cd ..
fi

echo "[3/5] Building BusyBox..."
cd tools/busybox-1.36.1
make defconfig
make -j$(nproc)
cd ../..

echo "[4/5] Preparing rootfs..."
mkdir -p rootfs/bin
cp tools/busybox-1.36.1/busybox rootfs/bin/

echo "[5/5] LinDOS build complete!"
