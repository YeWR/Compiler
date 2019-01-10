char src[1000];
char pattern[100];
int prefix[100];
int n;
int m;

int printf(char* format, ...);
char * gets (char * str);

/* KMP algorithm */
void KMP_matching()
{
	int flag = 0;
	int k = 0;
	int q = 0;
	/* Compute prefix*/
	for (q = 2; q <= m; q=q+1)
	{
		while (k > 0 && pattern[k] != pattern[q - 1])
			k = prefix[k - 1];
		if (pattern[k] == pattern[q - 1])
			k=k+1;
		prefix[q - 1] = k;
	}
	/* Match!*/
	q = 0;
	for (int j = 0; j < n; j=j+1)
	{
		while (q > 0 && pattern[q] != src[j])
			q = prefix[q - 1];
		if (pattern[q] == src[j])
			q=q+1;
		if (q == m)
		{
			if (flag == 0) {
			    int temp1 = j - m +1;
				printf("%d", temp1);
			}
			else {
			    int temp2 = j - m +1;
				printf(",%d", temp2);
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
	for (int i = 0; i < 1000; i=i+1) {
		src[i] = '\0';
	}
	for (int i = 0; i < 100; i=i+1) {
		pattern[i] = '\0';
	}
	for (int i = 0; i < 100; i=i+1) {
		prefix[i] = 0;
	}
	gets(src);
	gets(pattern);
	for (int i = 0; i < 1000; i=i+1) {
		if (src[i] == '\0') {
			n = i;
			break;
		}
		if (src[i] == '\n') {
			n = i;
			break;
		}
	}
	for (int i = 0; i < 100; i=i+1) {
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
