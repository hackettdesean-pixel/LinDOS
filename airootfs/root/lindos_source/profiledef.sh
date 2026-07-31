#!/usr/bin/env bash
iso_name="lindos"
iso_label="LINDOS_$(date +%Y%m%d)"
iso_publisher="Lindos OS"
iso_application="Lindos Live ISO"
iso_version="1.0.0"
install_dir="arch"
arch="x86_64"
filesize="0"
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
)
