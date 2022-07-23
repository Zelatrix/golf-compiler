; ModuleID = "/home/callum/specifications-arrays/specifications-arrays/codegen.py"
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
  %".7" = load double, double* %".5"
  %".8" = load double, double* %".3"
  %".9" = fadd double %".8", %".7"
  store double %".9", double* %".3"
  %".11" = load double, double* %".3"
  %".12" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".11")
  %".13" = load double, double* %".5"
  %".14" = load double, double* %".3"
  %".15" = fsub double %".14", %".13"
  store double %".15", double* %".3"
  %".17" = load double, double* %".3"
  %".18" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".17")
  %".19" = load double, double* %".5"
  %".20" = load double, double* %".3"
  %".21" = fmul double %".20", %".19"
  store double %".21", double* %".3"
  %".23" = load double, double* %".3"
  %".24" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".23")
  %".25" = load double, double* %".5"
  %".26" = load double, double* %".3"
  %".27" = fdiv double %".26", %".25"
  store double %".27", double* %".3"
  %".29" = load double, double* %".3"
  %".30" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".29")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"