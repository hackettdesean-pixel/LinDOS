# LinDOS Prime

LinDOS Prime is an advanced bare-metal hardware optimizer daemon and lightweight hybrid desktop environment.

## Quick Start
```bash
make
./lindos_core &
python3 gui/desktop.py
#!/bin/bash
set -e

echo "=========================================="
echo " [LinDOS Prime] Interactive Nano Workspace Setup"
echo "=========================================="

# 1. Install nano and essential utilities
apt-get update && apt-get install -y nano build-essential g++ make python3 python3-tk git

# 2. Create Directory Structure
mkdir -p src gui scripts .github/workflows

# 3. Write C++ Hardware Optimizer Engine
cat << 'EOF' > src/lindos_core.cpp
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <unistd.h>

class LinDOSCore {
private:
    bool writeSysFile(const std::string& path, const std::string& value) {
        std::ofstream file(path);
        if (!file.is_open()) return false;
        file << value;
        return file.good();
    }

    bool runCmd(const std::string& cmd) {
        int res = std::system(cmd.c_str());
        return (res == 0);
    }

public:
    void initializeOptimizations() {
        std::cout << "[LinDOS Core] Initializing low-level system optimizations...\n";

        if (runCmd("modprobe zram 2>/dev/null")) {
            writeSysFile("/sys/block/zram0/comp_algorithm", "zstd");
            writeSysFile("/sys/block/zram0/disksize", "1G");
            runCmd("mkswap /dev/zram0 >/dev/null 2>&1");
            runCmd("swapon -p 100 /dev/zram0 >/dev/null 2>&1");
            std::cout << "[LinDOS Core] ZRAM initialized successfully.\n";
        }

        if (writeSysFile("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "performance")) {
            std::cout << "[LinDOS Core] CPU locked to High-Performance mode.\n";
        } else {
            std::cout << "[LinDOS Core] Hardware sysfs locked by host environment (Normal for containers).\n";
        }
    }

    void monitorAndBoost() {
        std::cout << "[LinDOS Core] Background optimization loop active...\n";
        while (true) {
            writeSysFile("/proc/sys/vm/drop_caches", "3");
            sleep(10);
        }
    }
};

int main() {
    LinDOSCore core;
    core.initializeOptimizations();
    core.monitorAndBoost();
    return 0;
}
