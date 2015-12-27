#include <vector>
#include <iostream>
#include <string>

namespace My
{
	using namespace std;

	enum TokenType { Operators, lBracket, rBracket, Num, Var, Power, None };

	class Token
	{
	private:
		char _symbol; // "+", "-", "*", "/"
		TokenType _type;

		TokenType kind(char symbol)
		{

			if (symbol == '+' || symbol == '*' ||
				symbol == '-' || symbol == '/' || 
				symbol == '^')
				return TokenType::Operators;
			else
				if (symbol == '^')
				return TokenType::Power;
			else 
				if (symbol == '(')
				return TokenType::lBracket;
			else 
				if (symbol == ')')
				return TokenType::rBracket;
			else
				if ('a' <= symbol && symbol <= 'z')
				return TokenType::Var;
			else 
				if ('0' <= symbol && symbol <= '9')
				return TokenType::Num;
			else
				return None;
		}

	public:
		Token() : _type(None) { } 
		Token(char symbol) : _symbol(symbol), _type(kind(symbol)) { }

		bool operator== (Token& other) const
		{
			if (other._symbol == _symbol
				&& other._type == _type)
				return true;
			return false;
		}
		
		TokenType type() const	{ return _type; }
		char symbol() const		{ return _symbol; }

	};

	struct Node
	{

		Node* left	= nullptr;
		Node* right = nullptr;
		Token token;

		Node& operator= (Node& other)
		{
			left = other.left;
			right = other.right;
			token = Token(other.token);
			return *this;
		}

		Node() { }
		Node(char symbol) : token(symbol)		{ }
		Node(const Token& token) : token(token) { }
		Node(const Node* node)
		{
			if (node == nullptr)
				throw exception("Node(): thought overthought, it happened.");
			else
				token = node->token;
			left =	(node->left != nullptr) ? new Node(node->left) : nullptr;
			right = (node->right != nullptr) ? new Node(node->right) : nullptr;
		}

		~Node()
		{
			delete left;
			delete right;
		}

	};

	class ParseTree
	{
	private:
		Node* root		= new Node;
		
		int lowest_priority(string in) {
			int index = -1;
			int lowest = 0;
			int temp = 0;
			int empower = 0;

			for (int i = 0; i < in.size(); i++)
			{
				switch (in[i]) {

				case('(') : 
					empower += 3;
					break;

				case(')') :
					empower -= 3;
					break;

				case('+') :
				case('-') :
				case('*') :
				case('/') :
				case('^') :
					temp = 
						in[i] == '+' || in[i] == '-' ? 1 : 
						in[i] == '/' || in[i] == '*' ? 2 : 
						in[i] == '^'				 ? 3 : 0;
					temp += empower;
					if (temp < lowest || lowest == 0) {
						lowest = temp;
						index = i;
					}

				}

				if (empower < 0) throw exception("ParseTree: Wrong brackets1 input.");
			}

			if (empower > 0) throw exception("ParseTree: Wrong brackets2 input.");

			return index;
		}

		void Parse(string in, Node* entry)
		{
			if (in[0] == '(' && in[in.size() - 1] == ')') 
			{
				int count = 0;
				bool erasing = true;
				for (int i = 1; i < in.size() - 1; i++) {
					if (in[i] == ')') count -= 2;
					if (in[i] == '(') count += 2;
					if (count < 0) erasing = false;
				}
				if (erasing) {
					in.erase(0, 1);
					in.erase(in.size() - 1, 1);
				}
			}
			int lowest = lowest_priority(in);
			string left;
			string right;

			// if lowest is OK, then
			if (lowest != -1) {
				char* temp = nullptr;
				if (entry != nullptr) 
				{
					entry->token = Token(in[lowest]);
					entry->left = new Node;
					entry->right = new Node;
					Parse(in.substr(0, lowest),							 entry->left);
					Parse(in.substr(lowest + 1, in.size() - lowest - 1),	 entry->right);
				}
				else
					throw exception("ParseTree: null Entry Pointer.");

			}
			// if not, no more expressions being added, only vars & nums 
			else
				if (in.size() != 1)
					throw exception("ParseTree: Bad length or something.");
				else
				{
					if (entry != nullptr) {
						entry->token = Token(in[0]);
					}
				}
		}

		int get_power_base(string& in, int pos)
		{
			//Pre-format function, can be applied before Parse()
			bool error = false;
			int brackets = 0;
			Token* previous = new Token(in[pos+1]);
			Token* current = nullptr;
			while (pos >= 0)
			{
				current = new Token(in[pos]);

				if (current->type() == rBracket) brackets++;
				if (current->type() == lBracket) brackets--;

				switch (current->type())
				{
				case(Power) :
					if (previous->type() != Num)
						error = true;
					break;

				case('(') : case(Operators) :
					if (previous->type() != Var && previous->type() != Num &&
						previous->type() != lBracket)
						error = true;
					break;

				case(Num) : case(Var) : case(')') :
					if (previous->type() != Power && previous->type() != Operators &&
						previous->type() != rBracket)
						error = true;
					break;
				}

				if (error) throw exception("Wrong expression input.");

				if (brackets == 0)
					if (current->type() == Var || current->type() == Num ||
						current->type() == lBracket)
						return pos;

				delete previous;
				previous = current;

				pos--;
			}
			throw exception("Somewhat wrong expression O_o.");
		}

		//replace powers by multiplication:
		//from x^a to x*x*x*....*x representation
/*		void open_powers(string& in)
		{
			int border = 0;
			for (int i = in.size() - 1; i >= 0; i--)
			{
				if (in[i] == ' ') in.erase(i, 1);
				if (in[i] == '^')
				{
					if (i + 1 >= in.size())
						throw exception("ParseTree: Wrong input (...)^c input, 'c' should be const.");

					border = get_power_base(in, i);
					string left = in.substr(0, border);
					string mid = in.substr(border, i - border);
					string duplicate = mid;
					string right;
					right =
						(i + 2 < in.size())
						? right = in.substr(i + 2, in.size() - i - 2)
						: right = "";
					for (int j = 0; j < in[i + 1] - '0' - 1; j++) {
						duplicate += "*" + mid;
					}

					in = left + duplicate + right;
					i = in.size() - 1;
				}
			}
		}
*/
		//void renew(string in)
		//{
		//	delete root;
		//	root = new Node;

		//	if (lowest_priority(in) < 0)
		//		throw exception("ParseTree: Wrong input, brackets assumed.");
		//	//open_powers(in);

		//	Parse(in, root);

		//}

		void fold() // Свертка выражений
		{

		}
	public:
		ParseTree(string in)
		{
			if (lowest_priority(in) < 0) 
				throw exception("ParseTree: Wrong input, brackets assumed.");
			//open_powers(in);

			Parse(in, root);
		}

		void differentiate(Node* entry = nullptr)
		{
			if (entry == nullptr) entry = root;


			
			
			/*Node* minus;
			Node* subtr;*/
			switch (entry->token.type()) {

			case(Num) :
				entry->token = Token('0');
				return;

			case(Var) :
				entry->token = Token('1');
				return;
			}

			char ch;

			Node* power;
			Node* div;
			Node* plus;
			Node* minus;
			Node* mult1;
			Node* mult2;
			Node* mult;

			switch (entry->token.symbol()) {

			case('^') :

				ch = entry->right->token.symbol();
				
				
				if ( ch >= '2') 
				{

					mult1 = new Node('*');
					mult2 = new Node('*');

					if (ch == '2') 
					{
						mult1->left = new Node('2');
						mult1->right = new Node(entry->left);
					}

					else 

					{
						power = new Node(entry);
						power->right->token = Token(char(ch) - 1);

						mult1->left = new Node(entry->right->token.symbol());
						mult1->right = power;
					}

					mult2->left = mult1;
					mult2->right = new Node(entry->left);

					//Clean mem
					delete entry->left;
					delete entry->right;
					*entry = *mult2;

					mult2->left = nullptr;
					mult2->right = nullptr;
					delete mult2;

					//Was suuuuch a bug: differentiate(mult2->right);
					differentiate(entry->right);
					
				} 
				
				else
			
				if (ch == '1') {
					delete entry->right;
					*entry = *entry->left;
					differentiate(entry);
				}

				else

				if (ch == '0') {
					delete entry->left;
					delete entry->right;
					entry->left = nullptr;
					entry->right = nullptr;
					entry->token = Token('0');
				}

				break;

			case('/'):

				div = new Node('/');
				minus = new Node('-');
				mult1 = new Node('*');
				mult2 = new Node('*');

				minus->left = mult1;
				minus->right = mult2;

				mult1->left = new Node(entry->left);
				mult2->left = new Node(entry->left);
				//          ...
				//		    (-) minus
				//		   /	\
				//        /		 \
				//       /		  \
				//      /          \
				//    (*)  mult1   (*)  mult2
				//   /   \		  /   \
				//  /     \	     /     \
				// f'(x)  g(x) f(x)    g'(x)
				mult1->right = new Node(entry->right);
				mult2->right = new Node(entry->right);

				div->left = minus;
				div->right = new Node('^');
				div->right->left = new Node(entry->right);
				div->right->right = new Node('2');

				//Clean mem
				delete entry->left;
				delete entry->right;
				*entry = *div;
				
				div->left = nullptr;
				div->right = nullptr;
				delete div;

				differentiate(mult1->left);
				differentiate(mult2->right);

				break;

			case('*'):

				plus = new Node('+');
				mult1 = new Node('*');
				mult2 = new Node('*');

				plus->left = mult1;
				plus->right= mult2;
				
				mult1->left = new Node(entry->left);
				mult2->left = new Node(entry->left);
				//		    (+) plus
				//		   /	\
				//        /		 \
				//       /		  \
				//      /          \
				//    (*)  mult1   (*)  mult2
				//   /   \		  /   \
				//  /     \	     /     \
				// f'(x)  g(x) f(x)    g'(x)
				mult1->right = new Node(entry->right);
				mult2->right = new Node(entry->right);

				//Clean mem
				delete entry->left;
				delete entry->right;
				*entry = *plus;

				plus->left = nullptr;
				plus->right = nullptr;
				delete plus;

				differentiate(mult1->left);
				differentiate(mult2->right);

				break;

			case('+') : case('-') :
				differentiate(entry->left);
				differentiate(entry->right);

				break;

			}

		}
		

		void print(Node* entry = nullptr)
		{
			if (entry == nullptr) entry = root;

			bool lbrackets = false;
			bool rbrackets = false;

			if (entry->token.symbol() == '^' )
			{
				if (entry->left->token.symbol() == '*' ||
					entry->left->token.symbol() == '/' )
					lbrackets = true;

				if (entry->right->token.symbol() == '*' ||
					entry->right->token.symbol() == '/' )
					rbrackets = true;
			}

			if (entry->token.symbol() == '*' ||
				entry->token.symbol() == '/' ||
				entry->token.symbol() == '^')
			{
				if (entry->left->token.symbol() == '+' ||
					entry->left->token.symbol() == '-' )
					lbrackets = true;

				if (entry->right->token.symbol() == '+' ||
					entry->right->token.symbol() == '-' )
					rbrackets = true;
			}

			if (entry->left != nullptr) 
			{
				if (lbrackets) cout << '(';
				print(entry->left);
				if (lbrackets) cout << ')';
			}
			
			cout << entry->token.symbol(); _sleep(10);

			if (entry->right != nullptr) 
			{
				if (rbrackets) cout << '(';
				print(entry->right);
				if (rbrackets) cout << ')';
			}

		}
	};



}
