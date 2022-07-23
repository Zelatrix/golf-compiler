; ModuleID = "/home/callum/compiler-files/current/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = alloca double
  store double              0x0, double* %".2"
  %".4" = alloca double
  store double              0x0, double* %".4"
  br label %"loop_start"
loop_start:
  %".7" = load double, double* %".2"
  %".8" = fcmp ole double %".7", 0x4024000000000000
  %".9" = uitofp i1 %".8" to double
  %".10" = fptosi double %".9" to i1
  br i1 %".10", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".12" = load double, double* %".2"
  %".13" = fcmp ole double %".12", 0x4024000000000000
  %".14" = uitofp i1 %".13" to double
  %".15" = fptosi double %".14" to i1
  br label %"loop_start.1"
loop_start.endif:
  ret void
loop_start.1:
  %".17" = load double, double* %".4"
  %".18" = fcmp ole double %".17", 0x4024000000000000
  %".19" = uitofp i1 %".18" to double
  %".20" = fptosi double %".19" to i1
  br i1 %".20", label %"loop_start.1.if", label %"loop_start.1.endif"
loop_start.1.if:
  %".22" = load double, double* %".4"
  %".23" = fcmp ole double %".22", 0x4024000000000000
  %".24" = uitofp i1 %".23" to double
  %".25" = fptosi double %".24" to i1
  %".26" = load double, double* %".2"
  %".27" = bitcast [6 x i8]* @"fstr" to i64*
  %".28" = call i32 (i64*, ...) @"printf"(i64* %".27", double %".26")
  %".29" = load double, double* %".4"
  %".30" = bitcast [6 x i8]* @"fstr" to i64*
  %".31" = call i32 (i64*, ...) @"printf"(i64* %".30", double %".29")
  %".32" = load double, double* %".4"
  %".33" = fadd double %".32", 0x3ff0000000000000
  store double %".33", double* %".4"
  br label %"loop_start.1"
loop_start.1.endif:
  %".36" = load double, double* %".2"
  %".37" = fadd double %".36", 0x3ff0000000000000
  store double %".37", double* %".2"
  br label %"loop_start"
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1