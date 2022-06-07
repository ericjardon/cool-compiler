-- A let-bound variable can shadow a same-named let-bound variable.
class Example inherits Main {
  y:Int;
  
  do(num:Int, num2:Int) : Object {{
    y<-15;
    let extra:Bool, exxtra:Bool in
      {extra;
      exxtra;
      num;};
  }};

  dont():Object {
    0
  };

  mymain():Object {{
    do(177, 189);
    dont();
  }};
};

class Main inherits IO
{
  x: Int <- 13;
  ex: Example;
  main() : Object {{
    -- ex <- NEW Example; 
    let local:Int<-0 in
      ex.main();
  }};
};
