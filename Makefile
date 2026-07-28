CXX = g++
CXXFLAGS = -O3 -Wno-unused-result
SRC = src/lindos_core.cpp
TARGET = lindos_core

all: $(TARGET)

$(TARGET): $(SRC)
$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)
@echo "[LinDOS] Build complete! Executable created: ./lindos_core"

clean:
rm -f $(TARGET)
