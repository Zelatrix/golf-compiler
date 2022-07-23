; ModuleID = "/home/callum/fns2/funs_no_errors_v2/functions_no_errors/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %"mybitcast" = bitcast [6 x i8]* @"fstr" to i64*
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
define i64 @"f"() 
{
function:
  %".2" = alloca double
  store double 0x4000000000000000, double* %".2"
  ret i64 0
}
