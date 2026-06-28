#include <iostream>
#include <vector>
#include <set>
#include <cstring>

template <typename Iterator, typename Predicate>
Iterator mymax(Iterator first, Iterator last, Predicate pred) {
    if (first == last) return last;  // Prazan niz

    Iterator max = first;
    for (++first; first != last; ++first) {
        if (pred(*first, *max)) {
            max = first;
        }
    }
    return max;
}

bool gt_int(const int& a, const int& b) { return a > b; }
bool gt_char(const char& a, const char& b) { return a > b; }
bool gt_str(const std::string& a, const std::string& b) { return a > b; }

int main() {
    int arr_int[] = {1, 3, 5, 7, 4, 6, 9, 2, 0};
    const int* max_int = mymax(
        &arr_int[0],
        &arr_int[sizeof(arr_int)/sizeof(int)],
        gt_int
    );
    std::cout << "Najveci int[] element: " << *max_int << "\n";

    char arr_char[] = "Suncana strana ulice";
    const char* max_char = mymax(
        &arr_char[0],
        &arr_char[sizeof(arr_char)/sizeof(char) - 1],
        gt_char
    );
    std::cout << "Najveci char[] element: " << *max_char << "\n";

    std::vector<std::string> vec_str = {"Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise"};
    auto max_vec_str = mymax(
        vec_str.begin(),
        vec_str.end(),
        gt_str
    );
    std::cout << "Najveci vector<string> element: " << *max_vec_str << "\n";

    std::set<int> set_int = {1, 3, 5, 7, 4, 6, 2, 0};
    auto max_set_int = mymax(
        set_int.begin(),
        set_int.end(),
        gt_int
    );
    std::cout << "Najveci set<int> element: " << *max_set_int << "\n";

    return 0;
}