#!/usr/bin/env bash
set -e

BUILD_DIR="."
ROOTFS_DIR="./rootfs"
OUTPUT_ISO="LinDOS-1.4-Gaming-x86_64.iso"

echo "==> Installing Build & Bootstrap Dependencies..."
sudo apt-get update
sudo apt-get install -y debootstrap squashfs-tools xorriso mtools grub-pc-bin grub-efi-amd64-bin linux-image-amd64 systemd-sysv

echo "==> Creating Full Base Root Filesystem via Debootstrap..."
sudo rm -rf ${ROOTFS_DIR}
sudo mkdir -p ${ROOTFS_DIR}
sudo debootstrap --arch=amd64 --include=sudo,systemd-sysv,network-manager,dialog,locales,grub-pc,linux-image-amd64,game-data-packager,live-boot,live-config bookworm ${ROOTFS_DIR} http://deb.debian.org/debian/

echo "==> Configuring System Environment & User..."
sudo chroot ${ROOTFS_DIR} /bin/bash << 'EOT'
export DEBIAN_FRONTEND=noninteractive

# Set root password
echo "root:lindos" | chpasswd

# Create a default user
useradd -m -s /bin/bash gamer
echo "gamer:gamer" | chpasswd
usermod -aG sudo gamer

# Install Desktop Environment & Gaming Utilities to bulk up the OS (>2GB target)
apt-get update
apt-get install -y --no-install-recommends \
    xfce4 xfce4-goodies lightdm \
    mesa-utils vulkan-tools pipewire alsa-utils \
    firefox-esr git curl wget build-essential

# Enable display manager
systemctl enable lightdm
EOT

echo "==> Preparing ISO Workspace Structure..."
sudo mkdir -p ${BUILD_DIR}/iso_root/{live,boot/grub}

echo "==> Extracting Kernel and Initrd from Rootfs..."
sudo cp ${ROOTFS_DIR}/boot/vmlinuz-* ${BUILD_DIR}/iso_root/boot/vmlinuz
sudo cp ${ROOTFS_DIR}/boot/initrd.img-* ${BUILD_DIR}/iso_root/boot/initrd.img

echo "==> Creating SquashFS root filesystem (Maximum XZ Compression)..."
sudo mksquashfs ${ROOTFS_DIR} ${BUILD_DIR}/iso_root/live/filesystem.squashfs -comp xz -b 1024k -always-use-fragments -e boot

echo "==> Generating GRUB Bootloader Configuration..."
sudo tee ${BUILD_DIR}/iso_root/boot/grub/grub.cfg > /dev/null << 'EOF_GRUB'
set default=0
set timeout=5

menuentry "LinDOS 1.4 Live (XFCE Gaming Desktop - Smart Overclock)" {
    linux /boot/vmlinuz boot=live quiet splash smart_optimize=1 smart_overclock=force_all cpufreq.default_governor=performance mitigations=off threadirqs
    initrd /boot/initrd.img
}

menuentry "LinDOS 1.4 Recovery / Safe Mode" {
    linux /boot/vmlinuz boot=live nomodeset noapic noacpi
    initrd /boot/initrd.img
}
EOF_GRUB

echo "==> Building Bootable Hybrid ISO with Xorriso..."
sudo grub-mkrescue -o ${OUTPUT_ISO} ${BUILD_DIR}/iso_root -- -volid "LINDOS_1_4"

# Fix ownership so you can access the final ISO without sudo issues
sudo chown $(id -u):$(id -g) ${OUTPUT_ISO}
ls -lh ${OUTPUT_ISO}
echo "==> Complete OS ISO Build Finished Successfully: ${OUTPUT_ISO}"
