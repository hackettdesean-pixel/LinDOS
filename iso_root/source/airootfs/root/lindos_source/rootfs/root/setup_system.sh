#!/bin/bash
set -e

echo "[+] Purging conflicting desktop environments and display managers..."
pacman -Rns --noconfirm xfce4 xfce4-goodies lightdm lightdm-gtk-greeter gdm lxdm gnome gnome-shell 2>/dev/null || true

echo "[+] Updating system packages..."
pacman -Syu --noconfirm

echo "[+] Installing KDE Plasma Desktop Environment and SDDM..."
pacman -S --noconfirm \
    plasma-meta \
    kde-applications-meta \
    sddm

echo "[+] Installing core apps and utilities..."
pacman -S --noconfirm \
    firefox \
    vlc \
    gimp \
    thunar \
    geany \
    htop \
    papirus-icon-theme \
    ttf-dejavu

echo "[+] Installing Wine (.exe support) and binfmt..."
pacman -S --noconfirm \
    binfmt-support \
    wine-staging \
    winetricks \
    wine-mono \
    wine_gecko

echo "[+] Installing hardware drivers (GPUs, Wi-Fi, Audio, Bluetooth)..."
pacman -S --noconfirm \
    mesa \
    lib32-mesa \
    xf86-video-amdgpu \
    xf86-video-intel \
    nvidia \
    nvidia-utils \
    lib32-nvidia-utils \
    linux-firmware \
    wireless_tools \
    wpa_supplicant \
    networkmanager \
    bluez \
    bluez-utils \
    alsa-firmware \
    alsa-utils \
    pulseaudio \
    pulseaudio-alsa

if [ -f /usr/bin/update-binfmts ]; then
    update-binfmts --enable wine || true
elif [ -d /proc/sys/fs/binfmt_misc ]; then
    if [ ! -f /proc/sys/fs/binfmt_misc/wine ]; then
        echo ':DOSExecutable:M::MZ::/usr/bin/wine:' > /proc/sys/fs/binfmt_misc/register 2>/dev/null || true
    fi
fi

fc-cache -fv
systemctl enable sddm
systemctl enable NetworkManager
systemctl enable bluetooth
echo "[+] KDE Plasma setup complete!"
