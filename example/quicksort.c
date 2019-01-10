int printf(char* format, ...);
char * gets(char * str);
int a[1000];

int split(int low, int high)
{
	int part_element = a[low];

	while (1) {
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

void quicksort(int low, int high)
{
	int middle;

	if (low < high)
	{
		middle = split(low, high);
		int middle1 = middle - 1;
		quicksort(low, middle1);
		int middle2 = middle + 1;
		quicksort(middle2, high);
	}
}

int main(void)
{
	char str[1000];
	int i;
	for (i = 0; i < 1000; i = i + 1) {
		str[i] = '\0';
	}
	gets(str);
	int k = 0;
	int temp = 0;
	int flag = 0;
	for (i = 0; i < 1000; i = i + 1) {
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

	quicksort(0, k);
	
	for (i = 0; i < k+1; i = i + 1) {
		printf("%d ", a[i]);
	}
	printf("\n");
	return 0;
}


