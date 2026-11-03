// Educational CUDA vector addition kernel for the Module 4 introduction.
// Build on a CUDA-capable system with: nvcc vector_add.cu -o vector_add
// Run with: ./vector_add
#include <cuda_runtime.h>
#include <iostream>
#include <cstdlib>

__global__ void vector_add(const int* a, const int* b, int* c, int n) {
    const int index = blockIdx.x * blockDim.x + threadIdx.x;
    if (index < n) {
        c[index] = a[index] + b[index];
    }
}

int main() {
    constexpr int n = 7;
    const int host_a[n] = {1, 2, 3, 4, 5, 6, 7};
    const int host_b[n] = {10, 20, 30, 40, 50, 60, 70};
    int host_c[n] = {};
    int *device_a = nullptr, *device_b = nullptr, *device_c = nullptr;

    auto check = [](cudaError_t status, const char* operation) {
        if (status != cudaSuccess) {
            std::cerr << operation << ": " << cudaGetErrorString(status) << "\n";
            std::exit(EXIT_FAILURE);
        }
    };

    check(cudaMalloc(&device_a, n * sizeof(int)), "cudaMalloc(a)");
    check(cudaMalloc(&device_b, n * sizeof(int)), "cudaMalloc(b)");
    check(cudaMalloc(&device_c, n * sizeof(int)), "cudaMalloc(c)");
    check(cudaMemcpy(device_a, host_a, n * sizeof(int), cudaMemcpyHostToDevice), "copy a");
    check(cudaMemcpy(device_b, host_b, n * sizeof(int), cudaMemcpyHostToDevice), "copy b");

    constexpr int threads_per_block = 4;
    constexpr int blocks = (n + threads_per_block - 1) / threads_per_block;
    vector_add<<<blocks, threads_per_block>>>(device_a, device_b, device_c, n);
    check(cudaGetLastError(), "kernel launch");
    check(cudaDeviceSynchronize(), "kernel execution");
    check(cudaMemcpy(host_c, device_c, n * sizeof(int), cudaMemcpyDeviceToHost), "copy result");

    std::cout << "Vector addition: ";
    for (int i = 0; i < n; ++i) {
        std::cout << host_c[i] << (i + 1 == n ? "\\n" : " ");
    }

    cudaFree(device_a);
    cudaFree(device_b);
    cudaFree(device_c);
    return EXIT_SUCCESS;
}
