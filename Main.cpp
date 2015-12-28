#include "MyUtils.h"
#include <iostream>
#include <string>

using namespace My;

int main()
{
	string s;


	//Try: d/dx ((1+2*x^3)*x)^3/x == (3*((1+2*x^3)*x)^2*(2*3*x^2*x+1+2*x^3)*x - ((1+2*x^3)*x)^3)/x^2
	{
		ParseTree parser("((1+2*x^3)*x)^3/x");
		parser.print();
		cout << endl << endl;
		parser.differentiate();
		parser.print();
	}

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
