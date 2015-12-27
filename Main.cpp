#include "MyUtils.h"
#include <iostream>
#include <string>

using namespace My;

int main()
{
	string s;

	
	
	while (cin >> s)
	{
		try {
			ParseTree parser(s);
			parser.print();
			cout << endl << endl;
			parser.differentiate();
			parser.print();
		}
		catch (exception e) {
			cout << endl << e.what() << endl << endl;
		}
	}
	return 0;
}
