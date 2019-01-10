int f(int a)
{
    int ans = a;
	if (a > 10){
	    ans = ans + f(a);
	}
	return ans;
}

int main()
{
    int a = 1;
	f(2);
	return 0;
}