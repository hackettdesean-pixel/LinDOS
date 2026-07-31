#!/bin/bash
set -e
echo "[+] Removing conflicting XFCE and LightDM packages..."
pacman -Rns --noconfirm xfce4 xfce4-goodies lightdm lightdm-gtk-greeter 2>/dev/null || true

echo "[+] Installing local KDE Plasma and applications..."
pacman -U --noconfirm /storage/emulated/0/Audiobooks/LinDOS-main/kde-plasma/*.pkg.tar.zst
pacman -U --noconfirm /storage/emulated/0/Audiobooks/LinDOS-main/apps/*.pkg.tar.zst

systemctl enable sddm
systemctl enable NetworkManager
echo "[+] Local KDE Plasma setup finished successfully!"
