; ModuleID = "/home/callum/functions/functions_2/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i8*
}

declare i32 @"printf"(i8* %".1", ...)

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
define i64 @"myfun"()
{
function:
  %".2" = add i8 2, 3
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2", i8* %".2")
  ret i64 0
}
