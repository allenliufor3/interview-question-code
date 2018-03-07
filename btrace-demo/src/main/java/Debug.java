import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;

/**
 * @version V1.0 <br/>
 * @description: ${TODO}<br/>
 * @date 2018/1/17 12:05 <br/>
 */
@BTrace
public class Debug {

    @OnMethod(
            clazz="/java\\..*/",
            method="/.*/"
    )
    public static void m(@ProbeClassName String probeClass, @ProbeMethodName String probeMethod) {
        print(Strings.strcat("entered ", probeClass));
        println(Strings.strcat(".", probeMethod));
    }
}
