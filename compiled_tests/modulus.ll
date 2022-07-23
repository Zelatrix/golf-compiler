; ModuleID = "/home/callum/usb/current/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = frem double 0x4010000000000000, 0x4014000000000000
  %".3" = fcmp oeq double %".2", 0x4010000000000000
  %".4" = uitofp i1 %".3" to double
  %".5" = bitcast [6 x i8]* @"fstr" to i64*
  %".6" = call i32 (i64*, ...) @"printf"(i64* %".5", double %".4")
  %".7" = frem double 0x4010000000000000, 0x4014000000000000
  %".8" = fcmp one double %".7", 0x4010000000000000
  %".9" = uitofp i1 %".8" to double
  %".10" = bitcast [6 x i8]* @"fstr" to i64*
  %".11" = call i32 (i64*, ...) @"printf"(i64* %".10", double %".9")
  %".12" = frem double 0x4010000000000000, 0x4014000000000000
  %".13" = fcmp oeq double %".12", 0x4010000000000000
  %".14" = uitofp i1 %".13" to double
  %".15" = bitcast [6 x i8]* @"fstr" to i64*
  %".16" = call i32 (i64*, ...) @"printf"(i64* %".15", double %".14")
  %".17" = frem double 0x4010000000000000, 0x4014000000000000
  %".18" = fcmp one double %".17", 0x4010000000000000
  %".19" = uitofp i1 %".18" to double
  %".20" = bitcast [6 x i8]* @"fstr" to i64*
  %".21" = call i32 (i64*, ...) @"printf"(i64* %".20", double %".19")
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1