void f(){
    int arr[1];
    #pragma acc serial reduction(max:arr[0:1])
    {}
}
