#!/bin/bash

set -e

echo "=============================="
echo "       LinDOS Build System"
echo "=============================="

ROOT=$(pwd)

mkdir -p build
mkdir -p downloads
mkdir -p rootfs
mkdir -p initramfs

echo "[+] Checking dependencies"

for tool in gcc make git cpio gzip; do
    if command -v $tool >/dev/null; then
        echo "[OK] $tool"
    else
        echo "[MISSING] $tool"
    fi
done

echo "[+] LinDOS directory ready"

echo "Build stage 1 complete"
