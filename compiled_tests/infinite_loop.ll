; ModuleID = "/home/callum/arrays2/codegen.py"
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
  %".6" = fptosi double 0x3ff0000000000000 to i1
  br i1 %".6", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".8" = fptosi double 0x3ff0000000000000 to i1
  %".9" = load double, double* %".3"
  %".10" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".9")
  %".11" = load double, double* %".3"
  %".12" = fadd double %".11", 0x3ff0000000000000
  store double %".12", double* %".3"
  br label %"loop_start"
loop_start.endif:
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
declare i32 @"main_fn"(i8 %".1", i64* %".2") 
