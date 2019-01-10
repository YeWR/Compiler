int printf(char* format, ...);
char * gets (char * str);
int main() {
	char src[1000];
	int i;
	i = 0;
	for (i = 0; i < 1000; i = i + 1) {
		src[i] = '\0';
	}
	gets(src);
	int m;
	m = 0;
	for (i = 0; i < 1000; i = i + 1) {
		if (src[i] == '\0') {
			m = i;
			break;
		}
	}
	if (m == 0) {
		printf("empty string");
		return 0;
	}
	int flag = 1;
	for (i = 0; i < m; i = i + 1) {
		if (src[i] != src[m - 1 - i]) {
			flag = 0;
			break;
		}
	}
	if (flag == 0) {
		printf("False");
	}
	else {
		printf("True");
	}
	return 0;
}
