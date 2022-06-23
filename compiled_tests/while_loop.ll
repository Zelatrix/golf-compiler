; ModuleID = "/home/callum/specifications/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = alloca double
  store double 0x4024000000000000, double* %".3"
  br label %"loop_start"
loop_start:
  %".6" = load double, double* %".3"
  %".7" = fcmp ogt double %".6",              0x0
  %".8" = uitofp i1 %".7" to double
  %".9" = fptosi double %".8" to i1
  br i1 %".9", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".11" = load double, double* %".3"
  %".12" = fcmp ogt double %".11",              0x0
  %".13" = uitofp i1 %".12" to double
  %".14" = fptosi double %".13" to i1
  %".15" = load double, double* %".3"
  %".16" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".15")
  %".17" = load double, double* %".3"
  %".18" = fsub double %".17", 0x3ff0000000000000
  store double %".18", double* %".3"
  br label %"loop_start"
loop_start.endif:
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
declare i32 @"main_fn"(i8 %".1", i64* %".2") 
