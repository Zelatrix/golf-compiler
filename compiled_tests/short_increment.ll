; ModuleID = "/home/callum/functions/functions_2/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = alloca double
  store double 0x4024000000000000, double* %".3"
  %".5" = load double, double* %".3"
  %".6" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".5")
  %".7" = load double, double* %".3"
  %".8" = fadd double %".7", 0x3ff0000000000000
  store double %".8", double* %".3"
  %".10" = load double, double* %".3"
  %".11" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".10")
  %".12" = alloca double
  store double 0x4024000000000000, double* %".12"
  %".14" = load double, double* %".12"
  %".15" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".14")
  %".16" = load double, double* %".12"
  %".17" = fsub double %".16", 0x3ff0000000000000
  store double %".17", double* %".12"
  %".19" = load double, double* %".12"
  %".20" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".19")
  %".21" = alloca double
  store double 0x4024000000000000, double* %".21"
  %".23" = load double, double* %".21"
  %".24" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".23")
  %".25" = load double, double* %".21"
  %".26" = fmul double %".25", 0x4000000000000000
  store double %".26", double* %".21"
  %".28" = load double, double* %".21"
  %".29" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".28")
  %".30" = alloca double
  store double 0x4024000000000000, double* %".30"
  %".32" = load double, double* %".30"
  %".33" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".32")
  %".34" = load double, double* %".30"
  %".35" = fdiv double %".34", 0x4014000000000000
  store double %".35", double* %".30"
  %".37" = load double, double* %".30"
  %".38" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".37")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"