; ModuleID = "/home/callum/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = alloca double
  store double 0x4024000000000000, double* %".2"
  br label %"loop_start"
loop_start:
  %".5" = load double, double* %".2"
  %".6" = fcmp ogt double %".5",              0x0
  %".7" = uitofp i1 %".6" to double
  %".8" = fptosi double %".7" to i1
  br i1 %".8", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".10" = load double, double* %".2"
  %".11" = fcmp ogt double %".10",              0x0
  %".12" = uitofp i1 %".11" to double
  %".13" = fptosi double %".12" to i1
  %".14" = load double, double* %".2"
  %".15" = bitcast [6 x i8]* @"fstr" to i64*
  %".16" = call i32 (i64*, ...) @"printf"(i64* %".15", double %".14")
  %".17" = load double, double* %".2"
  %".18" = fsub double %".17", 0x3ff0000000000000
  store double %".18", double* %".2"
  br label %"loop_start"
loop_start.endif:
  ret void
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1