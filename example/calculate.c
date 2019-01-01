int printf(char* format, ...);
char * gets (char * str);
char src[1000];
int len;
char operate[1000];
int operate_top;
int number[1000];
int number_top;

int isOperate(char s) {
	if (s == '+' || s == '-' || s == '*' || s == '/') {
		return 1;
	}
	else {
		return 0;
	}
}

int isPart(char s) {
	if (s == '(' || s == ')') {
		return 1;
	}
	else {
		return 0;
	}
}

int isPrior(char s, char t) {
	if (s == '*' || s == '/') {
		if (t == '+' || t == '-') {
			return 1;
		}
	}
	if (t == '(') {
		return 1;
	}
	return 0;
}

int cal() {
	int res;
	int i;
	i = 0;
	res = 0;
	int num;
	num = 0;
	for (i = 0; i < len; i=i+1) {
		if (isOperate(src[i]) || isPart(src[i])) {
			if (isOperate(src[i])) {
				if (operate_top == -1) {
					operate[operate_top + 1] = src[i];
					operate_top=operate_top+1;
				}
				else {
					if (isPrior(src[i], operate[operate_top]) == 1) {
						operate[operate_top + 1] = src[i];
						operate_top=operate_top+1;
					}
					else {
						if (operate[operate_top] == '+') {
							number[number_top - 1] = number[number_top] + number[number_top - 1];
						}
						if (operate[operate_top] == '-') {
							number[number_top - 1] = number[number_top - 1] - number[number_top];
						}
						if (operate[operate_top] == '*') {
							number[number_top - 1] = number[number_top] * number[number_top - 1];
						}
						if (operate[operate_top] == '/') {
							number[number_top - 1] = number[number_top - 1] / number[number_top];
						}
						if (operate[operate_top] == '(') {
							operate[operate_top + 1] = src[i];
							operate_top=operate_top+1;
							continue;
						}
						if (operate[operate_top] != '(') {
							number_top--;
							operate[operate_top] = src[i];
						}
					}
				}
			}
			if (isPart(src[i])) {
				if (src[i] == '(') {
					operate[operate_top + 1] = src[i];
					operate_top=operate_top+1;
				}
				else {
					while (operate[operate_top] != '(') {
						if (operate[operate_top] == '+') {
							number[number_top - 1] = number[number_top] + number[number_top - 1];
						}
						if (operate[operate_top] == '-') {
							number[number_top - 1] = number[number_top - 1] - number[number_top];
						}
						if (operate[operate_top] == '*') {
							number[number_top - 1] = number[number_top] * number[number_top - 1];
						}
						if (operate[operate_top] == '/') {
							number[number_top - 1] = number[number_top - 1] / number[number_top];
						}
						number_top--;
						operate_top--;
					}
					operate_top--;
				}
			}
		}
		else {
			num = num * 10;
			num += src[i] - '0';
			if (i == len - 1 || (i != len-1 && (isOperate(src[i+1]) || isPart(src[i+1])))) {
				number[number_top + 1] = num;
				number_top = number_top+1;
				num = 0;
			} 
		}
	}
	while (operate_top != -1 || number_top != 0)
	{
		if (operate[operate_top] == '+') {
			number[number_top - 1] = number[number_top] + number[number_top - 1];
		}
		if (operate[operate_top] == '-') {
			number[number_top - 1] = number[number_top - 1] - number[number_top];
		}
		if (operate[operate_top] == '*') {
			number[number_top - 1] = number[number_top] * number[number_top - 1];
		}
		if (operate[operate_top] == '/') {
			number[number_top - 1] = number[number_top - 1] / number[number_top];
		}
		number_top--;
		operate_top--;
	}
	return number[0];
}

int main() {
	len = 0;
	operate_top = -1;
	number_top = -1;
	int i;
	i = 0;
	for (i = 0; i < 1000; i=i+1) {
		src[i] = '\0';
		operate[i] = '\0';
		number[i] = 0;
	}
	gets(src);
	for (i = 0; i < 1000; i=i+1) {
		if (src[i] == '\0') {
			len = i;
			break;
		}
		if (src[i] == '\n') {
			len = i;
			break;
		}
	}
	int res;
	res = cal();
	printf("%d", res);
	return 0;
}