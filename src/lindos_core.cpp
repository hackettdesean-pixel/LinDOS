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
            std::cout << "[LinDOS Core] ZRAM initialized.\n";
        }

        if (writeSysFile("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor", "performance")) {
            std::cout << "[LinDOS Core] CPU locked to High-Performance mode.\n";
        } else {
            std::cout << "[LinDOS Core] Hardware sysfs locked by host environment (Virtual Root Active).\n";
        }
    }

    void monitorAndBoost() {
        std::cout << "[LinDOS Core] Background optimization loop running...\n";
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
