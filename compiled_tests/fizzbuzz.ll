; ModuleID = "/home/callum/usb/current/functions/arguments/codegen.py"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

define void @"main"() 
{
entry:
  %".2" = alloca double
  store double              0x0, double* %".2"
  br label %"loop_start"
loop_start:
  %".5" = load double, double* %".2"
  %".6" = fcmp olt double %".5", 0x4034000000000000
  %".7" = uitofp i1 %".6" to double
  %".8" = fptosi double %".7" to i1
  br i1 %".8", label %"loop_start.if", label %"loop_start.endif"
loop_start.if:
  %".10" = load double, double* %".2"
  %".11" = fcmp olt double %".10", 0x4034000000000000
  %".12" = uitofp i1 %".11" to double
  %".13" = fptosi double %".12" to i1
  %".14" = load double, double* %".2"
  %".15" = frem double %".14", 0x4008000000000000
  %".16" = fcmp oeq double %".15",              0x0
  %".17" = uitofp i1 %".16" to double
  %".18" = load double, double* %".2"
  %".19" = frem double %".18", 0x4014000000000000
  %".20" = fcmp oeq double %".19",              0x0
  %".21" = uitofp i1 %".20" to double
  %".22" = fptosi double %".17" to i64
  %".23" = fptosi double %".21" to i64
  %".24" = and i64 %".22", %".23"
  %".25" = uitofp i64 %".24" to double
  %".26" = fptosi double %".25" to i1
  br i1 %".26", label %"loop_start.if.if", label %"loop_start.if.else"
loop_start.endif:
  ret void
loop_start.if.if:
  %".28" = bitcast [6 x i8]* @"fstr" to i64*
  %".29" = call i32 (i64*, ...) @"printf"(i64* %".28", double 0x3ff0000000000000)
  %".30" = load double, double* %".2"
  %".31" = fadd double %".30", 0x3ff0000000000000
  store double %".31", double* %".2"
  br label %"loop_start.if.endif"
loop_start.if.else:
  %".34" = load double, double* %".2"
  %".35" = frem double %".34", 0x4008000000000000
  %".36" = fcmp oeq double %".35",              0x0
  %".37" = uitofp i1 %".36" to double
  %".38" = fptosi double %".37" to i1
  br i1 %".38", label %"loop_start.if.else.if", label %"loop_start.if.else.endif"
loop_start.if.endif:
  %".47" = load double, double* %".2"
  %".48" = frem double %".47", 0x4014000000000000
  %".49" = fcmp oeq double %".48",              0x0
  %".50" = uitofp i1 %".49" to double
  %".51" = fptosi double %".50" to i1
  br i1 %".51", label %"loop_start.if.endif.if", label %"loop_start.if.endif.endif"
loop_start.if.else.if:
  %".40" = bitcast [6 x i8]* @"fstr" to i64*
  %".41" = call i32 (i64*, ...) @"printf"(i64* %".40", double 0x4000000000000000)
  %".42" = load double, double* %".2"
  %".43" = fadd double %".42", 0x3ff0000000000000
  store double %".43", double* %".2"
  br label %"loop_start.if.else.endif"
loop_start.if.else.endif:
  br label %"loop_start.if.endif"
loop_start.if.endif.if:
  %".53" = bitcast [6 x i8]* @"fstr" to i64*
  %".54" = call i32 (i64*, ...) @"printf"(i64* %".53", double 0x4008000000000000)
  %".55" = load double, double* %".2"
  %".56" = fadd double %".55", 0x3ff0000000000000
  store double %".56", double* %".2"
  br label %"loop_start.if.endif.endif"
loop_start.if.endif.endif:
  %".59" = load double, double* %".2"
  %".60" = bitcast [6 x i8]* @"fstr" to i64*
  %".61" = call i32 (i64*, ...) @"printf"(i64* %".60", double %".59")
  %".62" = load double, double* %".2"
  %".63" = fadd double %".62", 0x3ff0000000000000
  store double %".63", double* %".2"
  br label %"loop_start"
}

declare i32 @"printf"(i64* %".1", ...) 

@"fstr" = internal constant [6 x i8] c"%lf \0a\00", align 1