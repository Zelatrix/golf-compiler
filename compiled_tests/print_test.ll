; ModuleID = "/home/callum/golf-compiler/codegen.py"
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
  ret void
}

declare i32 @"printf"(i64* %".1", ...)

declare i64 @"printstr"(i64* %".1", ...)

@".str" = internal constant [15 x i8] c"Goodbye, World!", align 1
@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1