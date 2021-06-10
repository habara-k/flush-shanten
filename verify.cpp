#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include "shanten-number-calculator/calsht.hpp"

int main()
{
  clock_t start = clock();

  Calsht calsht;
  // Set the location of shanten tables
  calsht.initialize(".");

  for (std::string file : {"shanten-py.txt", "shanten-rs.txt"}) {
    std::ifstream ifs(file);
    std::string line;
    while (std::getline(ifs, line)) {
      std::vector<int> hand(34);
      std::stringstream ss(line);
      for (int i = 0; i < 9; ++i) ss >> hand[i];
      int actual; ss >> actual;
      
      auto expected = calsht.calc_lh(hand.data(), 4);
      if (expected != actual) {
          std::cout << "expedted: " << expected << std::endl;
          std::cout << "actual: " << actual << std::endl << std::endl;
          std::cout << "hand: ";
          for (int i = 0; i < 9; ++i) std::cout << hand[i] << ' ';
          std::cout << std::endl;
      }
      assert(expected == actual);
    }
  }

  const double elapsed_time = static_cast<double>(clock()-start) / CLOCKS_PER_SEC;
  std::cout << "elapsed_time: " << elapsed_time << " [sec]" << std::endl;

  return 0;
}
