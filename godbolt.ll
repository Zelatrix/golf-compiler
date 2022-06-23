@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1

define dso_local i32 @myfun() #0 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  store i32 2, i32* %2, align 4
  %3 = load i32, i32* %2, align 4
  %4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %3)
  %5 = load i32, i32* %1, align 4
  ret i32 %5
}

declare dso_local i32 @printf(i8*, ...) #1
