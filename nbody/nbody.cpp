#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>

#include "vector.hpp"

using namespace std;

static const double G = 6.67428e-11;
static const double mSun = 1.98892e30;
static const double mEarth = 5.9742e24;
static const double AU = 1.495978707e8;
static const double vEarthOrbit = 29780.0;

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
            const vec3 gravForce = normalize(points[j] - pi) *
                ((G * masses[i]) * masses[j] /
                 norm2(points[j] - pi));
            grav += gravForce / masses[i];
        }
    }

    return grav;
}

int main(int argc, char** argv) {
    vector<vec3> points(2);
    vector<vec3> velocities(2);
    vector<double> masses(2);

    // Sun
    points[0] = vec3(0,0,0);
    velocities[0] = vec3(0,0,0);
    masses[0] = 1.0;

    // Earth
    points[1] = vec3(1.0 * AU, 0, 0);
    velocities[1] = vec3(0, vEarthOrbit, 0);
    masses[1] = mEarth / mSun;

    const double dt = 60*60;
    const int timesteps = 500;
    cerr << "Timesteps: " << timesteps << endl;

    ofstream file("pos.txt");
    for(int t = 0; t < timesteps; ++t) {
        file << points[0] << "," << points[1] << endl;
        integrateRK4(points, velocities, masses, dt);

        if(t%100 == 0) cerr << "T: " << t << endl;
    }

    return 0;
}

static const int N = 10000;
static const double Nd = (double)N;

void integrateRK4(
        vector<vec3>& points,
        vector<vec3>& v,
        const vector<double>& masses,
        const double& dt) {

    const vector<vec3> pcopy = points;
    const vector<vec3> vcopy = v;
    const float h = dt / Nd;

//#pragma omp parallel for schedule(dynamic)
    for(int i=0; i < points.size(); ++i) {
        for(int j=0; j < N; ++j) {
            const vec3 dxdt1 = vcopy[i];
            const vec3 dvdt1 = gravity(pcopy[i], pcopy, masses, i);

            const vec3 dxdt2 = vcopy[i] + h * dvdt1/2.0;
            const vec3 dvdt2 = gravity(pcopy[i] + h * dxdt1/2.0, pcopy, masses, i);

            const vec3 dxdt3 = vcopy[i] + h * dvdt2/2.0;
            const vec3 dvdt3 = gravity(pcopy[i] + h * dxdt2/2.0, pcopy, masses, i);

            const vec3 dxdt4 = vcopy[i] + h * dvdt3;
            const vec3 dvdt4 = gravity(pcopy[i] + h * dxdt3, pcopy, masses, i);

            points[i] += (h/6.0) * (dxdt1 + 2.0*(dxdt2 + dxdt3) + dxdt4);
            v[i] += (h/6.0) * (dvdt1 + 2.0*(dvdt2 + dvdt3) + dvdt4);
        }
    }
}
