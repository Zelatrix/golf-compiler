; ModuleID = "/home/callum/compiler6/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = alloca double
  store double 0x4037800000000000, double* %".2"
  %".4" = alloca double
  store double 0x4033800000000000, double* %".4"
  %".6" = load double, double* @"x"
  %".7" = bitcast [6 x i8]* @"fstr" to i64*
  %".8" = call i32 (i64*, ...) @"printf"(i64* %".7", double %".6")
  %".9" = load double, double* @"y"
  %".10" = bitcast [6 x i8]* @"fstr" to i64*
  %".11" = call i32 (i64*, ...) @"printf"(i64* %".10", double %".9")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1
@"x" = internal global double undef
@"y" = internal global double undef