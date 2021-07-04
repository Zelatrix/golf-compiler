define void @"main"()
{
    entry:
      %".2" = bitcast [6 x i8]* @"fstr" to i64*
      %".3" = alloca double
      store double 0x3ff0000000000000, double* %".3"
      %".5" = alloca double
      store double 0x4024000000000000, double* %".5"
      br label %"entry.cond"
    entry.cond:
      %".8" = load double, double* %".5"
      %".9" = fcmp ogt double %".8",              0x0
      %".10" = uitofp i1 %".9" to double
      %".11" = fptosi double %".10" to i1
      br i1 %".11", label %"entry.if", label %"entry.endif"
    entry.if:
      %".13" = load double, double* %".3"
      %".14" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".13")
      %".15" = load double, double* %".3"
      %".16" = fmul double %".15", 0x4000000000000000
      store double %".16", double* %".3"
      %".18" = load double, double* %".5"
      %".19" = fsub double %".18", 0x3ff0000000000000
      store double %".19", double* %".5"
      br label %"entry.cond"
    entry.endif:
      ret void
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"