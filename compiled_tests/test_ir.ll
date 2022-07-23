define void @"main"()
{
    entry:
      %".2" = bitcast [6 x i8]* @"fstr" to i64*
      %".3" = alloca double
      store double 0x4024000000000000, double* %".3"
      br label %"entry.cond"

    entry.cond:
      %".6" = load double, double* %".3"
      %".7" = fcmp ogt double %".6",              0x0
      %".8" = uitofp i1 %".7" to double
      %".9" = fptosi double %".8" to i1
      br i1 %".9", label %"entry.if", label %"entry.endif"

    entry.if:
      %".11" = load double, double* %".3"
      %".12" = call i32 (i64*, ...) @"printf"(i64* %".2", double %".11")
      %".13" = load double, double* %".3"
      %".14" = fsub double %".13", 0x3ff0000000000000
      store double %".14", double* %".3"
      br label %"entry.cond"

    entry.endif:
      ret void
}

declare i32 @"printf"(i64* %".1", ...)

@"fstr" = internal constant [6 x i8] c"%lf \0a\00"