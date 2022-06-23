; ModuleID = "/home/callum/functions/functions_2/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = fsub double 0x4014000000000000, 0x3ff0000000000000
  %".4" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".3")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"