; ModuleID = "/home/callum/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  ret void
}

declare i32 @"printf"(i64* %".1", ...)

@".str" = internal constant [15 x i8] c"Goodbye, World!", align 1
@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1