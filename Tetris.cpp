#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <time.h>

#define cursor SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), a) //управление положением курсора
#define checkl CheckLeft(curBL, curTURN,a)
#define checkr CheckRight(curBL, curTURN,a)
#define checkd CheckDown(curBL, curTURN,a)
#define check Check(curBL, curTURN,a)
#define clear Clear(curBL, curTURN,a)

int block[7][4][4][4] = {
	{
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 1, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 1, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 1, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 1, 1, 0 },
		},
	},
	{
		{ { 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 1, 1, 1, 1 },
		},
		{ { 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 1, 1, 1, 1 },
		},
	},
	{
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 1 },
		{ 0, 0, 0, 1 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 1, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 0, 0 },
		{ 0, 1, 1, 1 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 1, 0, 0 },
		{ 0, 1, 0, 0 },
		},
	},
	{
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 1 },
		{ 0, 1, 0, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 0, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 0, 0, 1 },
		{ 0, 1, 1, 1 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 1, 0, 0 },
		{ 0, 1, 0, 0 },
		{ 0, 1, 1, 0 },
		},
	},
	{
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 1 },
		{ 0, 0, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 0, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 1, 1, 1 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 1, 0 },
		{ 0, 0, 1, 1 },
		{ 0, 0, 1, 0 },
		},
	},
	{
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 0, 1, 1 },
		{ 0, 1, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 1, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 0, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 0, 1, 1 },
		{ 0, 1, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 1, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 0, 1, 0 },
		},
	},
	{
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 0, 1, 1 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 1 },
		{ 0, 0, 1, 1 },
		{ 0, 0, 1, 0 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 0 },
		{ 0, 1, 1, 0 },
		{ 0, 0, 1, 1 },
		},
		{ { 0, 0, 0, 0 },
		{ 0, 0, 0, 1 },
		{ 0, 0, 1, 1 },
		{ 0, 0, 1, 0 },
		},
	}
};

int field[14][23] = {
	{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
	{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1 },
	{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
	{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 },
};

int CheckLeft(int curBL, int curTURN, COORD a){
	for (int i = 0; i < 4; i++){
		for (int j = 0; j < 4; j++){
			if (a.X + j >= 0 && a.X + j <= 13 && a.Y + i >= 0){
				if ((block[curBL][curTURN][i][j] == 1) && (field[a.X + j][a.Y + i] != 0))return 0;
			}
		}
	}
	return 1;
}

int CheckRight(int curBL, int curTURN, COORD a){
	for (int i = 0; i < 4; i++){
		for (int j = 0; j < 4; j++){
			if (a.X + j + 2 >= 0 && a.X + j + 2 <= 13 && a.Y + i >= 0){
				if ((block[curBL][curTURN][i][j] == 1) && (field[a.X + j + 2][a.Y + i] != 0))return 0;
			}
		}
	}
	return 1;
}

int CheckDown(int curBL, int curTURN, COORD a){
	for (int i = 0; i < 4; i++){
		for (int j = 0; j < 4; j++){
			if (a.X + j + 1 >= 0 && a.X + j + 1 <= 13 && a.Y + i + 1 >= 0){
				if ((block[curBL][curTURN][i][j] == 1) && (field[a.X + j + 1][a.Y + i + 1] != 0))return 0;
			}
		}
	}
	return 1;
}

int Check(int curBL, int curTURN, COORD a){
	int nextTURN = (curTURN + 1) % 4;
	for (int i = 0; i < 4; i++){
		for (int j = 0; j < 4; j++){
			if (a.X + j + 1 >= 0 && a.X + j + 1 <= 13 && a.Y + i >= 0){
				if (((block[curBL][nextTURN][i][j] == 1) && (field[a.X + j + 1][a.Y + i] != 0)))return 0;
			}
		}
	}
	return 1;
}

void Clear(int curBL, int curTURN, COORD a){
	cursor;
	COORD b = a;
	for (int i = 0; i < 4; i++){
		a = b;
		a.Y += i;
		cursor;
		if (a.Y >= 0){
			for (int j = 0; j < 4; j++){
				if (block[curBL][curTURN][i][j] == 0){ a.X++; }
				else{
					cursor;
					printf(" ");
					a.X++;
				}
			}
		}
	}
}

void PrintBlock(int curBL, int curTURN, COORD a){
	cursor;
	COORD b = a;
	for (int i = 0; i < 4; i++){
		a = b;
		a.Y += i;
		cursor;
		if (a.Y >= 0){
			for (int j = 0; j < 4; j++){
				if (block[curBL][curTURN][i][j] == 0){ a.X++; }
				else{
					cursor;
					printf("#");
					a.X++;
				}
			}
		}
	}
}
void StartField(){
	COORD a;
	a.X = 0;
	a.Y = 0;
	cursor;
	for (int i = 0; i < 21; i++){
		for (int j = 0; j < 12; j++){
			if (i == 20){ if (j == 0 || j == 11){ printf("|"); } else{ printf("_"); } }
			else{
				if (j == 0 || j == 11)printf("|");
				else{
					printf(" ");
				}
			}
		}
		printf("\n");
	}
	a.X = 21;
	a.Y = 0;
	cursor;
	printf("Control: in game: arrows, Space, pause - Num0, quit - Esc");
	a.Y++;
	cursor;
	printf("menu: choose lvl - Space, start - Enter, exit - Esc");
}

int CheckStr(int y){
	for (int x = 2; x <= 11; x++){
		if (!field[x][y])return 0;
	}
	return 1;
}

int CheckNullStr(int y){
	for (int x = 2; x <= 11; x++){
		if (field[x][y])return 0;
	}
	return 1;
}

void ClearStr(int y){
	COORD a;
	a.X = 1;
	a.Y = y;
	cursor;
	for (int x = 2; x <= 11; x++){
		field[x][y] = 0;
	}
	printf("          ");
	return;
}

void Gravity(int y){
	COORD a;
	a.X = 1;
	a.Y = y;
	if (CheckNullStr(y)&&y>0){
		cursor;
		for (int x = 2; x <= 11; x++){
			field[x][y] = field[x][y-1];
			if (field[x][y - 1]){printf("#");}else{printf(" ");}
		}
		ClearStr(y - 1);
	}
	return;
}



int main(){
	//убирает курсор
	struct _CONSOLE_CURSOR_INFO acur;
	acur.dwSize = 1;
	acur.bVisible = FALSE;
	SetConsoleCursorInfo(GetStdHandle(STD_OUTPUT_HANDLE), &acur);
	//заголовок окна
	char* s = "Tetris";
	SetConsoleTitle((LPCTSTR)s);
	StartField();

	char key = 0;
	int curTURN = 0;
	int nextBL = 0;
	srand(time(NULL));
	int curBL = rand() % 7;
	int count = 0;
	COORD a;
	a.X = 4;
	a.Y = -2;
	COORD ug;
	ug.X = 15;
	ug.Y = 1;
	int level = 1;
	int level0 = level;
	int thisClock = -1000;
	int gameover = 0;

	//menu
	while (1){
		level = 1;
		switch (_getch()){
		case 32:
			a.X = 21;
			a.Y = 2;
			cursor;
			printf("start lvl: ");
			scanf_s("%d", &level);
			a.X = 21;
			a.Y = 2;
			cursor;
			printf("              ");
		case 13:
			StartField();
			//game
			while (1){
				a.X = 15;
				a.Y = 6;
				cursor;
				printf("level:%2.d  count:%2.d", level,count);
				level0 = level;
				for (int x = 2; x <= 11; x++){
					if (field[x][20] == 0){
						a.X = x - 1;
						a.Y = 20;
						cursor;
						printf("_");
					}
				}
				a.X = 4;
				a.Y = -2;
				curBL = nextBL;
				curTURN = 0;
				Clear(nextBL, 0, ug);
				srand(time(NULL));
				nextBL = rand() % 7;
				PrintBlock(nextBL, 0, ug);
				PrintBlock(curBL, curTURN, a);
				for (int x = 2; x <= 11; x++){
					if (field[x][0]){
						gameover = 1;
						a.X = 1;
						a.Y = 1;
						cursor;
						printf("GAME OVER!");
						break;
					}
				}
				if (gameover == 1)break;
				//block
				while (1){
					//falling
					if (thisClock + 1000 - 49 * level0 < clock()){
						if (!checkd){
							for (int i = 0; i < 4; i++){
								for (int j = 0; j < 4; j++){
									if (a.X + j + 1 >= 0 && a.X + j + 1 <= 13 && a.Y + i >= 0){
										if (block[curBL][curTURN][i][j]){
											field[a.X + j + 1][a.Y + i] = block[curBL][curTURN][i][j];
										}
									}
								}
							}
							break;
						}
						clear;
						a.Y++;
						thisClock = clock();
						PrintBlock(curBL, curTURN, a);
					}
					//control
					if (_kbhit()){
						key = _getch();
						if (key == 72){
							if (check){
								clear;
								curTURN = (curTURN + 1) % 4;
								PrintBlock(curBL, curTURN, a);
							}
						}
						if (key == 75){
							if (checkl){
								clear;
								a.X--;
								PrintBlock(curBL, curTURN, a);
							}
						}
						if (key == 77){
							if (checkr){
								clear;
								a.X++;
								PrintBlock(curBL, curTURN, a);
							}
						}
						if (key == 80){
							if (checkd){
								clear;
								a.Y++;
								PrintBlock(curBL, curTURN, a);
							}
						}
						if (key == 48){
							PrintBlock(curBL, curTURN, a);
							_getch();
							continue;
						}
						if (key == 82){
							PrintBlock(curBL, curTURN, a);
							_getch();
							continue;
						}
						if (key == 27)break;
						if (key == 32){
							level0 = 21;
						}
					}
				}
				if (key == 27){
					gameover = 0;
					break;
				}
				for (int i = 20; i >= 0; i--){
					if (CheckStr(i)){ 
						count++;
						ClearStr(i);
					}
				}
				for (int j = 0; j < 4;j++){
					for (int i = 20; i >= 0; i--){
						Gravity(i);
					}
				}
				if (count >= level * 2){
					level++;
					count = 0;
				}
				if (level == 20){
					gameover = 2;
					break;
				}
			}
			a.X = 1;
			for (int y = 0; y <= 20; y++){
				a.Y = y;
				cursor;
				if(y!=20)printf("          ");
				else
					printf("__________"); 
				for (int x = 2; x <= 11; x++){
					field[x][y] = 0;
				}
			}
			if (gameover == 1){
				a.X = 1;
				a.Y = 1;
				cursor;
				printf("GAME OVER!");
				/*a.X = 1;
				a.Y = 20;
				cursor;
				printf("__________");*/
			}
			if (gameover == 2){
				a.X = 2;
				a.Y = 1;
				cursor;
				printf("YOU WIN!");
				/*a.X = 1;
				a.Y = 20;
				cursor;
				printf("__________");*/
			}
			gameover = 0;
			break;
		case 27:
			return 0;
			break;
		}
	}
	cursor;
	printf("     ");
	getchar();
	return 0;
}
