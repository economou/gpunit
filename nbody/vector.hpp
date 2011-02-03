#pragma once

#include <cmath>
#include <cassert>
#include <iostream>

using std::ostream;

class point3;

class vec3 {
    friend class point3;
    public:
        vec3(const point3& p);

        vec3(){
            x = 0.f;
            y = 0.f;
            z = 0.f;
            w = 0.f;
        }

        vec3(const double& x_, const double& y_, const double& z_){
            x = x_;
            y = y_;
            z = z_;
            w = 0.f;
        }

        vec3(const vec3& v){
            x = v.x;
            y = v.y;
            z = v.z;
            w = 0.f;
        }

        vec3(const double& f){
            x = f;
            y = f;
            z = f;
            w = 0.f;
        }


        inline const double& operator()(const int& index) const{
#ifdef DEBUG
            assert(index < 3);
#endif
            return *(&x + index);
        }

        inline double& operator()(const int& index){
#ifdef DEBUG
            assert(index < 3);
#endif
            return *(&x + index);
        }

        inline const vec3 operator+(const vec3& v) const {
            return vec3(v) += *this;
        }

        inline vec3& operator+=(const vec3& v){
            x += v.x;
            y += v.y;
            z += v.z;
            return (*this);
        }

        inline const vec3 operator-(const vec3& v) const {
            return vec3(*this) -= v;
        }

        inline vec3& operator-=(const vec3& v){
            return (*this) += -v;
        }

        inline const vec3 operator-() const {
            return vec3(-x, -y, -z);
        }

        inline const vec3 operator*(const double& f) const {
            return vec3(*this) *= f;
        }

        inline vec3& operator*=(const double& f){
            x *= f;
            y *= f;
            z *= f;
            return (*this);
        }

        inline const vec3 operator*(const vec3& v) const {
            return vec3(*this) *= v;
        }

        inline vec3& operator*=(const vec3& v){
            x *= v(0);
            y *= v(1);
            z *= v(2);
            return (*this);
        }

        inline const vec3 operator/(const double& f) const {
            return vec3(*this) *= 1.f / f;
        }

        inline vec3& operator/=(const double& f){
            return (*this) *= 1.f / f;
        }

        inline const vec3 operator/(const vec3& v) const {
            return vec3(*this) /= v;
        }

        inline vec3& operator/=(const vec3& v){
            x /= v(0);
            y /= v(1);
            z /= v(2);
            return (*this);
        }

        inline bool operator==(const vec3& v) const {
            return
                (x == v.x) &&
                (y == v.y) &&
                (z == v.z);
        }

        union{
            struct {
                double x;
                double y;
                double z;
                double w;
            };
        };
};

template <typename vecType>
inline double norm(const vecType& v) {
    return sqrtf(norm2(v));
}

inline double dot(const vec3& u, const vec3& v){
    return
        (u.x * v.x) +
        (u.y * v.y) +
        (u.z * v.z);
}

inline vec3 cross(const vec3& a, const vec3& b){
    return vec3(
            (a.y * b.z) - (a.z * b.y),
            (a.z * b.x) - (a.x * b.z),
            (a.x * b.y) - (a.y * b.x)
        );
}

inline const vec3 operator*(const double& f, const vec3& u){
    return u * f;
}

inline vec3& operator*=(const double& f, vec3& u){
    return (u *= f);
}

inline const vec3 operator/(const double& f, const vec3& v){
    return vec3(f / v.x, f / v.y, f / v.z);
}

inline double norm2(const vec3& v) {
    return v.x*v.x + v.y*v.y + v.z*v.z;
}

inline const vec3 normalize(const vec3& u){
    return u / norm(u);
}

ostream& operator<<(ostream& out, const vec3& x);
