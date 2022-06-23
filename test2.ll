; ModuleID = "/home/callum/functions_2/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
define double @"myfun"()
{
function:
  %".2" = fadd double 0x4000000000000000, 0x4008000000000000
  ret double 0x0
}
