; ModuleID = "/home/callum/usb/current/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = fcmp olt double 0x4010000000000000, 0x4014000000000000
  %".3" = uitofp i1 %".2" to double
  %".4" = fcmp olt double %".3", 0x4018000000000000
  %".5" = uitofp i1 %".4" to double
  %".6" = bitcast [6 x i8]* @"fstr" to i64*
  %".7" = call i32 (i64*, ...) @"printf"(i64* %".6", double %".5")
  %".8" = fcmp ogt double 0x4010000000000000, 0x4014000000000000
  %".9" = uitofp i1 %".8" to double
  %".10" = fcmp ogt double %".9", 0x4018000000000000
  %".11" = uitofp i1 %".10" to double
  %".12" = bitcast [6 x i8]* @"fstr" to i64*
  %".13" = call i32 (i64*, ...) @"printf"(i64* %".12", double %".11")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1