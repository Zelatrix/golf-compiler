; ModuleID = "/home/callum/usb/current/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = alloca double
  store double              0x0, double* %".2"
  %".4" = alloca double
  store double 0x4018000000000000, double* %".4"
  br label %"loop_start"
loop_start:
  %".7" = load double, double* %".2"
  %".8" = load double, double* %".4"
  %".9" = fdiv double %".8", 0x4000000000000000
  %".10" = fcmp olt double %".7", %".9"
  %".11" = uitofp i1 %".10" to double
  %".12" = fptosi double %".11" to i1
  br i1 %".12", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".14" = load double, double* %".2"
  %".15" = load double, double* %".4"
  %".16" = fdiv double %".15", 0x4000000000000000
  %".17" = fcmp olt double %".14", %".16"
  %".18" = uitofp i1 %".17" to double
  %".19" = fptosi double %".18" to i1
  %".20" = load double, double* %".2"
  %".21" = bitcast [6 x i8]* @"fstr" to i64*
  %".22" = call i32 (i64*, ...) @"printf"(i64* %".21", double %".20")
  %".23" = load double, double* %".2"
  %".24" = fadd double %".23", 0x3ff0000000000000
  store double %".24", double* %".2"
  br label %"loop_start"
loop_start.endif:
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1