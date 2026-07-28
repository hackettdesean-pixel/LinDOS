#!/usr/bin/env bash
set -e

BUILD_DIR="."
ROOTFS_DIR="./rootfs"
OUTPUT_ISO="LinDOS-1.3-Gaming-x86_64.iso"

echo "==> Preparing ISO Workspace..."
mkdir -p ${BUILD_DIR}/iso_root/{live,boot/grub}

echo "==> Creating SquashFS root filesystem (Maximum XZ Compression)..."
mksquashfs ${ROOTFS_DIR} ${BUILD_DIR}/iso_root/live/filesystem.squashfs -comp xz -b 1024k -always-use-fragments

echo "==> Copying Kernel and Initrd..."
cp ${ROOTFS_DIR}/boot/vmlinuz* ${BUILD_DIR}/iso_root/boot/vmlinuz 2>/dev/null || cp /boot/vmlinuz* ${BUILD_DIR}/iso_root/boot/vmlinuz
cp ${ROOTFS_DIR}/boot/initrd.img* ${BUILD_DIR}/iso_root/boot/initrd.img

echo "==> Generating GRUB Bootloader Configuration..."
cat << 'EOF_GRUB' > ${BUILD_DIR}/iso_root/boot/grub/grub.cfg
set default=0
set timeout=5

menuentry "LinDOS 1.3 Live (Performance Mode - Smart Overclock Forced)" {
    linux /boot/vmlinuz boot=live quiet splash quiet_success smart_optimize=1 smart_overclock=force_all cpufreq.default_governor=performance mitigations=off threadirqs nvme_load=YES
    initrd /boot/initrd.img
}

menuentry "LinDOS 1.3 Live (Gaming Mode - GameScope & AMD/NVIDIA Tuning)" {
    linux /boot/vmlinuz boot=live quiet splash gamescope=1 smart_optimize=1 smart_overclock=force_all cpufreq.default_governor=performance mitigations=off amdgpu.ppfeaturemask=0xffffffff threadirqs
    initrd /boot/initrd.img
}

menuentry "LinDOS 1.3 Recovery (Safe Mode / Boot Repair)" {
    linux /boot/vmlinuz boot=live nomodeset noapic noacpi fallback=1
    initrd /boot/initrd.img
}
EOF_GRUB

echo "==> Building Bootable Hybrid ISO with Xorriso..."
grub-mkrescue -o ${OUTPUT_ISO} ${BUILD_DIR}/iso_root -- -volid "LINDOS_1_3"

echo "==> ISO Build Complete: ${OUTPUT_ISO}"
