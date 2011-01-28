.PHONY: all clean

CXXFLAGS = -O3 -msse -msse2 -msse3 -msse4 -msse4.1 -msse4.2 -fopenmp

all:
	g++ $(CXXFLAGS) nbody.cpp vector.cpp -o nbody
