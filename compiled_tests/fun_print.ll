; ModuleID = "/home/callum/usb/current/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  call void @"f"()
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1
define void @"f"() 
{
f:
  %".2" = alloca double
  store double 0x4000000000000000, double* %".2"
  %".4" = load double, double* %".2"
  %".5" = bitcast [6 x i8]* @"fstr" to i64*
  %".6" = call i32 (i64*, ...) @"printf"(i64* %".5", double %".4")
  ret void
}

define void @"g"(i32 %"f") 
{
g:
  %".3" = alloca i32
  store i32 %"f", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = bitcast [6 x i8]* @"fstr" to i64*
  %".7" = call i32 (i64*, ...) @"printf"(i64* %".6", i32 %".5")
  ret void
}
