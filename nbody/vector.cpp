#include <iostream>
#include "vector.hpp"

using std::ostream;

ostream& operator<<(ostream& out, const vec3& x){
    out << x(0) << " " << x(1) << " " << x(2);
    return out;
}
