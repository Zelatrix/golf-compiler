; ModuleID = "/home/callum/strings-current/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  %"str_const" = alloca [15 x i8]
  store [15 x i8] c"Hello, World!\0a\00", [15 x i8]* %"str_const"
  %".3" = bitcast [2 x i8]* @"fstr" to i64*
  %".4" = call i32 (i64*, ...) @"printf"(i64* %".3", [15 x i8]* %"str_const")
  %"str_const.1" = alloca [17 x i8]
  store [17 x i8] c"Goodbye, World!\0a\00", [17 x i8]* %"str_const.1"
  %".6" = bitcast [2 x i8]* @"fstr" to i64*
  %".7" = call i32 (i64*, ...) @"printf"(i64* %".6", [17 x i8]* %"str_const.1")
  ret void
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [2 x i8] c"%s", align 1