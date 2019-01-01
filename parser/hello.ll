declare i32 @"printf"(i8 %".1")

define i32 @"c"()
{
c:
  ret i32 0
}

define i32 @"main"()
{
main:
  %"a" = alloca i32
  store i32 1, i32* %"a"
  %".3" = load i32, i32* %"a"
  %".4" = call i32 @"printf"(i8 "asdas")
  %"b" = alloca i32
  %".5" = sub i32 4, 5
  %".6" = mul i32 %".5", 6
  %".7" = add i32 3, %".6"
  store i32 %".7", i32* %"b"
  br label %".10"
.9:
  br label %".24"
.10:
  %"i" = alloca i32
  store i32 1, i32* %"i"
  br label %".11"
.11:
  %".16" = load i32, i32* %"i"
  %".17" = icmp slt i32 %".16", 2
  %".18" = icmp ne i1 %".17", 0
  br i1 %".18", label %".12", label %".9"
.12:
  store i32 3, i32* %"i"
  %"b.1" = alloca i32
  store i32 0, i32* %"b.1"
  br label %".11"
.23:
  ret i32 0
.24:
  %"i.1" = alloca i32
  store i32 0, i32* %"i.1"
  br label %".25"
.25:
  %".30" = load i32, i32* %"i.1"
  %".31" = icmp slt i32 %".30", 3
  %".32" = icmp ne i1 %".31", 0
  br i1 %".32", label %".26", label %".23"
.26:
  store i32 4, i32* %"i.1"
  %"a.1" = alloca i32
  store i32 1, i32* %"a.1"
  br label %".25"
}