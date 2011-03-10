#include <iostream>
#include <fstream>
#include <vector>
#include <sys/time.h>
#include <cstdlib>
#include <cmath>

#include "vector.hpp"

using namespace std;

static const double G = 6.67428e-11;
static const double mSun = 1.98892e30;
static const double mEarth = 5.9742e24;
static const double metersPerAU = 1.495978707e11;
static const double vEarthOrbit = 29780;
static const double AUsPerParsec = 206264.8062;

void integrateRK4(
        vector<vec3>& points,
        vector<vec3>& v,
        const vector<double>& masses,
        const double& dt);

inline vec3 gravity(
        const vec3& pi,
        const vector<vec3>& points,
        const vector<double>& masses,
        const int& i) {

    vec3 grav(0.0);

    for(int j=0; j<points.size(); ++j) {
        if(j != i) {
            const vec3 r = points[j] - pi;
            const double acceleration = G * masses[j] / norm2(r);
            grav += acceleration * normalize(r);
        }
    }

    return grav;
}

static const int N = 512;
int main(int argc, char** argv) {
    vector<vec3> points(N);
    vector<vec3> velocities(N);
    vector<double> masses(N);

    for(int i=0; i<N; ++i) {
        points[i] = vec3(rand() / (float) RAND_MAX);
        velocities[i] = vec3(rand() / (float) RAND_MAX);
        masses[i] = (rand() / (float) RAND_MAX);
    }

    // Sun
    /*
    points[0] = vec3(0,0,0);
    velocities[0] = vec3(0,0,0);
    masses[0] = mSun;

    // Earth
    points[1] = vec3(1.0 * metersPerAU, 0, 0);
    velocities[1] = vec3(0, vEarthOrbit, 0);
    masses[1] = mEarth;
    */

    const double dt = (60 * 60 * 24);
    const int timesteps = 730;
    cerr <<  timesteps << endl;

    ofstream file("pos.txt");

    struct timeval start, end;
    for(int t = 0; t < timesteps; ++t) {
        file << points[0] << "," << points[1] << "," << points[2] << endl;
        gettimeofday(&start, NULL);
        integrateRK4(points, velocities, masses, dt);
        gettimeofday(&end, NULL);
        const float elapsed = (float)(end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1e6f;
        cerr << elapsed << "s" << endl;

        if(t%100 == 0) cerr << "T: " << t << endl;
    }

    return 0;
}

void integrateRK4(
        vector<vec3>& points,
        vector<vec3>& v,
        const vector<double>& masses,
        const double& dt) {

    const vector<vec3> pcopy = points;
    const vector<vec3> vcopy = v;

    for(int i=0; i < points.size(); ++i) {
        const vec3 dxdt1 = vcopy[i];
        const vec3 dvdt1 = gravity(pcopy[i], pcopy, masses, i);

        const vec3 dxdt2 = vcopy[i] + dt * dvdt1/2.0;
        const vec3 dvdt2 = gravity(pcopy[i] + dt * dxdt1/2.0, pcopy, masses, i);

        const vec3 dxdt3 = vcopy[i] + dt * dvdt2/2.0;
        const vec3 dvdt3 = gravity(pcopy[i] + dt * dxdt2/2.0, pcopy, masses, i);

        const vec3 dxdt4 = vcopy[i] + dt * dvdt3;
        const vec3 dvdt4 = gravity(pcopy[i] + dt * dxdt3, pcopy, masses, i);

        points[i] += (dt/6.0) * (dxdt1 + 2.0*(dxdt2 + dxdt3) + dxdt4);
        v[i] += (dt/6.0) * (dvdt1 + 2.0*(dvdt2 + dvdt3) + dvdt4);
    }
}
