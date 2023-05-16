; ModuleID = "/home/callum/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  call void @"f"(double 0x3ff0000000000000, double 0x4000000000000000)
  call void @"f"(double 0x4008000000000000, double 0x4010000000000000)
  ret void
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1
define void @"f"(double %"x", double %"y")
{
f:
  %".4" = alloca double
  store double %"x", double* %".4"
  %".6" = alloca double
  store double %"y", double* %".6"
  %".8" = load double, double* %".4"
  %".9" = bitcast [6 x i8]* @"fstr" to i64*
  %".10" = call i32 (i64*, ...) @"printf"(i64* %".9", double %".8")
  %".11" = load double, double* %".4"
  %".12" = fadd double %".11", 0x3ff0000000000000
  store double %".12", double* %".4"
  %".14" = load double, double* %".4"
  %".15" = bitcast [6 x i8]* @"fstr" to i64*
  %".16" = call i32 (i64*, ...) @"printf"(i64* %".15", double %".14")
  %".17" = load double, double* %".6"
  %".18" = bitcast [6 x i8]* @"fstr" to i64*
  %".19" = call i32 (i64*, ...) @"printf"(i64* %".18", double %".17")
  %".20" = load double, double* %".6"
  %".21" = fadd double %".20", 0x4000000000000000
  store double %".21", double* %".6"
  %".23" = load double, double* %".6"
  %".24" = bitcast [6 x i8]* @"fstr" to i64*
  %".25" = call i32 (i64*, ...) @"printf"(i64* %".24", double %".23")
  ret void
}
