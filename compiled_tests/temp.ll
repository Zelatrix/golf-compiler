; ModuleID = "D:\early-deliverable\codegen.py"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*                           ; Lines 2 and 3 allocate space for the variable in memory
  %".3" = alloca double
  store double 0x4000000000000000, double* %".3"                      ; Store the value 3 in a variable
  %".5" = load double, double* %".3"                                  ; Load the variable's value
  %".6" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".5")    ; Print out the value of the variable
  %".7" = fadd double %".5", 0x4008000000000000                       ; Add 3 to the value of the loaded variable
  %".8" = load double, double* %".3"                                  ; Put the new value back into memory
  %".9" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".7")    ; Print out the new value
  ret void
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"