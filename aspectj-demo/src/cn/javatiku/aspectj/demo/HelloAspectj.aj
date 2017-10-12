package cn.javatiku.aspectj.demo;

public aspect HelloAspectj {

	pointcut HelloWorldPointcut() : execution(* cn.javatiku.aspectj.demo.HelloMain.main(..));

	before():HelloWorldPointcut(){
		System.out.println("before advice...");
	}

	after():HelloWorldPointcut(){
		System.out.println("after advice..");
	}
}
