; ModuleID = "/home/callum/specifications-arrays/specifications-arrays/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = alloca double
  store double 0x4000000000000000, double* %".3"
  %".5" = load double, double* %".3"
  %".6" = fmul double %".5", 0x4000000000000000
  %".7" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".6")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"