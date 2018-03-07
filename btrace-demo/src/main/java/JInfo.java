import com.sun.btrace.annotations.*;
import static com.sun.btrace.BTraceUtils.*;

/*
 * A simple sample that prints system properties, flags and exits.
 * This BTrace program mimics the jinfo command line tool in JDK.
 */
@BTrace
public class JInfo {
    static {
        println("System Properties:");
        printProperties();
        println("VM Flags:");
        printVmArguments();
        println("OS Enviroment:");
        printEnv();
        exit(0);
    }
}