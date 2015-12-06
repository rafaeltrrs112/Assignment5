#include <iostream>
#include <fstream>
#include <vector>
#include <map>

using namespace std;
//Contains helper method
bool contains(string s, char c){
    for(char find : s){
        if (find == c ) return true;
    }
    return false;
}
//Brace balancing helper
long braceBalance(string s){
    long balance = 0;
    for(auto& c : s){
        if (c == '{') {
            balance++;
        }
        else if(c == '}') balance--;
    }
    return balance;
}
vector<string> fileToArray(string fileName){
    vector<string> fileAsString;
    ifstream fileInput;
    fileInput.open(fileName);
    string line;
    //Create a vector of strings so I don't have to deal with tokens
    while(std::getline(fileInput, line)){
         fileAsString.push_back(line);
    }
    //remove multi line comments
    for(int i = 0; i < fileAsString.size(); i++){
        if(fileAsString[i].find("/*") != string::npos){
            for(int j = i + 1; j < fileAsString.size(); j++){
                if(fileAsString[j].find("*/") != string::npos){
                    fileAsString.erase(fileAsString.begin()+i, fileAsString.begin()+j+1);
                }
            }
        }
    }
    //Remove comments
    for(int i = 0; i < fileAsString.size(); i++){
        if(fileAsString[i].find("//") != string::npos) {
            fileAsString.erase(fileAsString.begin() + i);
            i--;
        }
    }
    //Remove white space
    for(int i = 0; i < fileAsString.size(); i++){
        if(fileAsString[i].find_first_not_of(' ') == std::string::npos){
            fileAsString.erase(fileAsString.begin() + i);
            i--;
        }
    }
    return fileAsString;
}
int max_diff(int a[], int n){
    int size = n;
    int right = 1;
    int left = 0;
    int max = 0;
    for(; (right < n && left < n - 1); right++, left++){
        int thisMax = a[right] - a[left];
        if(thisMax < 0) thisMax = thisMax * -1;
        if(thisMax > max) max = thisMax;
    }
    return max;
}
int main() {
    int a[] = {1, 3, 8, 2};
    cout << max_diff(a, 4);
    return 0;
}
