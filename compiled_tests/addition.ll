; ModuleID = "/home/callum/fns2/funs_no_errors_v2/functions_no_errors/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = alloca double
  store double 0x4000000000000000, double* %".3"
  %".5" = alloca double
  store double 0x4008000000000000, double* %".5"
  %".7" = alloca double
  %".8" = load double, double* %".3"
  %".9" = load double, double* %".5"
  %".10" = fadd double %".8", %".9"
  store double %".10", double* %".7"
  %".12" = load double, double* %".7"
  %".13" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".12")
  ret void
}

declare dso_local i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"