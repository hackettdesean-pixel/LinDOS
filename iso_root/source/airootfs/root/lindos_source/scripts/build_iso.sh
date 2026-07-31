#!/bin/bash
set -e

echo "[LinDOS Builder] Setting up build workspace..."
BUILD_DIR="/tmp/lindos_iso_build"
LIVE_DIR="$BUILD_DIR/live"

rm -rf $BUILD_DIR
mkdir -p $LIVE_DIR/opt/lindos

make clean && make

cp lindos_core $LIVE_DIR/opt/lindos/
cp -r gui $LIVE_DIR/opt/lindos/

mkdir -p release
tar -czvf release/LinDOS-Prime-live.tar.gz -C $LIVE_DIR .
echo "[LinDOS Builder] Package compiled successfully: release/LinDOS-Prime-live.tar.gz"
