; ModuleID = "D:\early-deliverable\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = alloca double
  store double 0x4024000000000000, double* %".3"

entry.cond:
  %".5" = load double, double* %".3"
  %".6" = fcmp ogt double %".5",              0x0
  %".7" = uitofp i1 %".6" to double
  %".8" = fptosi double %".7" to i1
  br i1 %".8", label %"entry.if", label %"entry.endif"

entry.if:
  %".10" = load double, double* %".3"
  %".11" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".10")
  %".12" = load double, double* %".3"
  %".13" = fsub double %".12", 0x3ff0000000000000
  store double %".13", double* %".3"
  br label %"entry.endif"

entry.endif:
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"