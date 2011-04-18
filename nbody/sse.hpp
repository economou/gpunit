#pragma once

#include <xmmintrin.h>

#define ALIGN_16 __attribute__((aligned(16)))

#define loadps(mem)     _mm_load_ps((const float* const)(mem))
#define storess(ss,mem) _mm_store_ss((float* const)(mem),(ss))
#define minss           _mm_min_ss
#define maxss           _mm_max_ss
#define minps           _mm_min_ps
#define maxps           _mm_max_ps
#define addps           _mm_add_ps
#define subps           _mm_sub_ps
#define mulps           _mm_mul_ps
#define mulss           _mm_mul_ss
#define divps           _mm_div_ps
#define sqrtps          _mm_sqrt_ps
#define shufps          _mm_shuffle_ps
#define shufarg         _MM_SHUFFLE
#define zerops          _mm_setzero_ps
#define set1ps          _mm_set1_ps
#define float2int(f)    _mm_cvtss_si32(_mm_load_ss(&(f)))
#define rotatelps(ps)   _mm_shuffle_ps((ps),(ps), 0x39)
#define muxhps(low,high) _mm_movehl_ps((low),(high))

#ifdef __SSE4_1__
#include <smmintrin.h>

// dec(241) = bin(1111 0001), uses all 4 dwords of input and uses the LSdword of the output.
static const int DOTMASK = 241;

#define dotps           _mm_dp_ps
#endif
