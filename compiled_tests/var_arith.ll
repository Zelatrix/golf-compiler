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
  %".6" = fadd double %".5", 0x4008000000000000
  %".7" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".6")
  %".8" = load double, double* %".3"
  %".9" = fdiv double %".8", 0x4000000000000000
  %".10" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".9")
  %".11" = load double, double* %".3"
  %".12" = fmul double %".11", 0x4000000000000000
  %".13" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".12")
  %".14" = load double, double* %".3"
  %".15" = fsub double %".14", 0x4000000000000000
  %".16" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".15")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"