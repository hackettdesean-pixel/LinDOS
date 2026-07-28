#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <unistd.h>
#include <sys/stat.h>

// LinDOS Core Hardware Optimizer Daemon
// Targets low-resource environments to maximize performance and manage memory.

const std::string ZRAM_DEVICE = "/dev/zram0";
const std::string CPU_GOVERNOR_PATH = "/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor";

bool executeCommand(const std::string& cmd) {
    int result = std::system(cmd.c_str());
    return (result == 0);
}

void configureZram() {
    std::cout << "[LinDOS] Initializing ZRAM swap optimization..." << std::endl;

    // Load zram module
    if (!executeCommand("modprobe zram num_devices=1")) {
        std::cerr << "[LinDOS Error] Failed to load zram kernel module." << std::endl;
        return;
    }

    // Set compression algorithm to lzo-rle or zstd for low overhead
    std::ofstream algoFile("/sys/block/zram0/comp_algorithm");
    if (algoFile.is_open()) {
        algoFile << "zstd";
        algoFile.close();
    }

    // Set disk size (e.g., 512MB compressed swap for low-RAM systems)
    std::ofstream sizeFile("/sys/block/zram0/disksize");
    if (sizeFile.is_open()) {
        sizeFile << "512M";
        sizeFile.close();
    }

    // Initialize swap area
    if (!executeCommand("mkswap /dev/zram0")) {
        std::cerr << "[LinDOS Error] Failed to make swap on " << ZRAM_DEVICE << std::endl;
        return;
    }

    // Enable swap with high priority
    if (!executeCommand("swapon -p 100 /dev/zram0")) {
        std::cerr << "[LinDOS Error] Failed to activate ZRAM swap." << std::endl;
        return;
    }

    std::cout << "[LinDOS] ZRAM successfully configured and activated." << std::endl;
}

void optimizeCpuPerformance() {
    std::cout << "[LinDOS] Tuning CPU governors for responsiveness..." << std::endl;

    // Set available cores to 'schedutil' or 'performance' depending on load
    std::string cmd = "for cpu in /sys/devices/system/cpu/cpu[0-9]*; do "
                      "if [ -f \"$cpu/cpufreq/scaling_governor\" ]; then "
                      "echo 'schedutil' > \"$cpu/cpufreq/scaling_governor\"; "
                      "fi; done";

    if (executeCommand(cmd)) {
        std::cout << "[LinDOS] CPU governors optimized successfully." << std::endl;
    } else {
        std::cerr << "[LinDOS Warning] Could not set CPU governor scaling across all cores." << std::endl;
    }
}

int main() {
    if (getuid() != 0) {
        std::cerr << "[LinDOS Error] Optimizer daemon must be run as root." << std::endl;
        return 1;
    }

    std::cout << "[LinDOS] Starting Hardware Optimization Daemon..." << std::endl;

    configureZram();
    optimizeCpuPerformance();

    std::cout << "[LinDOS] Optimization sequence completed." << std::endl;
    return 0;
}
