int printf(char* format, ...);
char * gets (char * str);
char src[1000];
char pattern[100];
int prefix[100];
int n;
int m;

/* KMP algorithm */
void KMP_matching()
{
	int flag;
	int k;
	int q, i;
	flag = 0;
	k = 0;
	/* Compute prefix*/
	for (q = 2; q <= m; q++)
	{
		while (k > 0 && pattern[k] != pattern[q - 1])
			k = prefix[k - 1];
		if (pattern[k] == pattern[q - 1])
			k++;
		prefix[q - 1] = k;
	}
	/* Match!*/
	q = 0;
	for (i = 0; i < n; i++)
	{
		while (q > 0 && pattern[q] != src[i])
			q = prefix[q - 1];
		if (pattern[q] == src[i])
			q++;
		if (q == m) 
		{
			if (flag == 0) {
				printf("%d", i - m + 1);
			}
			else {
				printf(",%d", i - m +1);
			}
			flag = 1;
			/* next match */
			q = prefix[q - 1];
		}
	}
	if (flag == 0) {
		printf("False");
	}
}

int main() {
	printf("please input two strings, first is src, second is pattern\n");
	n = 0;
	m = 0;
	int i;
	i = 0;
	for (i = 0; i < 1000; i++) {
		src[i] = '\0';
	}
	for (i = 0; i < 100; i++) {
		pattern[i] = '\0';
	}
	for (i = 0; i < 100; i++) {
		prefix[i] = 0;
	}
	gets(src);
	gets(pattern);
	for (i = 0; i < 1000; i++) {
		if (src[i] == '\0') {
			n = i;
			break;
		}
		if (src[i] == '\n') {
			n = i;
			break;
		}
	}
	for (i = 0; i < 100; i++) {
		if (pattern[i] == '\0') {
			m = i;
			break;
		}
		if (pattern[i] == '\n') {
			n = i;
			break;
		}
	}
	if (m == 0 || n == 0) {
		printf("empty string");
		return 0;
	}
	KMP_matching();
	return 0;
}