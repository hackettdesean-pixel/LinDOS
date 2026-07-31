CXX = g++
CC = gcc
CXXFLAGS = -O3 -march=native -flto -Wno-unused-result
CFLAGS = -O3 -march=native -flto
SRC = src/lindos_core.cpp
TARGET = lindos_core

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)
	@echo "[LinDOS] High-performance build complete: ./lindos_core"

clean:
	rm -f $(TARGET)
