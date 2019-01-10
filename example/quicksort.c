int printf(char* format, ...);
char * gets(char * str);

int split(int a[], int low, int high)
{
	int part_element = a[low];

	for (;;) {
		while (low < high && part_element <= a[high]) {
			high = high - 1;
		}
		if (low >= high) break;
		a[low] = a[high];
		low = low + 1;

		while (low < high && a[low] <= part_element) {
			low = low + 1;
		}
		if (low >= high) break;
		a[high] = a[low];
		high = high - 1;
	}

	a[high] = part_element;
	return high;
}

void quicksort(int a[], int low, int high)
{
	int middle;

	if (low >= high) return;
	middle = split(a, low, high);
	quicksort(a, low, (middle - 1));
	quicksort(a, (middle + 1), high);
}

int main(void)
{
	char str[1000];
	int i;
	for (i = 0; i < 1000; i++) {
		str[i] = '\0';
	}
	gets(str);
	int a[1000];
	int k = 0;
	int temp = 0;
	int flag = 0;
	for (i = 0; i < 1000; i++) {
		if (str[i] == '\0') {
			flag = 0;
			a[k] = temp;
			break;
		}
		else if (str[i] == ' ') {
			flag = 0;
			a[k] = temp;
			k = k + 1;
		}
		else {
			if (flag == 1) {
				temp = temp * 10;
				temp = temp + str[i] - '0';
			}
			else {
				temp = 0;
				flag = 1;
				temp = temp * 10;
				temp = temp + str[i] - '0';
			}
		}
	}

	quicksort(a, 0, k);
	
	for (i = 0; i < k+1; i++) {
		printf("%d ", a[i]);
	}
	printf("\n");
	return 0;
}


