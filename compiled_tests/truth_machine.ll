; ModuleID = "/home/callum/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"()
{
entry:
  %".2" = alloca double
  store double 0x3ff0000000000000, double* %".2"
  %".4" = load double, double* %".2"
  %".5" = fcmp oeq double %".4",              0x0
  %".6" = uitofp i1 %".5" to double
  %".7" = fptosi double %".6" to i1
  br i1 %".7", label %"entry.if", label %"entry.endif"
entry.if:
  %".9" = bitcast [6 x i8]* @"fstr" to i64*
  %".10" = call i32 (i64*, ...) @"printf"(i64* %".9", double              0x0)
  br label %"entry.endif"
entry.endif:
  %".12" = load double, double* %".2"
  %".13" = fcmp oeq double %".12", 0x3ff0000000000000
  %".14" = uitofp i1 %".13" to double
  %".15" = fptosi double %".14" to i1
  br i1 %".15", label %"entry.endif.if", label %"entry.endif.endif"
entry.endif.if:
  br label %"loop_start"
entry.endif.endif:
  ret void
loop_start:
  %".18" = fptosi double 0x3ff0000000000000 to i1
  br i1 %".18", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".20" = fptosi double 0x3ff0000000000000 to i1
  %".21" = bitcast [6 x i8]* @"fstr" to i64*
  %".22" = call i32 (i64*, ...) @"printf"(i64* %".21", double 0x3ff0000000000000)
  br label %"loop_start"
loop_start.endif:
  br label %"entry.endif.endif"
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1