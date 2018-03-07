import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;

/**
 * @version V1.0 <br/>
 * @description: btrace测试<br/>
 * @date 2018/3/7 13:35 <br/>
 */
@BTrace
public class BtraceDemo {

    @OnMethod(
            clazz = "Demo",
            method = "add",
            location = @Location(Kind.RETURN)
    )
    public static void sayHello(int a, int b, @Return int result) {
        println("a: " + a);
        println("b: " + b);
        println(result);
    }
}
