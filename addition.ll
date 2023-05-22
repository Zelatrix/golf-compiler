; ModuleID = "/home/callum/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = alloca double
  store double 0x4000000000000000, double* %".2"
  %".4" = alloca double
  store double 0x4008000000000000, double* %".4"
  %".6" = alloca double
  %".7" = load double, double* %".2"
  %".8" = load double, double* %".4"
  %".9" = fadd double %".7", %".8"
  store double %".9", double* %".6"
  %".11" = load double, double* %".6"
  %".12" = bitcast [2 x i8]* @"fstr" to i64*
  %".13" = call i32 (i64*, ...) @"printf"(i64* %".12", double %".11")
  ret void
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [2 x i8] c"%s", align 1