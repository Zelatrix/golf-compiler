; ModuleID = "/home/callum/compiler/current/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = alloca double
  store double 0x4000000000000000, double* %".2"
  %".4" = load double, double* %".2"
  %".5" = bitcast [6 x i8]* @"fstr" to i64*
  %".6" = call i32 (i64*, ...) @"printf"(i64* %".5", double %".4")
  %".7" = load double, double* %".2"
  %".8" = fadd double %".7", 0x3ff0000000000000
  store double %".8", double* %".2"
  %".10" = load double, double* %".2"
  %".11" = bitcast [6 x i8]* @"fstr" to i64*
  %".12" = call i32 (i64*, ...) @"printf"(i64* %".11", double %".10")
  %".13" = load double, double* %".2"
  %".14" = fadd double %".13", 0x4000000000000000
  store double %".14", double* %".2"
  %".16" = load double, double* %".2"
  %".17" = bitcast [6 x i8]* @"fstr" to i64*
  %".18" = call i32 (i64*, ...) @"printf"(i64* %".17", double %".16")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1