; ModuleID = "/home/callum/functions/functions_no_errors/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
define i64 @"myfun"() 
{
function:
  %".2" = alloca double
  store double 0x4000000000000000, double* %".2"
  %".4" = alloca double
  store double 0x4008000000000000, double* %".4"
  %".6" = alloca double
  %".7" = load double, double* %".2"
  %".8" = load double, double* %".4"
  %".9" = fadd double %".7", %".8"
  store double %".9", double* %".6"
  ret i64 0
}
