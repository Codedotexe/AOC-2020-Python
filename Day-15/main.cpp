#include <list> 
#include <iostream>
#include <unordered_map>

using namespace std;

int simulate(list<int> l, int totalTurns) {
	unordered_map<int,int> dict;

	// Insert pair (i,0) for every i in mem except the last one
	int i=1;
	for(list<int>::iterator it=l.begin(); it != --l.end(); ++it){
	    dict.insert(std::make_pair(*it, i));
	    i++;
	}

	int lastSpoken = *(--l.end()); // Last entry of l
	for(int t=l.size()+1; t<=totalTurns; t++) {
		int temp = lastSpoken;
		if(dict.find(lastSpoken) == dict.end()) {
			dict[lastSpoken] = t-1;
			lastSpoken = 0;			
		} else {
			lastSpoken = (t-1) - dict[lastSpoken];
		}

		dict[temp] = t-1;
	}
	return lastSpoken;
}

int main() {
	list<int> l = {13,16,0,12,15,1};
	cout << "Part 1: " << endl << simulate(l, 2020) << endl;
	cout << "Part 2: " << endl << simulate(l, 30000000) << endl; // Can take up to 30sec
	return 0;
}
