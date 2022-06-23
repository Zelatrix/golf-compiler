; ModuleID = "/home/callum/specifications/golf-compiler/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = bitcast [6 x i8]* @"fstr" to i64*
  %".3" = alloca double
  store double              0x0, double* %".3"
  br label %"loop_start"
loop_start:
  %".6" = load double, double* %".3"
  %".7" = fcmp olt double %".6", 0x4034000000000000
  %".8" = uitofp i1 %".7" to double
  %".9" = fptosi double %".8" to i1
  br i1 %".9", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".11" = load double, double* %".3"
  %".12" = fcmp olt double %".11", 0x4034000000000000
  %".13" = uitofp i1 %".12" to double
  %".14" = fptosi double %".13" to i1
  %".15" = load double, double* %".3"
  %".16" = fcmp oeq double 0x4008000000000000,              0x0
  %".17" = uitofp i1 %".16" to double
  %".18" = frem double %".15", %".17"
  %".19" = load double, double* %".3"
  %".20" = fcmp oeq double 0x4014000000000000,              0x0
  %".21" = uitofp i1 %".20" to double
  %".22" = frem double %".19", %".21"
  %".23" = fptosi double %".18" to i64
  %".24" = fptosi double %".22" to i64
  %".25" = and i64 %".23", %".24"
  %".26" = uitofp i64 %".25" to double
  %".27" = fptosi double %".26" to i1
  br i1 %".27", label %"loop_start.if.if", label %"loop_start.if.else"
loop_start.endif:
  ret void
loop_start.if.if:
  %".29" = call i32 (i64*, ...) @"printf"(i64* %".2", double 0x3ff0000000000000)
  br label %"loop_start.if.endif"
loop_start.if.else:
  %".31" = load double, double* %".3"
  %".32" = fcmp oeq double 0x4008000000000000,              0x0
  %".33" = uitofp i1 %".32" to double
  %".34" = frem double %".31", %".33"
  %".35" = fptosi double %".34" to i1
  br i1 %".35", label %"loop_start.if.else.if", label %"loop_start.if.else.endif"
loop_start.if.endif:
  %".40" = load double, double* %".3"
  %".41" = fcmp oeq double 0x4014000000000000,              0x0
  %".42" = uitofp i1 %".41" to double
  %".43" = frem double %".40", %".42"
  %".44" = fptosi double %".43" to i1
  br i1 %".44", label %"loop_start.if.endif.if", label %"loop_start.if.endif.endif"
loop_start.if.else.if:
  %".37" = call i32 (i64*, ...) @"printf"(i64* %".2", double 0x4000000000000000)
  br label %"loop_start.if.else.endif"
loop_start.if.else.endif:
  br label %"loop_start.if.endif"
loop_start.if.endif.if:
  %".46" = call i32 (i64*, ...) @"printf"(i64* %".2", double 0x4008000000000000)
  br label %"loop_start.if.endif.endif"
loop_start.if.endif.endif:
  %".48" = load double, double* %".3"
  %".49" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".48")
  br label %"loop_start"
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"
declare i32 @"main_fn"(i8 %".1", i64* %".2") 
