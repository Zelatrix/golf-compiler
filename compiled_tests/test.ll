; ModuleID = "/home/callum/specifications/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = alloca double
  store double              0x0, double* %".3"
  %".5" = alloca double
  store double 0x4000000000000000, double* %".5"
  br label %"loop_start"
loop_start:
  %".8" = load double, double* %".3"
  %".9" = fcmp olt double %".8", 0x4024000000000000
  %".10" = uitofp i1 %".9" to double
  %".11" = fptosi double %".10" to i1
  br i1 %".11", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".13" = load double, double* %".3"
  %".14" = fcmp olt double %".13", 0x4024000000000000
  %".15" = uitofp i1 %".14" to double
  %".16" = fptosi double %".15" to i1
  %".17" = load double, double* %".3"
  %".18" = load double, double* %".5"
  %".19" = fmul double %".17", %".18"
  %".20" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".19")
  %".21" = load double, double* %".3"
  %".22" = fadd double %".21", 0x3ff0000000000000
  store double %".22", double* %".3"
  br label %"loop_start"
loop_start.endif:
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
declare i32 @"main_fn"(i8 %".1", i64* %".2") 
