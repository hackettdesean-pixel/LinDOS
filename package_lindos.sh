#!/bin/bash
set -e

echo "[LinDOS] Creating LinDOS Prime deployment bundle..."
BUNDLE_DIR="lindos_prime_release"
rm -rf "$BUNDLE_DIR" "lindos-prime.tar.gz"
mkdir -p "$BUNDLE_DIR/bin"
mkdir -p "$BUNDLE_DIR/gui"
mkdir -p "$BUNDLE_DIR/config"

# Copy compiled optimizer binary
if [ -f "./bin/lindos-optimizer" ]; then
    cp ./bin/lindos-optimizer "$BUNDLE_DIR/bin/"
    echo "[LinDOS] Included C++ optimizer daemon."
fi

# Copy Python desktop environment
if [ -d "./gui" ]; then
    cp -r ./gui/* "$BUNDLE_DIR/gui/"
    echo "[LinDOS] Included Python desktop UI."
fi

# Copy boot script if it exists
if [ -f "/usr/local/bin/lindos-boot.sh" ]; then
    cp /usr/local/bin/lindos-boot.sh "$BUNDLE_DIR/config/"
    echo "[LinDOS] Included boot sequence script."
fi

# Compress into a portable tarball archive
tar -czf lindos-prime.tar.gz "$BUNDLE_DIR"
echo "[LinDOS] Success! Your portable release package is ready: lindos-prime.tar.gz"
